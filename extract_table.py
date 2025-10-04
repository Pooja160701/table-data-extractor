import asyncio
import json
import os
import csv
import gspread
from langchain.docstore.document import Document
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from playwright.async_api import async_playwright
from oauth2client.service_account import ServiceAccountCredentials

JSON_FILE_PATH = "table_data.json"

# Asynchronous function to extract table data from a webpage
async def extract_table(url, timeout=60000, wait_until="networkidle", wait_for_selector="table"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url, timeout=timeout, wait_until=wait_until)
            await page.wait_for_selector(wait_for_selector, timeout=timeout)
            table_data = await page.evaluate("""
            () => {
                const table = document.querySelector('table');
                if (!table) return null;
                let headers = [];
                const thead = table.querySelector('thead');
                if (thead) {
                    headers = Array.from(thead.querySelectorAll('tr th')).map(th => th.innerText.trim());
                } else {
                    const firstRow = table.querySelector('tr');
                    if (firstRow) {
                        headers = Array.from(firstRow.querySelectorAll('td, th')).map(cell => cell.innerText.trim());
                    }
                }
                const rows = [];
                const tbody = table.querySelector('tbody');
                const tableRows = tbody ? tbody.querySelectorAll('tr') : table.querySelectorAll('tr');
                tableRows.forEach((tr, rowIndex) => {
                    if (!thead && rowIndex === 0 && headers.length > 0) return;
                    const cells = Array.from(tr.querySelectorAll('td, th')).map(cell => cell.innerText.trim());
                    const rowObj = {};
                    headers.forEach((header, index) => {
                        rowObj[header] = cells[index] || "";
                    });
                    rows.push(rowObj);
                });
                return {headers, rows};
            }
            """)
        except Exception as e:
            await browser.close()
            raise Exception(f"Error extracting table from {url}: {e}") from e
        await browser.close()
        return table_data

# Function to save table data to JSON file
def save_table_data_to_json(table_data, file_path=JSON_FILE_PATH):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(table_data, f, ensure_ascii=False, indent=4)
    print(f"Table data saved to {file_path}")

# Function to load table data from JSON file
def load_table_data_from_json(file_path=JSON_FILE_PATH):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Function to compare new and old table data
def compare_table_data(new_data, old_data):
    if not old_data:
        return True  # If there's no previous data, consider it changed
    return new_data != old_data

# Converts extracted table data into LangChain Documents
def create_documents_from_table(table_data):
    documents = []
    if table_data:
        headers = table_data.get("headers", [])
        for row in table_data.get("rows", []):
            row_str = "\n".join(f"{header}: {row.get(header, '')}" for header in headers)
            document = Document(page_content=row_str, metadata={"headers": headers})
            documents.append(document)
    return documents

# Function to store documents in vector store
def store_documents_in_vector_store(documents):
    embeddings = OpenAIEmbeddings(openai_api_key="put-your-key-here")
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

# Tool to extract table data from the URL
def table_extraction_tool(url):
    table_data = asyncio.run(extract_table(url))
    return table_data

# Agent to invoke extraction tool and perform other actions
def create_agent():
    tools = [
        Tool(
            name="Table Extraction",
            func=table_extraction_tool,
            description="Extracts table data from the provided URL using Playwright."
        )
    ]
    openai_api_key = "put-your-key-here"
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent

'''"Zero-shot" means the model can handle tasks or provide responses to new situations without requiring additional training or context. 
"React" indicates that the agent responds dynamically to inputs or conditions, and 
"Description" suggests that the agent's function involves generating or interpreting descriptions.'''

# Main function to process the user input and perform operations
if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    table_data = table_extraction_tool(url)
    print(table_data)

    # Load old data from JSON
    old_table_data = load_table_data_from_json()

    # Compare new and old data
    if compare_table_data(table_data, old_table_data):
        print("The table data has changed!")
        save_table_data_to_json(table_data)
        documents = create_documents_from_table(table_data)
        vectorstore = store_documents_in_vector_store(documents)
    else:
        print("No changes in the table data.")

    # Convert JSON to CSV for further processing
    def json_to_csv(json_file, csv_file):
        with open(json_file, 'r', encoding='utf-8') as jsonf:
            data = json.load(jsonf)

        headers = data['headers']
        rows = data['rows']

        with open(csv_file, 'w', newline='', encoding='utf-8') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    json_to_csv('table_data.json', 'table_data.csv')

    # Add data to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open('LangChain')
    worksheet = spreadsheet.get_worksheet(0)

    with open('table_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    worksheet.append_row(data['headers'])

    for row in data['rows']:
        worksheet.append_row(
            [row['row 1'], row['row 2'], row['row 3'], row['row 4'], row['row 5']])
    print(f"Data from 'table_extract.json' has been added to the existing Google Spreadsheet.")