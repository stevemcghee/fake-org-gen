# Fake Organization Data Generator

This project contains a set of Python scripts to generate fake, but realistic, organizational data, including:

*   **Calendars:** Generates `.ics` files with random, non-overlapping meetings for a set of users across multiple domains.
*   **Emails:** Extracts sample emails from a large dataset (like the Enron corpus) and packages them into `.mbox` files.
*   **Documents:** Generates a variety of themed documents, spreadsheets, presentations, and AI-generated images.

## Quick Start

The `generate_all.py` script provides a single entry point to run all the data generation scripts at once. It uses a `config.json` file to configure the output.

### Setup

1.  **Create a `config.json` file:**

    Copy the `config.example.json` file to `config.json`. The `config.json` file defines the global `domain` and `users` for the generated data, as well as the settings for each module.

    ```bash
    cp config.example.json config.json
    ```

2.  **Install Dependencies:**

    Each subdirectory may have its own `requirements.txt` file. Install the dependencies for each module you intend to use.

    ```bash
    pip install -r calendar/requirements.txt
    pip install -r docs/requirements.txt
    pip install -r email/requirements.txt
    ```

3.  **Set API Key:**

    The document generation script requires a Gemini API key. Make sure to set it as an environment variable:

    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```

### Usage

Run the `generate_all.py` script from the root of the project.

```bash
python3 generate_all.py
```

You can also specify a different config file:

```bash
python3 generate_all.py --config my_custom_config.json
```

### Configuration

The `config.json` file allows for detailed configuration of the generated data.

**Global Options:**

*   `domain`: The domain name to use for email addresses and calendar invites.
*   `users`: A dictionary of users to generate data for. The key is the username, and the value is a list containing the user's full name and email prefix.

**Calendar Options (`calendar`):**

*   `months_to_generate`: The number of months to generate events for.
*   `num_events_range`: A list containing the minimum and maximum number of events to generate per month.
*   `location`: The default location for events.
*   `shared_event_types`: A list of event titles for meetings with multiple attendees.
*   `solo_event_types`: A list of event titles for events with a single attendee.

**Email Options (`email`):**

*   `num_samples`: The total number of emails to extract from the source file.
*   `output_dir`: The directory to save the generated `.mbox` files.
*   `num_mbox_files`: The number of `.mbox` files to split the emails into.

**Document Options (`docs`):**

*   `num_files`: The number of files to generate per user.
*   `org_name`: The name of the organization to use in the generated documents.
*   `theme`: The theme to use for the generated documents.
*   `file_types`: A list of file types to generate (e.g., "document", "spreadsheet", "presentation", "image").
*   `doc_types`: A list of document types to generate (e.g., "Internal Memo", "Project Proposal").
*   `sheet_types`: A list of spreadsheet types to generate (e.g., "Financial Statement", "Sales Tracker").
*   `ppt_types`: A list of presentation types to generate (e.g., "Quarterly Review", "New Product Pitch").

## Individual Scripts

### Setup

#### 1. Get the Enron Email Corpus

This project uses the Enron email dataset for its email generation features. To get the required `emails.csv` file, you first need to download the dataset.

Run the following command in your terminal to download the dataset to your `~/Downloads` folder.

```bash
#!/bin/bash
curl -L -o ~/Downloads/enron-email-dataset.zip -C - \
  https://www.kaggle.com/api/v1/datasets/download/wcukierski/enron-email-dataset
```

After downloading, unzip the `enron-email-dataset.zip` file. Inside, you will find `emails.csv`.

#### 2. Place the Data File

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

### Fake File Generator

The `docs/generate_files.py` script leverages the Gemini API to generate a variety of realistic, themed business files.

**Features**

- Takes an arbitrary business theme via the command line.
- Generates unique content for every file.
- Creates a variety of documents (memos, proposals), spreadsheets (financial statements, sales trackers), presentations (quarterly reviews, product pitches), and AI-generated images.
- Uses AI-generated titles for descriptive filenames.
- Formats presentations with concise, AI-generated bullet points.

**Setup**

1.  **Install Dependencies:** Navigate to the `docs` directory and install the required Python packages.
    ```bash
    cd docs
    pip install -r requirements.txt
    ```

2.  **Set API Key:** The script requires a Gemini API key. Set it as an environment variable.
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```

**Usage**

Run the script from within the `docs` directory, providing a theme.

```bash
python3 generate_files.py --theme "Financial services for Ents in Middle-earth"
```

You can also customize the users, number of files, and organization name:

```bash
python3 generate_files.py --theme "Lembas bread bakery in Lothlorien" --users galadriel legolas --num-files 10 --org-name "Lothlorien Lembas Co."
```