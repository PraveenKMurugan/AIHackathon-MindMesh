import requests
import json
from config import (
    CONFLUENCE_BASE_URL,
    CONFLUENCE_EMAIL,
    CONFLUENCE_API_TOKEN
)

def fetch_pages(space_key, limit=50):
    """
    Fetch all Confluence pages for a space, handling pagination.
    Returns a list of dicts with page metadata + HTML content.
    """
    pages = []
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content"

    params = {
        "spaceKey": space_key,
        "type": "page",
        "expand": "body.storage,version",
        "limit": limit
    }

    print(f"Fetching pages from Confluence space: {space_key}")

    while True:
        response = requests.get(
            url,
            params=params,
            auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)
        )

        if response.status_code != 200:
            print("Error fetching pages:", response.text)
            break

        data = response.json()

        for page in data.get("results", []):
            pages.append({
                "source": "confluence",
                "id": page["id"],
                "title": page["title"],
                "version": page["version"]["number"],
                "lastUpdated": page["version"]["when"],
                "html": page["body"]["storage"]["value"],
                "url": f"{CONFLUENCE_BASE_URL}/pages/{page['id']}"
            })

        # Pagination
        next_link = data.get("_links", {}).get("next")
        if not next_link:
            break

        # Important: next uses relative URL
        url = CONFLUENCE_BASE_URL + next_link
        params = None  # next link already contains parameters

    print(f"Fetched {len(pages)} pages.")
    return pages


# if __name__ == "__main__":
#     space_key = "PROD"   # change your space key here
#     pages = fetch_pages(space_key)

#     # Optional: Save raw output for debugging
#     with open("confluence_pages.json", "w", encoding="utf-8") as f:
#         json.dump(pages, f, indent=2, ensure_ascii=False)

#     print("Saved to confluence_pages.json")
