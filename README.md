# Asbestos Screening Tool for Building Drawings

An OCR-based application for extracting material descriptions from building drawings and matching them against a reference database to support preliminary asbestos risk screening.

## Overview

Building drawings and material schedules may contain technical descriptions of construction materials. Reviewing these descriptions manually can be time-consuming.

This project combines Optical Character Recognition (OCR), image processing, text matching, and an interactive Streamlit interface to help identify materials that may require further asbestos assessment.

**Important:** This tool provides preliminary screening only. It cannot confirm the presence or absence of asbestos.

## Key Features

- **Drawing and Image Upload:** Upload building drawings or photographs of material schedules.
- **OCR-Based Text Extraction:** Extract text from supported images using EasyOCR.
- **Enhanced OCR:** Optionally process an enhanced image copy to help detect additional text.
- **Manual Material Entry:** Enter material descriptions directly for screening.
- **CSV and Excel Upload:** Upload material schedules for processing.
- **Database Matching:** Compare extracted material descriptions with a reference materials database.
- **Screening Results:** Review matched materials, likelihood indicators, and screening statuses.
- **Report Export:** Download screening results as a CSV report.
- **Country and Construction-Year Inputs:** Provide contextual information for preliminary screening.

## Technology Stack

- Python
- Streamlit
- EasyOCR
- OpenCV
- Pandas
- NumPy
- RapidFuzz
- Pillow

## Application Workflow

1. Upload a building drawing, material schedule, or image.
2. Extract text using OCR, or enter material descriptions manually.
3. Process and normalize the extracted text.
4. Match material descriptions against the reference database.
5. Review the screening results and unmatched text.
6. Export the report for further review.

## Repository Structure

```text
asbestos-material-detection/
├── README.md
├── app.py
├── screening.py
├── requirements.txt
├── asbestos_reference.csv
└── Asbestos_Screening_Colab.ipynb
```

The repository contains the application code, screening logic, reference data, documentation, and development notebook. The CSV filename shown above is illustrative; use the exact filename committed to the repository.

## Installation

### 1. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/asbestos-material-detection.git
cd asbestos-material-detection
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

EasyOCR also depends on PyTorch. Its required model weights may be downloaded during the first run.

## Run the Application

Start the Streamlit application from the project directory:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

Ensure that the reference database is available at the file path expected by the application.

## Current Status

The application has been developed and tested through a Google Colab-based workflow. GitHub is used to maintain the source code and project documentation.

Further testing is needed to evaluate OCR quality, database-matching reliability, and deployment compatibility across different building drawings.

## Limitations

- OCR performance may vary with image resolution, rotation, image quality, and complex drawing layouts.
- Abbreviations and ambiguous material descriptions can produce incorrect or incomplete matches.
- The reference database may not contain every material or product description.
- A missing database match does not mean that a material is asbestos-free.
- A positive text match does not establish the actual asbestos content of a material.

## Safety Disclaimer

This application is intended for research and preliminary screening. It is not a certified asbestos detection system and must not be used as definitive evidence of asbestos presence or absence.

Do not drill, cut, break, or sample suspected materials yourself. Consult a qualified asbestos professional and use appropriate laboratory analysis and applicable local procedures.

## Future Improvements

- Improve OCR performance on technical drawings and material schedules.
- Introduce more robust material-name normalization and fuzzy matching.
- Evaluate the system against a labeled test dataset.
- Improve reporting of ambiguous matches and confidence levels.
- Expand the reference database using verified, appropriately licensed information.
