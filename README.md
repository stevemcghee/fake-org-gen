# Fake Organization Data Generator

This project contains a set of Python scripts to generate fake, but realistic, organizational data, including:

*   **Calendars:** Generates `.ics` files with random, non-overlapping meetings for a set of users across multiple domains.
*   **Emails:** Extracts sample emails from a large dataset (like the Enron corpus) and packages them into `.mbox` files.
*   **Documents:** Generates a variety of themed documents, spreadsheets, presentations, and AI-generated images.

## Setup

### 1. Get the Enron Email Corpus

This project uses the Enron email dataset for its email generation features. To get the required `emails.csv` file, you first need to download the dataset.

Run the following command in your terminal to download the dataset to your `~/Downloads` folder.

```bash
#!/bin/bash
curl -L -o ~/Downloads/enron-email-dataset.zip -C - \
  https://www.kaggle.com/api/v1/datasets/download/wcukierski/enron-email-dataset
```

After downloading, unzip the `enron-email-dataset.zip` file. Inside, you will find `emails.csv`.

### 2. Place the Data File

Move the `emails.csv` file into the `email/` directory within this project. The scripts are configured to look for it there.

The final structure should look like this:

```
fake-org-gen/
├── calendar/
│   └── generate_events.py
└── email/
    ├── emails.csv  <-- Place the file here
    └── ... (other scripts)
```

## Fake File Generator

The `docs/generate_files.py` script leverages the Gemini API to generate a variety of realistic, themed business files.

### Features

- Takes an arbitrary business theme via the command line.
- Generates unique content for every file.
- Creates a variety of documents (memos, proposals), spreadsheets (financial statements, sales trackers), presentations (quarterly reviews, product pitches), and AI-generated images.
- Uses AI-generated titles for descriptive filenames.
- Formats presentations with concise, AI-generated bullet points.
- Sanitizes filenames to prevent errors.

### Setup

1.  **Install Dependencies:**

    Navigate to the `docs` directory and install the required Python packages.

    ```bash
    cd docs
    pip install -r requirements.txt
    ```

2.  **Set API Key:**

    This script requires a Gemini API key. Make sure to set it as an environment variable:

    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```

### Usage

Run the script from within the `docs` directory, providing a theme for the generated content.

```bash
python3 generate_files.py --theme "Financial services for Ents in Middle-earth"
```

You can also customize the users, number of files, and organization name:

```bash
python3 generate_files.py --theme "Gondor-based catering company" --users legolas aragorn --num-files 10 --org-name "Gondor Gastronomy"
```

The script will create an `output` directory structured by username, filled with `.docx`, `.xlsx`, `.pptx`, and `.png` files.