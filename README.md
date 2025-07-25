# Fake Organization Data Generator

This project contains a set of Python scripts to generate fake, but realistic, organizational data, including:

*   **Calendars:** Generates `.ics` files with random, non-overlapping meetings for a set of users across multiple domains.
*   **Emails:** Extracts sample emails from a large dataset (like the Enron corpus) and packages them into `.mbox` files.

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
