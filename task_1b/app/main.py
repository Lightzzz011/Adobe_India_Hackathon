import os, json, re
import pdfplumber
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

INPUT_ROOT = "/app/input"
OUTPUT_ROOT = "/app/output"


def extract_keywords(text):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    return [w for w in words if w not in ENGLISH_STOP_WORDS]


def extract_text_blocks(pdf_path):
    blocks = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    for para in text.split("\n"):
                        para = para.strip()
                        if len(para.split()) > 4:
                            blocks.append({"text": para, "page": i + 1})
    except Exception as e:
        print(f" Failed to read PDF {pdf_path}: {e}")
    return blocks


def is_irrelevant(text):
    return len(text.split()) < 4 or len(text) < 20


def score_blocks(blocks, query, boost_keywords):
    texts = [b["text"] for b in blocks]
    if not texts:
        return []

    tfidf = TfidfVectorizer().fit(texts + [query])
    query_vec = tfidf.transform([query])
    scores = cosine_similarity(query_vec, tfidf.transform(texts)).flatten()

    results = []
    for b, s in zip(blocks, scores):
        boost = sum(1 for kw in boost_keywords if kw in b["text"].lower())
        penalty = 0.1 if is_irrelevant(b["text"]) else 0
        total_score = s + 0.15 * boost - penalty
        results.append({"text": b["text"], "page": b["page"], "score": float(total_score)})

    return sorted(results, key=lambda x: -x["score"])


def extract_subsections(text):
    phrases = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in phrases if 20 < len(p) <= 200]


def process_collection(collection_path, collection_name):
    config_path = os.path.join(collection_path, "config.json")
    if not os.path.exists(config_path):
        print(f" Skipping {collection_name}: config.json not found.")
        return

    print(f"\n Processing collection: {collection_name}")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    persona = config.get("persona", {}).get("role", "")
    job = config.get("job_to_be_done", {}).get("task", "")
    docs = config.get("documents", [])
    if not persona or not job or not docs:
        print(" Missing keys in config.json")
        return

    full_query = f"{persona}: {job}"
    boost_keywords = extract_keywords(job + " " + persona)

    print(f" Persona: {persona}")
    print(f" Job: {job}")
    print(f" Files: {[doc['filename'] for doc in docs]}")

    extracted_sections = []
    subsection_analysis = []

    for doc in docs:
        filename = doc["filename"]
        file_path = os.path.join(collection_path, filename)
        if not os.path.exists(file_path):
            print(f" Missing file: {filename}")
            continue

        blocks = extract_text_blocks(file_path)
        if not blocks:
            print(f" No valid blocks in {filename}")
            continue

        top_blocks = score_blocks(blocks, full_query, boost_keywords)[:5]
        for rank, item in enumerate(top_blocks, 1):
            extracted_sections.append({
                "document": filename,
                "section_title": item["text"][:80].strip(),
                "importance_rank": rank,
                "page_number": item["page"]
            })
            for sub in extract_subsections(item["text"]):
                subsection_analysis.append({
                    "document": filename,
                    "refined_text": sub,
                    "page_number": item["page"]
                })

    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in docs],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    out_path = os.path.join(OUTPUT_ROOT, f"{collection_name}_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f" Output saved to: {out_path}")


def process_all():
    print(" Starting PDF Persona Extractor...")
    if not os.path.exists(INPUT_ROOT):
        print(f" Input directory missing: {INPUT_ROOT}")
        return

    for entry in os.listdir(INPUT_ROOT):
        full_path = os.path.join(INPUT_ROOT, entry)
        if os.path.isdir(full_path):
            process_collection(full_path, entry)

    print(" All collections processed.")


if __name__ == "__main__":
    process_all()
