import os

def load_and_clean_documents(docs_dir):
    documents = {}
    if not os.path.exists(docs_dir):
        print(f"Error: Folder '{docs_dir}' not found. Please create it and add your .txt files.")
        return documents
    
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(docs_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                # Clean up empty lines and excess spaces
                cleaned_lines = [line.strip() for line in text.split("\n") if line.strip()]
                cleaned_text = "\n".join(cleaned_lines)
                documents[filename] = cleaned_text
    return documents

def chunk_text(text, chunk_size=600, overlap=150):
    chunks = []
    if len(text) <= chunk_size:
        return [text]
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk:
            chunks.append(chunk)
        # Sliding window step
        start += (chunk_size - overlap)
    return chunks

def run_pipeline():
    docs_dir = "documents"
    raw_docs = load_and_clean_documents(docs_dir)
    all_chunks = []
    
    for filename, text in raw_docs.items():
        doc_chunks = chunk_text(text)
        for i, chunk in enumerate(doc_chunks):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "source": filename,
                    "chunk_index": i
                }
            })
            
    print(f"=== PIPELINE STATS ===")
    print(f"Total documents loaded: {len(raw_docs)}")
    print(f"Total chunks created: {len(all_chunks)}")
    
    # Print sample chunks for inspection requirement
    print("\n=== SAMPLE CHUNKS INSPECTION ===")
    sample_indices = [0, min(5, len(all_chunks)-1), min(12, len(all_chunks)-1), min(20, len(all_chunks)-1), len(all_chunks)-1]
    unique_samples = sorted(list(set(sample_indices)))
    
    for idx in unique_samples[:5]:
        c = all_chunks[idx]
        print(f"\n[Source File: {c['metadata']['source']} | Chunk: {c['metadata']['chunk_index']}]")
        print("-" * 50)
        print(c['text'])
        print("-" * 50)

if __name__ == "__main__":
    run_pipeline()