"""Part 5 (step B): answer a question from Heba's documents and cite the sources (search -> prompt -> LLM)."""
from datetime import date

from langchain_core.prompts import PromptTemplate

from llm import load_llm
from vector_store import load_vector_store, search, source_label

# Built on the mentor's template, plus rules for citing sources and for not inventing facts
PROMPT = PromptTemplate.from_template(
    """You are an assistant that answers questions about Heba Qasem's professional profile.
Today's date is {today}. Use it to know if a date in the context is in the past or in the future.
Answer the question using ONLY the context below. Do not use any outside knowledge.
Each part of the context starts with its source in square brackets, for example [CV_ML.pdf (page 1)].
After every fact in your answer, write its source in square brackets, exactly as it appears in the context.
If two sources give different information (for example different numbers), mention both, each with its source.
If the context does not contain the answer, reply only: "I don't know based on the provided documents."
Answer in the same language as the question, in 150 words or fewer.

## Context:
{context}

## Question:
{question}"""
)


def build_context(results):
    """Put the found chunks in one text; each chunk starts with its source, e.g. [Profile.pdf (page 2)]."""
    parts = []
    for chunk, score in results:
        parts.append(f"[{source_label(chunk.metadata)}]\n{chunk.page_content}")
    return "\n\n---\n\n".join(parts)


def answer_question(question):
    """Search the chunks, build the prompt, ask the LLM. Returns the answer, the model name and the chunks used."""
    results = search(load_vector_store(), question)
    prompt = PROMPT.format(today=date.today().strftime("%B %Y"), context=build_context(results), question=question)
    response = load_llm().invoke(prompt)
    return {
        "answer": response.content,
        "model": response.response_metadata.get("model_name"),
        "chunks": [(source_label(chunk.metadata), chunk.page_content) for chunk, score in results],
    }


if __name__ == "__main__":
    questions = [
        "What degree does Heba have?",
        "Which backend technologies does Heba know?",
        "Tell me about the dental clinic project",
        "How many problems did Heba solve on LeetCode?",
        "What is Heba's favorite food?",   # not in the documents: the right answer is "I don't know"
    ]
    for question in questions:
        result = answer_question(question)
        searched_in = []
        for label, text in result["chunks"]:
            if label not in searched_in:
                searched_in.append(label)
        print("\n" + "=" * 60)
        print("Question:", question)
        print(f"Answer ({result['model']}):")
        print(result["answer"])
        print("Searched in:", ", ".join(searched_in))
