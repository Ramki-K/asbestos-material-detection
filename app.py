import io
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from screening import (load_reference, screen, add_status, COUNTRY_BAN_YEAR,
                       LAB_OPTIONS, RISK_RANK)

st.set_page_config(page_title="Asbestos Screening Tool", layout="wide")
st.title("Asbestos Screening Tool for Building Drawings")
st.warning(
    "This tool SCREENS for materials that may contain asbestos. It cannot tell you "
    "that asbestos is absent. Presence or absence is confirmed only by laboratory "
    "analysis of a sample taken by a trained, licensed professional. Do not drill, "
    "cut, break or sample suspect material yourself."
)

ref, entries = load_reference("asbestos_reference.csv")


@st.cache_resource
def load_reader():
    import easyocr
    try:
        import torch
        gpu = torch.cuda.is_available()
    except Exception:
        gpu = False
    return easyocr.Reader(["en"], gpu=gpu)


def ocr_image(pil_img, also_enhanced=True):
    reader = load_reader()
    arr = np.array(pil_img.convert("RGB"))
    found = [(t, c) for _, t, c in reader.readtext(arr)]
    if also_enhanced:
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
        found += [(t, c) for _, t, c in reader.readtext(gray)]
    return found


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Building details")
    country = st.selectbox("Country / region", list(COUNTRY_BAN_YEAR.keys()))
    year = st.number_input("Year of construction (0 = unknown)", 0, 2100, 0, 1)
    st.caption("Era rules are approximate. Confirm with your local regulator.")
    st.divider()
    with st.expander("Reference dataset"):
        st.dataframe(ref[["ref_id", "material_name", "category", "risk_level", "friable"]],
                     hide_index=True)

# ---------------- Inputs ----------------
col1, col2 = st.columns(2)
with col1:
    images = st.file_uploader("Upload drawings / photos of material schedules",
                              type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    enhance = st.checkbox("Also scan a 2x enhanced copy (slower, finds more text)", True)
with col2:
    typed = st.text_area(
        "Or type / paste materials (one per line)",
        placeholder="Roof: AC sheet\nPipe insulation in boiler room\nCeiling tiles 600x600\nVinyl floor tile",
        height=180)
    sched = st.file_uploader("Or upload a material schedule (CSV / Excel)",
                             type=["csv", "xlsx"])

if st.button("Run screening", type="primary"):
    items = []
    with st.spinner("Reading inputs..."):
        for f in images or []:
            for t, c in ocr_image(Image.open(f), enhance):
                items.append((t, c, "image"))
        for line in typed.splitlines():
            if line.strip():
                items.append((line.strip(), 1.0, "typed"))
        if sched is not None:
            df_s = pd.read_csv(sched) if sched.name.lower().endswith(".csv") else pd.read_excel(sched)
            for v in df_s.astype(str).values.ravel():
                if v and v.lower() != "nan":
                    items.append((v, 1.0, "schedule"))
    if not items:
        st.error("Nothing to screen. Upload an image, paste text or upload a schedule.")
    else:
        m, u = screen(items, entries, country, int(year))
        st.session_state["matched"] = m
        st.session_state["unmatched"] = u

# ---------------- Results ----------------
if "matched" in st.session_state:
    matched = st.session_state["matched"]
    unmatched = st.session_state["unmatched"]

    st.subheader("1. Suspect materials found")
    if matched.empty:
        st.info("No suspect materials were recognised in the input. This is NOT an "
                "asbestos clearance. The drawing may simply not list materials.")
    else:
        st.caption("After a laboratory report arrives, set 'Lab result' for that row.")
        shown = ["Text found", "Matched material", "Likelihood", "Friable", "Lab result",
                 "OCR check", "Match score", "Typical locations", "Notes", "Era note", "Source"]
        edited = st.data_editor(
            matched[shown],
            hide_index=True,
            
            disabled=[c for c in shown if c != "Lab result"],
            column_config={"Lab result": st.column_config.SelectboxColumn(
                "Lab result", options=LAB_OPTIONS, required=True)},
            key="editor",
        )
        full = matched.copy()
        full["Lab result"] = edited["Lab result"].values
        report = add_status(full)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("HIGH suspicion", int((report["Likelihood"] == "High").sum()))
        c2.metric("Possible / low-possible", int((report["Likelihood"] != "High").sum()))
        c3.metric("Confirmed by lab", int((report["Lab result"] == "Asbestos detected").sum()))
        c4.metric("Awaiting lab", int((report["Lab result"] == "Pending").sum()))

        st.subheader("2. Screening status")
        st.dataframe(report[["Text found", "Matched material", "Likelihood",
                             "Lab result", "Screening status"]],
                     hide_index=True)

        st.download_button("Download full report (CSV)",
                           report.to_csv(index=False).encode("utf-8"),
                           "asbestos_screening_report.csv", "text/csv")

        st.subheader("3. Next steps")
        st.markdown(
            "1. Do **not** disturb HIGH and POSSIBLE items.\n"
            "2. Ask a licensed asbestos surveyor to inspect and take samples.\n"
            "3. Send samples to an accredited laboratory.\n"
            "4. Enter the lab result above to update the status.\n"
            "5. Follow your local rules for management or removal.")

    with st.expander(f"Text that matched nothing ({len(unmatched)}) - review manually"):
        st.caption("Room names and unreadable text land here. Unmatched does not mean safe.")
        st.dataframe(unmatched, hide_index=True)
