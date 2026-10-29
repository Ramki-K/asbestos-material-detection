# asbestos-material-detection
OCR-based material extraction and database matching for asbestos risk screening in building drawings.
# Asbestos Material Detection Using OCR and Database Matching

## Overview

This project explores an OCR-based approach to extracting material names and specifications from architectural and structural building drawings and matching the extracted information against a reference materials database.

The goal is to support preliminary screening of building materials for potential asbestos-related risks using text extraction and database matching.

## Problem Statement

Architectural and structural drawings may contain material descriptions, product specifications, abbreviations, and other technical annotations. Reviewing these documents manually can be time-consuming.

This project explores a workflow that combines Optical Character Recognition (OCR), text processing, and database matching to identify material descriptions that may require further asbestos-related review.

## Objectives

- Extract text from building drawing images using OCR.
- Process and normalize detected material descriptions.
- Match extracted text against a reference materials database.
- Display potential matches and matching results.
- Provide an interactive interface for testing the workflow.

## Project Workflow

1. **Input:** Upload a supported building drawing or document image.
2. **OCR:** Detect text regions and recognize material-related text.
3. **Text processing:** Clean and normalize the extracted text.
4. **Database matching:** Compare extracted descriptions with entries in the reference database.
5. **Result display:** Present extracted text, matched records, and relevant screening results through the application interface.

## Technologies Used

- Python
- Optical Character Recognition (OCR)
- Image Processing
- Text Processing and String Matching
- Pandas
- Streamlit
- CSV-based material reference database

*Update this list to reflect the libraries and methods actually implemented in the code.*

## Repository Structure

```text
asbestos-material-detection/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── material_matching_test.csv
└── screenshots/
    └── application_demo.png
```

*Adjust the structure and filenames to match the files included in the repository.*

## Installation

### 1. Clone the repository

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

## Run the Application

If the Streamlit application is saved as `app.py`, run:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

Upload a supported sample drawing and review the OCR extraction and material-matching results.

## Current Status

This project is under development. OCR extraction, database matching, and the application workflow are being tested. Detection quality and matching reliability depend on drawing quality, OCR performance, and the coverage of the reference database.

## Limitations and Safety

- OCR may misread text in low-resolution, rotated, handwritten, or complex technical drawings.
- Material descriptions may be ambiguous, abbreviated, or missing from the reference database.
- A text match does not establish that a product contains asbestos.
- The application is a preliminary screening and research tool, not a substitute for qualified asbestos assessment, laboratory testing, or applicable regulatory procedures.

## Future Improvements

- Improve OCR performance on architectural and engineering drawings.
- Add confidence scores and more robust fuzzy matching.
- Support structured extraction of material specifications.
- Expand the reference database using verified and appropriately licensed sources.
- Evaluate extraction and matching performance on a labeled test dataset.
- Improve the interface and reporting of uncertain results.

## Disclaimer

This project is intended for research and preliminary screening only. Its outputs must not be used as definitive confirmation of asbestos presence or absence. Suspected materials should be assessed by qualified professionals using appropriate procedures.

## Author

Ramakrishnan K  
M.Tech, Energy Science and Technology  
Indian Institute of Technology Hyderabad
