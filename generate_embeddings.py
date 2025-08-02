import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# === Load .env ===
load_dotenv()

# === Configuration ===
KB_FOLDER = "../kb"  # 📁 Path to your knowledge base folder
MODEL_NAME = "all-MiniLM-L6-v2"  # ✅ Local transformer model

# === Step 1: Read Knowledge Base ===
def read_knowledge_base():
    print("📁 Reading knowledge base...")
    texts = []
    for filename in os.listdir(KB_FOLDER):
        if filename.endswith(".txt"):
            with open(os.path.join(KB_FOLDER, filename), "r", encoding="utf-8") as f:
                content = f.read()
                texts.append(content)
    combined_text = "\n".join(texts)
    print(f"✅ Characters read: {len(combined_text)}")
    print(f"🔹 Preview: {combined_text[:100]}...")
    return combined_text

# === Step 2: Chunk Text ===
def chunk_text(text, max_tokens=500):
    print("✂️ Chunking text...")
    words = text.split()
    chunks = [" ".join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]
    print(f"📄 Total Chunks: {len(chunks)}")
    return chunks

# === Step 3: Generate Embeddings Locally ===
def generate_embeddings(chunks, model_name=MODEL_NAME):
    print(f"🤖 Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    print("🔍 Generating embeddings for chunks...")
    vectors = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

    print(f"✅ Generated {len(vectors)} embeddings of dimension {vectors.shape[1]}")
    return vectors

# === Step 4: Save FAISS Index ===
def save_faiss_index(vectors):
    print("💾 Saving FAISS index...")
    if vectors is None or len(vectors) == 0:
        print("⚠️ No vectors to save.")
        return
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, "embeddings/faiss.index")
    print("✅ FAISS index saved to embeddings/faiss.index")

# === Main ===
if __name__ == "__main__":
    text = read_knowledge_base()
    chunks = chunk_text(text)
    vectors = generate_embeddings(chunks)
    save_faiss_index(vectors)