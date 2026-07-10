# pip install sentence-transformers
# pip install langchain_huggingface

import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain_chroma import Chroma # type: ignore
from langchain_openai import OpenAIEmbeddings # type: ignore
from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from langchain_core.documents import Document # type: ignore
from uuid import uuid4

# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="tirukkural_collection",  
    embedding_function=embeddings,
    persist_directory="./chroma_tirukkural_db",
)

def initial_add_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chunks = content.split('</kural>')
    chunks = [chunk.strip() + '</kural>' for chunk in chunks if chunk.strip()]
    
    documents = []
    uuids = []
    
    for chunk in chunks:
        doc_id = str(uuid4())
        documents.append(Document(page_content=chunk, metadata={"source": "tirukkural"}))
        uuids.append(doc_id)
    
    vector_store.add_documents(documents=documents, ids=uuids)
    print(f"Added {len(documents)} kurals")
    return uuids

def show_data(data="all"):
    if data == "all":
        results = vector_store.get()
        return [(results['ids'][i], results['documents'][i]) for i in range(len(results['ids']))]
    elif isinstance(data, str) and len(data) == 36:
        result = vector_store.get(ids=[data])
        if result['ids']:
            return [(result['ids'][0], result['documents'][0])]
        return []

def add(text, uuid=None):
    if uuid is None:
        uuid = str(uuid4())
    
    document = Document(page_content=text, metadata={"source": "tirukkural"})
    vector_store.add_documents(documents=[document], ids=[uuid])
    print(f"Added with UUID: {uuid}")
    return uuid

def update(uuid, text):
    document = Document(page_content=text, metadata={"source": "tirukkural"})
    vector_store.update_document(document_id=uuid, document=document)
    print(f"Updated UUID: {uuid}")

def search(query, k=5):
    results = vector_store.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])


# if __name__ == "__main__":
#     print("=== TEST 1: Initial Add Data ===")
#     file_path = r"C:\Users\faroz\OneDrive\Documents\GenAI\Chat_APP - RAG - chroma\data\tirukkural_output.txt"
#     uuids = initial_add_data(file_path)
#     print(f"Total UUIDs created: {len(uuids)}")
#     print(f"First 3 UUIDs: {uuids[:3]}")
#     print()
    
#     print("=== TEST 2: Show All Data (first 2 only) ===")
#     all_data = show_data("all")
#     print(f"Total records: {len(all_data)}")
#     for i, (uuid, text) in enumerate(all_data[:2]):
#         print(f"\n{i+1}. UUID: {uuid}")
#         print(f"   Text: {text[:100]}...")
#     print()
    
#     print("=== TEST 3: Show Specific UUID ===")
#     test_uuid = uuids[0]
#     specific_data = show_data(test_uuid)
#     if specific_data:
#         uuid, text = specific_data[0]
#         print(f"UUID: {uuid}")
#         print(f"Text: {text[:200]}...")
#     print()
    
    
#     print("=== TEST 4: Add New Kural ===")
#     new_text = "Test Kural Content Here</kural>"
#     new_uuid = add(new_text)
#     verify = show_data(new_uuid)
#     print(f"Verification: {verify[0][1] if verify else 'Not found'}")
#     print()
    
#     print("=== TEST 5: Update Existing Kural ===")
#     updated_text = "Updated Test Kural Content</kural>"
#     update(new_uuid, updated_text)
#     verify = show_data(new_uuid)
#     print(f"After update: {verify[0][1] if verify else 'Not found'}")
#     print()
    
#     print("=== TEST 6: Search Function ===")
#     search_results = search("knowledge", k=3)
#     print(f"Search results for 'knowledge' (k=3):")
#     for i, (uuid, text) in enumerate(search_results):
#         print(f"\n{i+1}. Text: {text[:100]}...")
#     print()
    
#     print("=== All Tests Completed ===")