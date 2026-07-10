# pip install sentence-transformers
# pip install langchain_huggingface

import os

os.environ["OPENAI_API_KEY"] = "your-api-key"

from langchain_chroma import Chroma # type: ignore
from langchain_openai import OpenAIEmbeddings # type: ignore
from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from langchain_core.documents import Document # type: ignore
from uuid import uuid4

# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="dummyCorp_collection",  
    embedding_function=embeddings,
    persist_directory="./chroma_dummyCorp_db",
)

def initial_add_data(text_list):
 
    if not isinstance(text_list, list) or not all(isinstance(t, str) for t in text_list):
        raise ValueError("Expected a list of strings as input.")
    
    documents = []
    uuids = []

    for text in text_list:
        doc_id = str(uuid4())
        documents.append(Document(page_content=text.strip(), metadata={"source": "dummycompany"}))
        uuids.append(doc_id)

    vector_store.add_documents(documents=documents, ids=uuids)
    print(f"Added {len(documents)} items to the collection.")
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