import fitz # PyMuPDF
import re
import sys

# --- 1. PDF EXTRACTION FUNCTION ---
def get_text_from_pdf(pdf_path):
    """
    Extracts text from a local PDF file, starting after the Abstract/Metadata, 
    stopping before "References", and cleaning up citation noise and URLs.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF '{pdf_path}': {e}", file=sys.stderr)
        return None
        
    print(f"Reading full text from '{pdf_path}'...")
    text = "".join(page.get_text() for page in doc)
    doc.close()
    
    if not text:
        return ""

    # --- FIND THE START (Skip Abstract wording) ---
    start_pos = 0
    abstract_pattern = r'\babstract\b'
    abstract_match = re.search(abstract_pattern, text, re.IGNORECASE)
    
    if abstract_match:
        start_pos = abstract_match.end()
    else:
        print("Warning: 'Abstract' marker not found. Starting extraction from beginning.")
        
    core_text = text[start_pos:]
    
    # --- FIND THE END (Stop before "References") ---
    end_pos = len(core_text)
    references_pattern = r'\breferences\b'
    end_match = re.search(references_pattern, core_text, re.IGNORECASE)

    if end_match:
        end_pos = end_match.start()
        print(f"Extraction stop found immediately before: '{end_match.group(0)}'")
    else:
        print("Warning: 'References' section not found. Extracting until EOF.")

    final_text = core_text[:end_pos]
    
    
    # --- CLEANUP (Remove Citations, Links, and Fix Hyphenation) ---
    # 1. Patterns for Citation and Link Removal (Your existing good patterns)
    pattern_et_al = r'\s*\([^()]*et al\.[^()]*\)' 
    pattern_raw_url = r'https?:\/\/[^\s\)]+'
    pattern_markdown_link = r'\[https?:[^\]]*\]\([^\)]*\)' 
    combined_pattern_noise = f'({pattern_et_al})|({pattern_raw_url})|({pattern_markdown_link})'

    cleaned_text = re.sub(combined_pattern_noise, '', final_text)

    # 2. Target Hyphenation Artifacts (e.g., 'popu-larity' -> 'popularity')
    # Finds a letter, followed by a hyphen, followed optionally by spaces, followed by a letter.
    # Replaces it with the two letters joined (e.g., a-b becomes ab).
    pattern_broken_word = r'([a-zA-Z])-\s*([a-zA-Z])'
    cleaned_text = re.sub(pattern_broken_word, r'\1\2', cleaned_text)

    # 3. Final Whitespace Cleanup
    # This removes excess newlines/spaces (and any remaining hyphenation artifacts that had a space)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    print(f"Successfully extracted and cleaned {len(cleaned_text)} characters.")
    return cleaned_text