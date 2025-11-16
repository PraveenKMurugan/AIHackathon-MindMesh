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
