import re
from typing import List, Dict

def split_into_sections(text: str):
    """
    Splits by headings (##, ###, or Confluence-style titles)
    """
    # Match typical headings: H1/H2, numbered headings, bold headings, etc.
    pattern = r"(?=^#+\s|^\d+\.\d*\s|^[-_]{3,}$)"
    parts = re.split(pattern, text, flags=re.MULTILINE)
    return [p.strip() for p in parts if p.strip()]


def chunk_text(text: str, max_chars: int = 2000, overlap: int = 200):
    """
    Splits text into chunks with overlap.
    """
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + max_chars, length)
        chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap  # keep overlap for context

    return chunks


def chunk_document(cleaned_text: str, page_id: str, page_title: str) -> List[Dict]:
    """
    Full chunking pipeline:
    1) Split into sections
    2) Chunk each section further
    3) Attach metadata
    """
    sections = split_into_sections(cleaned_text)
    final_chunks = []
    chunk_index = 0

    for section in sections:
        section_chunks = chunk_text(section)

        for chunk in section_chunks:
            final_chunks.append({
                "page_id": page_id,
                "title": page_title,
                "chunk_index": chunk_index,
                "content": chunk
            })
            chunk_index += 1

    return final_chunks
