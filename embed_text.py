from sentence_transformers import SentenceTransformer

# Small, fast, high-accuracy model for documentation search
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")
embed_model = SentenceTransformer(EMBED_MODEL_NAME)
print("Model loaded!")

def embed_texts(text_list):
    vectors = embed_model.encode(
        text_list,
        batch_size=16,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return vectors


def embed_text(text: str):
    return embed_model.encode(text, convert_to_numpy=True)
