import os
import fitz  
import json
from utils import is_valid_heading, guess_level
from collections import defaultdict

MY_INBOX = "/app/input"
MY_OUTBOX = "/app/output"

def analyze_document_stats(doc):
    """Collect document-wide statistics for better level detection"""
    size_freq = defaultdict(int)
    style_freq = defaultdict(int)
    
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span.get("size", 0), 1)
                    if size >= 10:
                        size_freq[size] += 1
                        style_freq[(size, span.get("flags", 0), span.get("font"))] += 1
    
    size_ranges = sorted(size_freq.keys(), reverse=True)[:3]
    return {
        'size_ranges': size_ranges,
        'style_freq': style_freq
    }

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    doc_stats = analyze_document_stats(doc)
    
    title = doc.metadata.get("title", "") or os.path.basename(pdf_path).replace('.pdf', '')
    outline = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if block.get("type", 0) != 0:
                continue

            lines_in_block = block.get("lines", [])
            if len(lines_in_block) > 2:
                continue  

            block_text = ""
            font_sizes = []
            is_bold = False

            for line in lines_in_block:
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if text:
                        block_text += text + " "
                        font_sizes.append(span.get("size", 0))
                        if not is_bold and (span.get("flags", 0) & 2 != 0 or "bold" in span.get("font", "").lower()):
                            is_bold = True

            block_text = block_text.strip()
            if not block_text or not font_sizes or not is_valid_heading(block_text):
                continue

            if len(block_text) > 75:
                continue  # too long to be a heading

            avg_size = sum(font_sizes) / len(font_sizes)
            level = guess_level(avg_size, doc_stats)

            if level:
                outline.append({
                    "level": level,
                    "text": block_text,
                    "page": page_num + 1
                })

    print(f" {pdf_path} → Extracted {len(outline)} headings")
    return {
        "title": title,
        "outline": outline
    }

def lets_go():
    print(" Checking input folder contents...")
    print(os.listdir(MY_INBOX))

    for f in os.listdir(MY_INBOX):
        print(f" Found file: {f}")
        if f.lower().endswith(".pdf"):
            input_path = os.path.join(MY_INBOX, f)
            print(f" Processing: {input_path}")
            result = process_pdf(input_path)

            output_file = os.path.splitext(f)[0] + ".json"
            output_path = os.path.join(MY_OUTBOX, output_file)

            print(f" Writing output to: {output_path}")
            with open(output_path, "w", encoding="utf-8") as out_f:
                json.dump(result, out_f, indent=2, ensure_ascii=False)
        else:
            print(f" Skipping non-PDF file: {f}")

if __name__ == "__main__":
    lets_go()
