import os
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_and_clean_documents, chunk_text

def build_vector_store():
    # Load and chunk documents
    raw_docs = load_and_clean_documents("documents")
    
    # Initialize Local ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Reset collection if it exists to prevent duplication
    try:
        chroma_client.delete_collection(name="unofficial_guide")
    except:
        pass
        
    collection = chroma_client.create_collection(name="unofficial_guide")
    
    # Load Local Embedding Model
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Prepare data arrays
    ids = []
    documents = []
    metadatas = []
    embeddings = []
    
    global_id = 0
    for filename, text in raw_docs.items():
        doc_chunks = chunk_text(text)
        for i, chunk in enumerate(doc_chunks):
            # Generate vectors
            embedding = model.encode(chunk).tolist()
            
            ids.append(f"id_{global_id}")
            documents.append(chunk)
            metadatas.append({"source": filename, "chunk_index": i})
            embeddings.append(embedding)
            global_id += 1
            
    # Load into ChromaDB
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )
    print(f"Successfully embedded and stored {len(documents)} chunks in ChromaDB!")
    return collection, model

def query_vector_store(query_text, collection, model, k=4):
    query_embedding = model.encode(query_text).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    print(f"\n🔍 Query: '{query_text}'")
    print("=" * 60)
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        dist = results['distances'][0][i]
        print(f"Result #{i+1} [Source: {meta['source']}] (Distance: {dist:.4f})")
        print(f"Content: {doc[:200]}...")
        print("-" * 60)

if __name__ == "__main__":
    # Build database and run tests
    collection, model = build_vector_store()
    
    # Test evaluation questions
    query_vector_store("How much of the final grade do pop quizzes account for in Eric Schweitzer's CS265 class?", collection, model)
    query_vector_store("Does Professor Shankar post his handwritten lecture notes?", collection, model)
    query_vector_store("What software tool must students teach themselves to use for the CSCI49383 VR development class projects?", collection, model)