# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the maintainer label (optional)
LABEL authors="pooja"

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 (optional, can be used if you plan to create a web app or need a port for external access)
# EXPOSE 80

# Set environment variables (if needed, such as for OpenAI API key or Google Sheets credentials)
# ENV OPENAI_API_KEY="your-openai-api-key"
# ENV GOOGLE_SHEETS_CREDS="your-credentials.json-path"

# Run the script when the container starts
CMD ["python", "extract_table.py"]
