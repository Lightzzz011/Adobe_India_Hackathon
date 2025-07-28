# 🧾 Task 1A – PDF Outline Extractor

This repository contains a Dockerized solution for **Task 1A** of the **Adobe India Hackathon 2025**. The goal is to extract structured section-level and sub-section-level outlines from PDF documents, conforming to strict runtime, output, and architectural constraints.

## 📌 Objective

Automatically extract the most relevant content from input PDF documents based on a predefined persona and job-to-be-done context. The output is a well-ranked list of section titles and refined granular subsections, all saved in a structured JSON format.

## 📁 Directory Structure
task_1a/
├── app/
│ ├── input/
│ ├── output/
│ ├── main.py
│ ├── utils.py
├── Dockerfile
└── requirements.txt


## ⚙️ Tech Stack

- Python 3.10+
- pdfplumber
- scikit-learn
- Docker

## 🚀 How to Run

### Build the Docker Image
```bash
docker build --platform linux/amd64 -t task_1a .
Run the Container
bash
Copy
Download
docker run --rm \
  -v "$(pwd)/app/input:/app/input:ro" \
  -v "$(pwd)/app/output:/app/output" \
  --network none task_1a
📤 Output Format
json
Copy
Download
{
  "metadata": {
    "input_documents": ["file.pdf"],
    "persona": "Role",
    "job_to_be_done": "Task"
  },
  "extracted_sections": [
    {
      "document": "file.pdf",
      "section_title": "Section",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "file.pdf",
      "refined_text": "Subsection",
      "page_number": 1
    }
  ]
}
✅ Validation
Processes all PDFs automatically

Generates valid JSON output

Completes within 10s per 50-page PDF

Works offline

≤200MB dependencies

AMD64 compatible
