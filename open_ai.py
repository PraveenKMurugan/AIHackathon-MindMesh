import openai

def answer_query(user_query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    You are a helpful internal assistant. Use the context below to answer.

    CONTEXT:
    {context}

    QUESTION:
    {user_query}

    Answer strictly from the context. If not found, say "No relevant info found."
    """

    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


import openai

openai.api_key = "YOUR_KEY"

def call_openai(prompt):
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
