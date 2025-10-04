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

## Building and Running the Docker Container

1. Build the Docker image:
   ```bash
   docker build -t table-data-extractor .

2. Run the Docker container:
   ```bash
   docker run -it table-data-extractor

The -it flag ensures you can interact with the container (if your script has inputs, like the URL for table extraction).

**Notes:**

- API Key and Credentials:
- Make sure to handle your API keys and credentials securely. You can either:
- Pass them as environment variables when running the container:
   ```bash
   docker run -it -e OPENAI_API_KEY="your-api-key" -e GOOGLE_SHEETS_CREDS="/path/to/creds.json" table-data-extractor
- Or use Docker volumes to mount local files (like your credentials.json) into the container:
   ```bash
   docker run -it -v /path/to/your/credentials.json:/app/credentials.json table-data-extractor
- Make sure the .gitignore worked and sensitive files like credentials.json aren’t uploaded.
