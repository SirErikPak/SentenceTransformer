from langchain_community.document_loaders import WebBaseLoader
import re
import textwrap
import os


# Step 1: Load the webpage
url = "https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-november-4-2025/"
loader = WebBaseLoader(url)
docs = loader.load()

# Step 2: Extract raw text
raw_text = docs[0].page_content

# Step 3: Clean the text
def clean_text(text):
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+|https\S+", "", text)

    # Remove [number] citations
    text = re.sub(r"\[\d+\]", "", text)

    # Remove everything after "WARNING:" (case-insensitive, greedy match)
    text = re.split(r"\bWARNING\b[:\s]*", text, flags=re.IGNORECASE)[0]

    # Remove extra whitespace
    text = re.sub(r"\s{2,}", " ", text).strip()

    return text

cleaned_text = clean_text(raw_text)
cleaned_text = textwrap.fill(cleaned_text, width=180)
print(cleaned_text)

