# Table Data Extractor

This Python script scrapes tabular data from a provided URL, saves the data to a JSON file, converts the JSON to CSV, and then uploads the data to a Google Sheets document.

## Features
- Scrape table data from a webpage using Playwright
- Save the scraped data to a JSON file
- Compare new and old data for changes
- Convert JSON to CSV format
- Upload data to Google Sheets

## Installation

### Prerequisites
You need the following to run the script:
- Python 3.x
- Google Sheets API credentials (`credentials.json` file)
- OpenAI API key for embeddings

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/table-data-extractor.git
   cd table-data-extractor

2. Install dependencies:
   ```bash
   pip install - r requirements.txt

3. Set up your Google Sheets API credentials:

4. Follow the Google Sheets API documentation to create and download credentials.json.

5. Get an OpenAI API key from OpenAI.

6. Run the script:
   ```bash
   python extract_table.py

7. Usage:
  When running the script, enter the URL of the page with the table data when prompted.
Your code files (including extract_table.py, .gitignore, etc.) are all there.

Make sure the .gitignore worked and sensitive files like credentials.json aren’t uploaded.
