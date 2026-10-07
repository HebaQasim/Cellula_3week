"""Part 1: read the local files (CVs, LinkedIn profile, extra notes, GitHub READMEs) as LangChain Documents."""
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def load_local_documents():
    """Read every file in data/cvs, data/linkedin, data/extra and data/github.

    Each result is a LangChain Document: the text is in page_content, and the
    file name (source) and the folder it came from (type) are in metadata.
    A PDF gives one Document per page (metadata["page"] starts from 0).
    """
    documents = []
    for folder_name in ["cvs", "linkedin", "extra", "github"]:
        folder = DATA_DIR / folder_name
        for path in sorted(folder.glob("*")):
            if path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(path))
            elif path.suffix.lower() in [".txt", ".md"]:
                loader = TextLoader(str(path), encoding="utf-8")
            else:
                continue  # skip any other kind of file

            for document in loader.load():
                document.metadata["source"] = path.name   # short name instead of the full path
                document.metadata["type"] = folder_name
                documents.append(document)
    return documents


if __name__ == "__main__":
    documents = load_local_documents()
    print("Documents found:", len(documents))
    for document in documents:
        source = document.metadata["source"]
        if "page" in document.metadata:
            source += f" (page {document.metadata['page'] + 1})"
        print("\n" + "=" * 60)
        print("Source:", source, "| Type:", document.metadata["type"],
              "| Characters:", len(document.page_content))
        print(document.page_content[:300])
