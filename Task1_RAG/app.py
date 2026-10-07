"""Part 6: Streamlit app - ask a question about Heba's professional profile and get an answer with its sources."""
import streamlit as st

st.set_page_config(page_title="Ask About Heba", page_icon="💼")

st.title("💼 Ask About Heba Qasem")
st.caption(
    "Answers come only from Heba's CVs, LinkedIn profile, certifications and GitHub READMEs. "
    "Every fact is followed by its source in [brackets]."
)

# ---------- Loading: each spinner appears only while something is really loading ----------
with st.spinner("Starting the app...", show_time=True):
    from llm import LLM_MODELS
    from rag import answer_question
    from vector_store import SEARCH_K, load_vector_store

with st.spinner("Loading the embedding model and the FAISS index...", show_time=True):
    load_vector_store()

with st.sidebar:
    st.header("About")
    st.write("**Sources:** 4 CVs, LinkedIn profile, certifications, contact info and 8 GitHub READMEs")
    st.write("**Embeddings:** all-MiniLM-L6-v2")
    st.write("**Vector database:** FAISS")
    st.write(f"**Chunks used for each answer:** {SEARCH_K}")
    st.write("**LLM:** Gemini (" + ", ".join(LLM_MODELS) + ")")
    st.header("Try asking")
    st.write("- What degree does Heba have?")
    st.write("- Which backend technologies does Heba know?")
    st.write("- Tell me about the dental clinic project")
    st.write("- How can I contact Heba?")

question = st.text_input("Your question", placeholder="e.g. What degree does Heba have?")

if st.button("Ask", type="primary"):
    if question.strip() == "":
        st.warning("Please write a question first.")
    else:
        try:
            with st.spinner("Searching the documents and writing the answer...", show_time=True):
                result = answer_question(question)
        except Exception as error:
            # All the free models were busy or did not answer in time
            st.error("The AI model did not answer right now. Please try again in a minute.", icon="⏳")
            st.caption(f"Details: {str(error)[:200]}")
        else:
            st.markdown(result["answer"])
            st.caption(f"Answered by {result['model']}")
            with st.expander(f"📄 The {len(result['chunks'])} chunks the answer was based on"):
                for label, text in result["chunks"]:
                    st.markdown(f"**{label}**")
                    st.text(text)
