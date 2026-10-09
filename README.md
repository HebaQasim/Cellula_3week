# Cellula Internship — Week 3

## Task 0 — BigBird Research

Folder: [`Task0_BigBird`](Task0_BigBird)

A research report about the BigBird Transformer model ([BigBird_Research.pdf](Task0_BigBird/BigBird_Research.pdf)).
It explains why standard self-attention has quadratic cost, how BigBird's sparse attention (window, global and
random attention, implemented in blocks of 64 tokens) makes it linear, and compares its complexity with BERT and
Longformer. It also covers applications for long documents, performance characteristics, advantages and limitations.

## Task 1 — Personal RAG Assistant

Folder: [`Task1_RAG`](Task1_RAG)

**Live app:** [https://heba-career-chat-i7x5cvry3rcyuob8q7uf7k.streamlit.app/](https://heba-career-chat-i7x5cvry3rcyuob8q7uf7k.streamlit.app/)

A Streamlit app that answers questions about my professional profile using Retrieval-Augmented Generation (RAG).
My CVs, LinkedIn profile, certifications and GitHub READMEs are split into chunks, embedded with
`all-MiniLM-L6-v2` and stored in a FAISS index. For each question, the closest chunks are sent to Google Gemini,
which answers **only** from them and writes the source after every fact. Built with LangChain.

Setup and usage instructions are in the app's [README](Task1_RAG/README.md).

## Repository structure

```text
Cellula_3week/
├── Task0_BigBird/
│   └── BigBird_Research.pdf
└── Task1_RAG/
    ├── data/
    │   ├── cvs/          (4 CV PDFs)
    │   ├── linkedin/     (Profile.pdf)
    │   ├── extra/        (certifications.txt, contact.txt)
    │   └── github/       (one README per repository)
    ├── fetch_github.py
    ├── load_documents.py
    ├── chunk_documents.py
    ├── embeddings.py
    ├── vector_store.py
    ├── llm.py
    ├── rag.py
    ├── app.py
    ├── .env.example
    ├── .gitignore
    ├── requirements.txt
    └── README.md
```
