import requests
import json
from config import (
    JIRA_API_TOKEN,
    JIRA_BASE_URL,
    JIRA_EMAIL
)

session = requests.Session()
session.auth = (JIRA_EMAIL, JIRA_API_TOKEN)
session.headers.update({"Accept": "application/json"})


def fetch_all_jira_issues(project_key):
    base_url = f"{JIRA_BASE_URL}/rest/api/3/search"
    
    start = 0
    max_results = 100
    all_issues = []

    while True:
        params = {
            "jql": f"project = {project_key}",
            "startAt": start,
            "maxResults": max_results
        }

        response = session.get(base_url, params=params)
        data = response.json()

        issues = data.get("issues", [])
        all_issues.extend(issues)

        print(f"Fetched {len(issues)} issues...")

        if len(issues) < max_results:
            break  

        start += max_results

    return all_issues
