import re
from bs4 import BeautifulSoup
import html

def clean_html(html_content: str) -> str:
    """Clean HTML from Confluence into readable plain text."""
    
    if not html_content:
        return ""

    # 1. BeautifulSoup parsing
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    # 2. Convert headings into readable text
    for h in soup.find_all(["h1", "h2", "h3", "h4"]):
        h.insert_before("\n\n" + ("#" * int(h.name[1])) + " ")

    # 3. Convert lists into bullet points
    for li in soup.find_all("li"):
        li.insert_before("\n• ")

    # 4. Extract raw text
    text = soup.get_text(separator="\n")

    # 5. Decode HTML entities (&nbsp; → space)
    text = html.unescape(text)

    # 6. Remove leftover URLs
    text = re.sub(r"http\S+", "", text)

    # 7. Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # 8. Trim ends
    text = text.strip()

    return text


def clean_pages(pages):
    """Clean list of Confluence pages returned from API."""
    cleaned = []

    for p in pages:
        clean_text, links = clean_html(p[html])
        cleaned.append({
            "pageId": p["pageId"],
            "title": p["title"],
            "version": p["version"],
            "lastUpdated": p["lastUpdated"],
            "url": p["url"],
            "text": clean_text,
            "links": links
        })

    return cleaned
