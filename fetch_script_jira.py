def run_jira_ingestion(project_key):
    issues = fetch_all_jira_issues(project_key)

    for issue in issues:
        doc = process_issue(issue)

        if not doc["text"].strip():
            print("Skipping empty:", doc["id"])
            continue

        store_in_chroma(doc)
        print("Stored embeddings for:", doc["id"])
