FROM python:3.10-slim

# Install system dependencies for PyMuPDF
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /app/input /app/output

# Copy only what's needed
COPY ./app /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app

# Run command (now main.py is in /app directly)
CMD ["python", "-u", "main.py"]