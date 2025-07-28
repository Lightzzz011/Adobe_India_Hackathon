Challenge 1a: PDF Processing Solution
Overview
This is a sample solution for Challenge 1a of the Adobe India Hackathon 2025. The challenge requires implementing a PDF processing solution that extracts structured data from PDF documents and outputs JSON files. The solution must be containerized using Docker and meet specific performance and resource constraints.

Critical Constraints
Execution Time: ≤ 10 seconds for a 50-page PDF
Model Size: ≤ 200MB (if using ML models)
Network: No internet access allowed during runtime execution
Runtime: Must run on CPU (amd64) with 8 CPUs and 16 GB RAM
Architecture: Must work on AMD64, not ARM-specific

Key Requirements
Automatic Processing: Process all PDFs from /app/input directory
Output Format: Generate filename.json for each filename.pdf
Input Directory: Read-only access only
Open Source: All libraries, models, and tools must be open source
Cross-Platform: Test on both simple and complex PDFs
Sample Solution Structure

task_1a/
├── app/
│ ├── input/ # Input PDFs (mounted read-only)
│ ├── output/ # Extracted output JSONs
│ ├── main.py # Main PDF extractor script
│ ├── utils.py # Helper functions
├── Dockerfile # Docker container definition
└── requirements.txt # Python dependencies


Implementation Guidelines
Performance Considerations
Memory Management: Efficient handling of large PDFs
Processing Speed: Optimize for sub-10-second execution
Resource Usage: Stay within 16GB RAM constraint
CPU Utilization: Efficient use of 8 CPU cores
Testing Strategy
Simple PDFs: Test with basic PDF documents
Complex PDFs: Test with multi-column layouts, images, tables
Large PDFs: Verify 50-page processing within time limit
Testing Your Solution
Local Testing
# Build the Docker image
docker build --platform linux/amd64 -t task_1a .

# Test with sample data
docker run --rm ^
-v "%cd%/app/input:/app/input:ro" ^
-v "%cd%/app/output:/app/output" ^
--network none task_1a

Validation Checklist
 All PDFs in input directory are processed
 JSON output files are generated for each PDF
 Output format matches required structure
 Output conforms to schema in sample_dataset/schema/output_schema.json
 Processing completes within 10 seconds for 50-page PDFs
 Solution works without internet access
 Memory usage stays within 16GB limit
 Compatible with AMD64 architecture
