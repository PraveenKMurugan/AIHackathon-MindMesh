pages = fetch_confluence_pages(CONFLUENCE_SPACE_KEY)

all_chunks = []
all_embeddings = []
all_metadata = []

for page in pages:
    print("Processing:", page["title"])

    text = clean_html(page["html"])
    if not text:
        continue

    chunks = chunk_text(text)

    metadata_list = [{
        "page_id": page["id"],
        "title": page["title"],
        "version": page["version"],
        "url": f"{CONFLUENCE_BASE_URL}/pages/{page['id']}",
    } for _ in chunks]

    embeddings = embed_texts(chunks)

    store_embeddings(chunks, embeddings, metadata_list)
