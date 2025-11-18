def get_answer(user_query):
    # 1) Embed user query
    q_emb = embed_text(user_query)

    # 2) Retrieve chunks
    results = search_knowledge_base(q_emb)
    chunks = results["documents"][0]

    # 3) Ask the LLM
    answer = answer_query(user_query, chunks)

    #if local llama llm is used.
    # answer = answer_query_llama_local(user_query, chunks)  
    return answer


def retrieve_chunks(question, top_k=5):
    q_emb = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    return docs, metas


def build_context(docs, metas):
    context_blocks = []

    for doc, meta in zip(docs, metas):
        block = f"""
        Source: {meta.get('url', 'unknown')}
        Issue/Page: {meta.get('jira_key', meta.get('page_id', 'N/A'))}

        {doc}
        """
        context_blocks.append(block)

    return "\n\n---\n\n".join(context_blocks)


def answer_query(question, top_k=5, use="llama"):
    docs, metas = retrieve_chunks(question, top_k=top_k)

    if not docs:
        return "No relevant information found."

    context = build_context(docs, metas)

    prompt = f"""
    You are an assistant trained on Odessa internal knowledge. 
    Use ONLY the context below to answer the question.

    Context:
    {context}

    Question: {question}

    Answer clearly, accurately, and reference the source URLs when useful.
    """

    if use == "llama":
        return call_llama(prompt)
    else:
        return call_openai(prompt)
