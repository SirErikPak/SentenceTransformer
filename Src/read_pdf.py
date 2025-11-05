import fitz # PyMuPDF
import re
import sys

def get_text_from_pdf(pdf_path):
    """
    Extracts text from a local PDF file, starting after the Abstract/Metadata 
    and stopping immediately before the References or Bibliography section.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF '{pdf_path}': {e}", file=sys.stderr)
        return None
        
    print(f"Reading full text from '{pdf_path}'...")
    # More efficient string concatenation
    text = "".join(page.get_text() for page in doc)
    doc.close()
    
    if not text:
        return ""
    
    # --- 1. DEFINE START AND END PATTERNS ---
    # Start pattern: Finds "1. Introduction", "I. Introduction", or just "Introduction"
    START_PATTERN = r"(\n\s*1\.\s+)|(\n\s*I\.\s+)|(\n\s*Introduction)"
    
    # NEW End pattern: Only stops at References or Bibliography
    END_PATTERN = r"(\n\s*References)|(\n\s*Bibliography)"
    
    # --- 2. FIND START POSITION (Skip Abstract/Metadata) ---
    start_pos = 0
    start_match = re.search(START_PATTERN, text, re.IGNORECASE)
    
    if start_match:
        start_pos = start_match.start()
        print(f"Extraction start found at: '{start_match.group(0).strip()}'")
    else:
        # Fallback: Search for the header 'Abstract' and start after it.
        abstract_match = re.search(r"(\n\s*Abstract\s*\n)", text, re.IGNORECASE)
        if abstract_match:
            start_pos = abstract_match.end()
            print("Warning: Section 1 not found. Starting after 'Abstract' section (Fallback).")
        else:
            print("Warning: Start of core content could not be reliably determined. Starting from beginning.")
            
    core_text = text[start_pos:]
    
    # --- 3. FIND END POSITION (Stop before References) ---
    end_pos = len(core_text)
    
    # Search for the end pattern within the core content
    end_match = re.search(END_PATTERN, core_text, re.IGNORECASE)

    if end_match:
        end_pos = end_match.start()
        print(f"Extraction stop found immediately before: '{end_match.group(0).strip()}'")
    else:
        print("Warning: No terminal section (References/Bibliography) found. Extracting until EOF.")

    # --- 4. SLICE AND RETURN ---
    final_text = core_text[:end_pos].strip()
    
    print(f"Successfully extracted {len(final_text)} characters of core content.")
    return final_text