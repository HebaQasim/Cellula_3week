"""Part 3: turn text into vectors (embeddings) with a Hugging Face model through LangChain."""
from functools import lru_cache

import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

from chunk_documents import chunk_documents
from load_documents import load_local_documents

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def load_embeddings():
    """Load the embedding model the first time; later calls reuse it (downloaded only once)."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={"device": "cpu"})


def similarity(vector_a, vector_b):
    """Cosine similarity: close to 1 = very close meaning, close to 0 = unrelated meaning."""
    return float(np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))


if __name__ == "__main__":
    embeddings = load_embeddings()

    # 1) One text becomes one vector (a list of numbers)
    vector = embeddings.embed_query("Heba studied Computer Systems Engineering")
    print("Numbers in one vector:", len(vector))
    print("First 5 numbers:", [round(number, 4) for number in vector[:5]])

    # 2) A question and three sentences: the closest meaning gets the highest similarity
    question = "What degree does Heba have?"
    sentences = [
        "B.Sc of Computer Systems Engineering, Palestine Technical University - Kadoorie",
        "Tawjihi (Scientific Stream), Jalqamous Secondary School",
        "Dental Clinic Management API: endpoints for doctors and treatments",
    ]
    question_vector = embeddings.embed_query(question)
    sentence_vectors = embeddings.embed_documents(sentences)
    print("\nQuestion:", question)
    for sentence, sentence_vector in zip(sentences, sentence_vectors):
        print(f"  similarity {similarity(question_vector, sentence_vector):.3f}  ->  {sentence}")

    # 3) All the chunks of the project become vectors
    chunks = chunk_documents(load_local_documents())
    chunk_vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])
    print("\nChunks:", len(chunks), "-> vectors:", len(chunk_vectors), "| numbers in each vector:", len(chunk_vectors[0]))
