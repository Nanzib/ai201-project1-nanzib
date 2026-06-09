import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
import gradio as gr
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key or "your_key_here" in api_key:
    print("❌ ERROR: Please add your actual Groq API key to your .env file.")

# Initialize ChromaDB and Embedding Model from Milestone 4
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="unofficial_guide")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Groq Client
groq_client = Groq(api_key=api_key)

def ask(question):
    # Retrieve the top 4 chunks from the vector store
    query_embedding = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=4
    )
    
    retrieved_chunks = results['documents'][0]
    metadatas = results['metadatas'][0]
    
    # Build the context block and track unique source files programmatically
    context_blocks = []
    sources = set()
    for text, meta in zip(retrieved_chunks, metadatas):
        sources.add(meta['source'])
        context_blocks.append(f"Source Document: {meta['source']}\nContent: {text}")
        
    context_str = "\n\n".join(context_blocks)
    
    # Create a strict grounding prompt system
    system_prompt = (
        "You are an assistant for 'The Unofficial Guide'. "
        "Answer the user's question using ONLY the provided text blocks as context. "
        "Do not use external or general knowledge. "
        "If the answer cannot be explicitly found in the text blocks below, reply exactly with: "
        "'I don't have enough information on that.' "
        "Keep your answer direct, objective, and accurate to the text."
    )
    
    user_prompt = f"Context:\n{context_str}\n\nQuestion: {question}"
    
    # Request the grounded response from Groq
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"Error communicating with the LLM API: {str(e)}"
        
    return {
        "answer": answer,
        "sources": sorted(list(sources))
    }

# Gradio Interface Helper Function
def handle_query(question):
    result = ask(question)
    sources_text = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources_text

# Construct Web Interface UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎓 The Unofficial Guide: Hunter CS Edition")
    
    inp = gr.Textbox(label="Your Question", placeholder="Ask something about Hunter College CS professors...", lines=2)
    btn = gr.Button("Ask System")
    
    answer = gr.Textbox(label="Answer", lines=8, interactive=False)
    sources = gr.Textbox(label="Retrieved from", lines=4, interactive=False)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()