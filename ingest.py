from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def ingest_pdfs(pdf_list):
    try:
        all_docs = []

        for pdf_path in pdf_list:
            try:
                loader = PyPDFLoader(pdf_path)
                documents = loader.load()
            except Exception as e:
                print(f"Skipping {pdf_path}: {e}")
                continue

            for doc in documents:
                doc.metadata["source"] = pdf_path

            all_docs.extend(documents)

        print(f"Loaded {len(all_docs)} pages")

        if not all_docs:
            print("No pages loaded, nothing to ingest")
            return

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(all_docs)
        print(f"Created {len(chunks)} chunks")

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        vectorstore = Chroma(
            persist_directory="db",
            embedding_function=embeddings
        )

        vectorstore.add_documents(chunks)  # langchain_chroma persists automatically

        print("All PDFs processed and stored successfully")

    except Exception as e:
        print("Ingestion Error:", e)
