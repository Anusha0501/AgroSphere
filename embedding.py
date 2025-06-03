import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

def embed_and_save_documents():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    loader = PyPDFDirectoryLoader("./Agriculture")
    print("Initialized PDF loader")

    docs = loader.load()
    print(f"Loaded {len(docs)} documents")

    unique_files = set()
    for doc in docs:
        file_name = os.path.basename(doc.metadata.get('source', 'Unknown'))
        if file_name not in unique_files:
            print(f"    File loaded: {file_name}")
            unique_files.add(file_name)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)
    print(f"Split into {len(final_documents)} chunks")

    for doc in final_documents:
        if 'source' in doc.metadata:
            source_file = doc.metadata['source']
            doc.metadata['source'] = os.path.basename(source_file)
        else:
            doc.metadata['source'] = os.path.basename(loader.directory)

    # Save to Chroma instead of FAISS
    print("Saving to Chroma...")
    vectorstore = Chroma.from_documents(final_documents, embeddings, persist_directory="my_chroma_store")
    vectorstore.persist()
    print("Chroma vector store saved at 'my_chroma_store'")

embed_and_save_documents()
