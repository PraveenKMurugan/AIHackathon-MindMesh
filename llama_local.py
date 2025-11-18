import requests
import json

def answer_query_llama_local(user_query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    You are a helpful internal assistant. Use the context below to answer.

    CONTEXT:
    {context}

    QUESTION:
    {user_query}

    Answer strictly from the context. If not found, say "No relevant info found."
    """

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    return response.json()["message"]["content"]


import requests
import json

def call_llama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1", "prompt": prompt}
    )
    text = ""
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():
            obj = json.loads(line)
            text += obj.get("response", "")
    return text
