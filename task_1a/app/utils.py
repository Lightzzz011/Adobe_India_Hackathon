import re

def is_valid_heading(text):
    """Filter out non-heading text with refined rules for general PDFs."""

    text = text.strip()
    if not text or len(text.split()) < 2:
        return False

    # ❌ Discard full sentences
    if text.endswith(".") or text.endswith("?"):
        return False

    # ❌ Reject lines that start lowercase (e.g., 'description of', 'example:')
    if text[0].islower():
        return False

    # ❌ Reject alphabetic or numeric bullet points like 'a. ...', '1.', 'i)'
    if re.match(r'^\(?[a-zA-Z0-9]{1,3}[\.\)]\s', text):
        return False

    # ❌ Reject code blocks, JSON, URLs, special formatting
    invalid_patterns = [
        r'^\s*[-•]\s+',       # Bullet points
        r'^\{.*\}$',          # JSON-looking block
        r'^https?://',        # URL
        r'^\s*```',           # Markdown code block
        r'[{}<>]',            # Markup symbols
    ]
    if any(re.match(p, text) for p in invalid_patterns):
        return False

    # ✅ Heuristic: Check capitalized word ratio
    words = text.split()
    capitalized = sum(1 for w in words if w[0].isupper())
    if capitalized / len(words) < 0.4:
        return False

    return True


def guess_level(font_size, doc_stats):
    """Guess heading level based on font size compared to dominant sizes in doc."""
    if not doc_stats['size_ranges']:
        return None

    size_ranges = sorted(doc_stats['size_ranges'], reverse=True)
    
    if font_size >= size_ranges[0] * 0.95:
        return "H1"
    elif len(size_ranges) > 1 and font_size >= size_ranges[1] * 0.9:
        return "H2"
    elif len(size_ranges) > 2 and font_size >= size_ranges[2] * 0.85:
        return "H3"
    return None
