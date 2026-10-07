"""Part 4: keep the chunk vectors in a FAISS vector database, save it on disk, and search it."""
from pathlib import Path

from langchain_community.vectorstores import FAISS

from chunk_documents import chunk_documents
from embeddings import load_embeddings
from load_documents import load_local_documents

BASE_DIR = Path(__file__).parent
INDEX_DIR = BASE_DIR / "faiss_index"

SEARCH_K = 6    # how many chunks we take for one question


def build_vector_store():
    """Read, chunk and embed all the documents, then save the FAISS index in the faiss_index folder."""
    chunks = chunk_documents(load_local_documents())
    vector_store = FAISS.from_documents(chunks, load_embeddings())
    vector_store.save_local(str(INDEX_DIR))
    return vector_store


def load_vector_store():
    """Load the saved index from disk. If it was never built, build it first."""
    if not INDEX_DIR.exists():
        return build_vector_store()
    # The index files were made by us (build_vector_store), so it is safe to open them
    return FAISS.load_local(str(INDEX_DIR), load_embeddings(), allow_dangerous_deserialization=True)


def search(vector_store, question):
    """Return the SEARCH_K chunks closest to the question, each with its score (smaller = closer).

    We also tried MMR search (max_marginal_relevance_search): it removed the repeated CV chunks,
    but it also brought unrelated chunks and dropped some relevant ones, so we kept this simple search.
    """
    return vector_store.similarity_search_with_score(question, k=SEARCH_K)


def source_label(metadata):
    """A short name for the place a chunk came from, e.g. 'Profile.pdf (page 2)' or 'contact.txt'."""
    label = metadata["source"]
    if "page" in metadata:
        label += f" (page {metadata['page'] + 1})"
    return label


if __name__ == "__main__":
    # Running this file always rebuilds the index, so any change in the data folder is included
    vector_store = build_vector_store()
    print("Vectors saved in the index:", vector_store.index.ntotal)
    print("Index folder:", INDEX_DIR)

    questions = [
        "What degree does Heba have?",
        "Which backend technologies does Heba know?",
        "Tell me about the dental clinic project",
    ]
    for question in questions:
        print("\n" + "=" * 60)
        print("Question:", question)
        for chunk, score in search(vector_store, question):
            preview = " ".join(chunk.page_content.split())[:80]
            print(f"  score {score:.3f} | {source_label(chunk.metadata)} | {preview}")
