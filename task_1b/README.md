# 🔍 Task 1B: Persona-Based PDF Section Extractor

This repository contains the solution for **Challenge 1B** of the **Adobe India Hackathon 2025**.  
The objective is to extract **relevant sections and subsections** from a collection of PDFs based on a provided persona and job-to-be-done description.

---

## 🚀 Objective

Given:
- A set of PDF documents
- A `config.json` containing:
  - `persona`: The role or profile of the user
  - `job_to_be_done`: Their specific task
  - `documents`: List of PDF filenames

You must extract:
1. The most relevant **sections** (ranked)
2. The best **sub-sections/sentences** from those sections

---

## ✅ Output Format

The output is a single JSON file per collection with the following structure:

```json
{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "processing_timestamp": "..."
  },
  "extracted_sections": [
    {
      "document": "...",
      "section_title": "...",
      "importance_rank": 1,
      "page_number": ...
    }
  ],
  "subsection_analysis": [
    {
      "document": "...",
      "refined_text": "...",
      "page_number": ...
    }
  ]
}


📦 Directory Structure

task_1b/
├── app/
│   ├── input/
│   │   ├── collection_1/
│   │   │   ├── config.json
│   │   │   ├── file1.pdf
│   │   │   └── file2.pdf
│   │   └── collection_2/...
│   ├── output/                   # JSON outputs saved here
│   └── main.py                   # Main persona extractor script
├── Dockerfile                    # Docker config
└── requirements.txt              # Python dependencies


🧠 Key Features
✅ Works for any collection — not tied to food-specific keywords

📄 Parses and scores all text blocks in each PDF

💡 Combines TF-IDF similarity + keyword boosting

🧠 Extracts ranked sections and important subphrases

🔒 Runs offline with no network dependency

🐳 Fully Dockerized and lightweight (CPU only, <1GB memory)


⚙️ Build & Run
🛠️ Build Docker Image
From the task_1b/ directory:


docker build --platform linux/amd64 -t pdf-persona .
▶️ Run the Extractor

docker run --rm -v "%cd%/app/input:/app/input" -v "%cd%/app/output:/app/output" pdf-persona
📝 Use $(pwd) instead of %cd% on Linux/macOS.

📋 Sample Config (config.json)

{
  "persona": {
    "role": "Food Contractor"
  },
  "job_to_be_done": {
    "task": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
  },
  "documents": [
    { "filename": "Lunch Ideas.pdf" },
    { "filename": "Dinner Ideas - Sides_1.pdf" }
  ]
}
🏁 Scoring Criteria
Criteria	Max Points
Section Relevance	60
Sub-section Relevance	40

This implementation targets a score ≥ 85 consistently across collections.

⚠️ Constraints Handled
✅ CPU-only, model size < 1GB

✅ Processes 3–5 PDFs in < 60s

✅ No internet access

✅ Cross-collection compatibility (not hardcoded)
