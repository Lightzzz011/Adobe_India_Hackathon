# 🧾 Task 1A – PDF Outline Extractor

This repository contains the solution for **Task 1A** of the Adobe India Hackathon 2025. The challenge is to extract structured outline data from PDF documents in a containerized, resource-efficient manner.

---

## 🐳 Build the Docker Image

docker build --platform linux/amd64 -t task_1a .

▶️ Run the Container

docker run --rm ^
  -v "%cd%/app/input:/app/input:ro" ^
  -v "%cd%/app/output:/app/output" ^
  --network none task_1a
🔁 Make sure your input PDFs are placed in app/input/ and output will be saved in app/output/.

📤 Output Format
Each output is saved as a single JSON file named after the input PDF. The JSON structure includes:

{
  "metadata": {
    "input_documents": [...],
    "persona": "Role",
    "job_to_be_done": "Task",
    "processing_timestamp": "ISO8601 timestamp"
  },
  "extracted_sections": [
    {
      "document": "filename.pdf",
      "section_title": "Top relevant section",
      "importance_rank": 1,
      "page_number": 3
    }
    // ...
  ],
  "subsection_analysis": [
    {
      "document": "filename.pdf",
      "refined_text": "Refined sub-sentence",
      "page_number": 3
    }
    // ...
  ]
}


⚙️ Implementation Guidelines
📈 Performance Considerations
Memory Management: Efficient handling of large PDFs

Processing Speed: Optimized to complete within 10 seconds for 50-page documents

Resource Usage: Must stay under 16GB RAM

CPU Utilization: Efficient use of up to 8 CPU cores


🧪 Testing Strategy
Simple PDFs: Test with basic layouts

Complex PDFs: Handle multi-column, images, tables

Large PDFs: Test with ~50-page files to ensure performance


✅ Validation Checklist
 All PDFs in /app/input/ are processed automatically

 Output JSONs are saved to /app/output/

 Output schema is valid and meaningful

 Processing time ≤ 10 seconds for 50-page PDFs

 Fully works offline (no internet access required)

 Model dependencies ≤ 200MB

 Fully containerized and CPU-only (amd64)
