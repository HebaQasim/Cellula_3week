# Task 1 — Personal RAG Assistant: "Ask About Heba Qasem"

A Streamlit app that answers questions about my professional profile (CVs, LinkedIn profile, certifications and
GitHub projects). The answers come **only** from these documents, and every fact in an answer is followed by its
source, for example `[CV_ML.pdf (page 1)]`. Built with **LangChain**, **FAISS** and **Google Gemini**.

**Live app:** [https://heba-career-chat-i7x5cvry3rcyuob8q7uf7k.streamlit.app/](https://heba-career-chat-i7x5cvry3rcyuob8q7uf7k.streamlit.app/)

## How it works

```text
                 ┌──────────── built once, saved in faiss_index/ ────────────┐
data/ files ──►  load (PDF / TXT / MD) ──► chunk (800 chars) ──► embeddings ──► FAISS index

question ──► embedding ──► FAISS: 6 closest chunks ──► prompt (chunks + sources + rules) ──► Gemini ──► answer with [sources]
```

1. **Load** — every file becomes a LangChain `Document` (text + metadata). A PDF gives one Document per page.
   The metadata keeps the file name (`source`), the folder (`type`) and, for PDFs, the page number.
2. **Chunk** — `RecursiveCharacterTextSplitter` cuts each Document into chunks of at most 800 characters
   (about 200 tokens) with up to 100 characters of overlap. It cuts between paragraphs first, then between lines,
   then between words, so sentences are not broken in the middle. Each chunk keeps the metadata of its Document.
3. **Embed** — `sentence-transformers/all-MiniLM-L6-v2` turns each chunk into a vector of 384 numbers.
   It reads at most 256 tokens per chunk, which is why the chunks are small.
4. **Store** — the 76 vectors and their chunks are stored in a **FAISS** index and saved on disk (`faiss_index/`),
   so the app does not recompute them at every start.
5. **Search** — the question is embedded with the same model and FAISS returns the **6 closest chunks**.
6. **Answer** — the chunks are put in a prompt, each one under its source label, and sent to Gemini.

## Data sources

| Folder | Files | Where they come from |
|---|---|---|
| `data/cvs/` | `CV_Graduation.pdf`, `CV_Internships.pdf`, `CV_ML.pdf`, `CV_UI_UX.pdf` | My four CV versions |
| `data/linkedin/` | `Profile.pdf` (2 pages) | LinkedIn → *Save to PDF* |
| `data/extra/` | `certifications.txt`, `contact.txt` | Written by hand: a certification that is on LinkedIn but not in the PDF, and the primary email (the CVs and LinkedIn show two different emails) |
| `data/github/` | 8 `.md` files, one per repository | Downloaded by `fetch_github.py`: a short header (name, link, description, language) + the README |

In total: **16 Documents → 76 chunks**.

## Files

| File | Step | Purpose |
|---|---|---|
| `fetch_github.py` | Data | Downloads the README of every public repository of `HebaQasim` into `data/github/` |
| `load_documents.py` | 1 | `load_local_documents()`: reads all files with `PyPDFLoader` / `TextLoader` |
| `chunk_documents.py` | 2 | `chunk_documents()`: `RecursiveCharacterTextSplitter` (800 / 100) |
| `embeddings.py` | 3 | `load_embeddings()`: the `all-MiniLM-L6-v2` model through `HuggingFaceEmbeddings` |
| `vector_store.py` | 4–5 | Builds, saves and loads the FAISS index; `search()` returns the 6 closest chunks |
| `llm.py` | 6 | `load_llm()`: Gemini through `ChatOpenAI`, with two backup models |
| `rag.py` | 6 | `answer_question()`: search → prompt → LLM → answer, model name and chunks |
| `app.py` | UI | The Streamlit app |
| `.env.example` | — | Shows the name of the API key to put in a `.env` file |
| `requirements.txt` | — | Python packages and versions |

Every step can be run on its own to see its result, for example `python chunk_documents.py` prints the number
of chunks per file and two neighbouring chunks, and `python rag.py` answers five test questions.

## Design choices

**LangChain.** The pipeline uses LangChain components at every step: document loaders, a text splitter,
`HuggingFaceEmbeddings`, the `FAISS` vector store, `PromptTemplate` and `ChatOpenAI`.

**Search: plain similarity search, 6 chunks.** The four CVs start with the same header (name, contact, education),
so the same information often appears in several of the closest chunks. I also tried **MMR search**
(`max_marginal_relevance_search`), which picks chunks that are close to the question *and* different from each other.
It removed the repeated chunks, but it also brought unrelated chunks and dropped a relevant one (for the dental
clinic question it lost the CV chunk listing the project's features). Losing the chunk that holds the answer is worse than
repeating information, so I kept similarity search and raised the number of chunks from 4 to 6.

**Prompt.** Based on the template from the session demo, with extra rules:

- answer **only** from the context, no outside knowledge (to reduce hallucinations);
- write the **source** after every fact, exactly as it appears above the chunk;
- if two sources disagree (for example different numbers), mention both, each with its source;
- if the answer is not in the context, reply only *"I don't know based on the provided documents."*;
- answer in the language of the question, in 150 words or fewer;
- **today's date** is given, because the model does not know it: without it, the model described a degree
  finished in June 2025 as "expected".

**LLM: Gemini through `ChatOpenAI`.** The Gemini API accepts the same request format as OpenAI, so `ChatOpenAI`
works with it by changing `base_url` only. Settings:

- `gemini-3.5-flash` first, then `gemini-3.1-flash-lite` and `gemini-3.5-flash-lite` as backups (`with_fallbacks`):
  free models are sometimes busy (error 503), and the app should still answer;
- no `temperature`: Google recommends keeping the default (1.0) for Gemini 3 models — the rules in the prompt
  keep the model on the documents;
- `reasoning_effort="low"`: the answer is in the chunks, so little reasoning is needed and the reply is faster;
- `timeout=30`: a model that does not answer within 30 seconds is skipped.

## Example results

From `python rag.py`:

| Question | Answer (summary) |
|---|---|
| What degree does Heba have? | B.Sc of Computer Systems Engineering, PTUK — cited from the CVs |
| Which backend technologies does Heba know? | Java, Spring Boot, REST APIs, JWT, MySQL, Hibernate, Maven, C#, ASP.NET Core, Swagger… — from three different files |
| Tell me about the dental clinic project | Graduation project: backend for patient records, appointments, treatments, a dental map per tooth; C# |
| How many problems did Heba solve on LeetCode? | The CVs give different numbers, so the answer lists each number with its CV |
| What is Heba's favorite food? | *"I don't know based on the provided documents."* (not in the documents) |

## Setup and run (Windows)

Requires **Python 3.13**.

```bat
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

1. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com) (*Get API key*).
2. Copy `.env.example` to a new file named `.env` and put the key in it: `GEMINI_API_KEY=...`
3. Start the app:

```bat
streamlit run app.py
```

The first start downloads the embedding model (about 90 MB) and builds the FAISS index; later starts are fast.
After changing any file in `data/`, rebuild the index with `python vector_store.py`.
To refresh the GitHub READMEs, run `python fetch_github.py` first.

## Deployment (Streamlit Community Cloud)

The app is deployed for free on **Streamlit Community Cloud**: [https://heba-career-chat-i7x5cvry3rcyuob8q7uf7k.streamlit.app/](https://heba-career-chat-i7x5cvry3rcyuob8q7uf7k.streamlit.app/)

- **Main file path:** `Task1_RAG/app.py` (the app is inside a folder of the repository)
- **Python version:** 3.13, the same as local development
- **API key:** saved in the app's **Secrets** settings, in TOML format: `GEMINI_API_KEY = "..."`.
  Streamlit makes it available as an environment variable, so `llm.py` reads it with `os.getenv` exactly like
  the `.env` file on my computer. The key is never written in the code or uploaded to GitHub.
- **FAISS index:** `faiss_index/` is not in the repository (`.gitignore`), so on the first start the app builds it
  from the `data/` folder. No code change was needed for the deployment.
- After a `git push`, Streamlit updates the app with the new code.

## Notes and limitations

- **Ask in English for the best results.** `all-MiniLM-L6-v2` is an English model: a question in Arabic is
  answered in Arabic, but the search finds less relevant chunks, so the answer can be incomplete.
- **Free LLM models can be busy.** If all three Gemini models fail, the app shows a message asking to try again.
- **The answer can only use the chunks that were found.** If a fact is in a chunk that is not among the 6 closest,
  it will be missing from the answer (for example one of the LeetCode numbers).
- **Snapshot of the data.** The documents are a copy from the day they were collected; the app does not read
  LinkedIn or GitHub live.
- `langchain-community` prints a deprecation warning when it is imported; the document loaders and FAISS still work.
