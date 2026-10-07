"""Part 2: split every Document into small overlapping chunks with LangChain (the metadata is kept)."""
from langchain_text_splitters import RecursiveCharacterTextSplitter

from load_documents import load_local_documents

CHUNK_SIZE = 800      # the most characters in one chunk
CHUNK_OVERLAP = 100   # the most characters shared by two neighbouring chunks


def chunk_documents(documents):
    """Cut each Document into chunks; every chunk keeps the metadata (source, type, page) of its Document."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(documents)


if __name__ == "__main__":
    documents = load_local_documents()
    chunks = chunk_documents(documents)
    print("Documents:", len(documents), "-> Chunks:", len(chunks))
    print("Longest chunk:", max(len(chunk.page_content) for chunk in chunks), "characters")

    # How many chunks came from each file
    counts = {}
    for chunk in chunks:
        source = chunk.metadata["source"]
        counts[source] = counts.get(source, 0) + 1
    print("\nChunks per file:")
    for source, count in counts.items():
        print(f"  {source}: {count}")

    # Show the first two chunks of one README, to see the overlap between them
    show_file = "DentalClinicManagement.md"
    file_chunks = [chunk for chunk in chunks if chunk.metadata["source"] == show_file]
    for number, chunk in enumerate(file_chunks[:2], start=1):
        print("\n" + "=" * 60)
        print(f"{show_file} - chunk {number} | Characters: {len(chunk.page_content)}")
        print(chunk.page_content)
    print("\nMetadata of a chunk:", file_chunks[0].metadata)
