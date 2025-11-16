def extract_text_from_adf(adf):
    if not isinstance(adf, dict):
        return ""

    result = []

    def walk(node):
        if node.get("type") == "text":
            result.append(node.get("text", ""))

        for child in node.get("content", []):
            walk(child)

    walk(adf)
    return "\n".join(result)

def process_issue(issue):
    key = issue["key"]
    fields = issue["fields"]

    summary = fields.get("summary", "")
    description_adf = fields.get("description")
    description = extract_text_from_adf(description_adf)

    combined_text = f"{summary}\n\n{description}"

    return {
        "jira_key": key,
        "summary": summary,
        "clean_text": combined_text,
        "url": f"{JIRA_BASE_URL}/browse/{key}"
    }
