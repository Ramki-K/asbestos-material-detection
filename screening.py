"""Asbestos SCREENING logic (not a detector).
Matches text from drawings / schedules to a reference list of materials that
are known to contain asbestos in some products. Presence is only ever
confirmed by laboratory analysis of a sample."""
import re
import pandas as pd
from rapidfuzz import fuzz

RISK_RANK = {"High": 3, "Medium": 2, "Low-possible": 1}
LAB_OPTIONS = ["Pending", "Asbestos detected", "Not detected"]
MATCH_THRESHOLD = 85

# Approximate year of the national ban (None = no complete ban / not applied).
# Verify against your local regulator before relying on this.
COUNTRY_BAN_YEAR = {
    "India": None,
    "United Kingdom": 1999,
    "European Union": 2005,
    "Australia": 2003,
    "Canada": 2018,
    "United States": None,
    "Other / unknown": None,
}


def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def load_reference(path="asbestos_reference.csv"):
    ref = pd.read_csv(path).fillna("")
    entries = []
    for _, r in ref.iterrows():
        for alias in str(r["aliases"]).split("|"):
            a = normalize(alias)
            if a:
                entries.append({
                    "alias": a,
                    "ref_id": r["ref_id"],
                    "material_name": r["material_name"],
                    "category": r["category"],
                    "typical_locations": r["typical_locations"],
                    "friable": r["friable"],
                    "risk_level": r["risk_level"],
                    "notes": r["notes"],
                })
    return ref, entries


def alias_score(q, alias):
    if re.search(rf"\b{re.escape(alias)}\b", q):
        return 100.0
    score = fuzz.ratio(q, alias)
    if len(alias) >= 9 and len(q) >= len(alias):
        score = max(score, fuzz.partial_ratio(q, alias))
    return float(score)


def match_text(text, entries, threshold=MATCH_THRESHOLD):
    q = normalize(text)
    if len(q) < 3:
        return None
    best, best_key = None, None
    for e in entries:
        s = alias_score(q, e["alias"])
        if s < threshold:
            continue
        key = (len(e["alias"]), s, RISK_RANK[e["risk_level"]])  # most specific alias wins
        if best_key is None or key > best_key:
            best, best_key = dict(e, score=round(s, 1)), key
    return best


def era_note(year, country):
    if not year:
        return "Construction year not given."
    ban = COUNTRY_BAN_YEAR.get(country)
    if ban is None:
        return (f"Built {year}: no complete national ban applied for {country}; "
                "construction year does NOT reduce the screening risk.")
    if year >= ban:
        return (f"Built {year}: after the ~{ban} ban, so likelihood is lower, but "
                "old stock, imports and reused materials are still possible. Verify.")
    return f"Built {year}: before the ~{ban} ban, when asbestos use was legal and common."


def final_status(risk, lab):
    if lab == "Asbestos detected":
        return "CONFIRMED - asbestos detected by laboratory"
    if lab == "Not detected":
        return "Not detected in the tested sample (applies only to that sample)"
    return {
        "High": "HIGH suspicion - assume asbestos until tested",
        "Medium": "POSSIBLE - sampling recommended",
        "Low-possible": "LOW-POSSIBLE - verify material type",
    }[risk]


def screen(items, entries, country="India", year=0):
    """items: list of (text, ocr_confidence, source). Returns (matched_df, unmatched_df)."""
    matched, unmatched, seen = [], [], set()
    for text, conf, source in items:
        key = normalize(text)
        if not key or key in seen:
            continue
        seen.add(key)
        m = match_text(text, entries)
        if m is None:
            unmatched.append({"Text found": text, "OCR confidence": round(float(conf), 3),
                              "Source": source})
            continue
        matched.append({
            "Text found": text,
            "Source": source,
            "OCR confidence": round(float(conf), 3),
            "OCR check": "Low OCR confidence - verify text" if (source == "image" and conf < 0.4) else "OK",
            "Matched material": m["material_name"],
            "Category": m["category"],
            "Match score": m["score"],
            "Likelihood": m["risk_level"],
            "Friable": m["friable"],
            "Typical locations": m["typical_locations"],
            "Notes": m["notes"],
            "Era note": era_note(year, country),
            "Lab result": "Pending",
        })
    cols_m = ["Text found","Source","OCR confidence","OCR check","Matched material","Category",
              "Match score","Likelihood","Friable","Typical locations","Notes","Era note","Lab result"]
    mdf = pd.DataFrame(matched, columns=cols_m)
    if len(mdf):
        mdf["_r"] = mdf["Likelihood"].map(RISK_RANK)
        mdf = mdf.sort_values("_r", ascending=False).drop(columns="_r").reset_index(drop=True)
    udf = pd.DataFrame(unmatched, columns=["Text found", "OCR confidence", "Source"])
    return mdf, udf


def add_status(mdf):
    mdf = mdf.copy()
    mdf["Screening status"] = [final_status(r, l) for r, l in zip(mdf["Likelihood"], mdf["Lab result"])]
    return mdf
