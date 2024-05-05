import os
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import FAISS
from langchain_voyageai import VoyageAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main():
    VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
    embed_model = "voyage-law-2"
    chunk_size = 1000
    chunk_overlap = 200
    # client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    embeddigns = VoyageAIEmbeddings(
        voyage_api_key=VOYAGE_API_KEY, model=embed_model)
    data_path = "../../data/"
    storage_path = "../../storage"
    file = "title_abst_RAG AND prompt.json"
    loader = JSONLoader(os.path.join(data_path, file), jq_schema=".[]")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(data)
    vectorstore = FAISS.from_documents(documents=docs, embedding=embeddigns)
    vectorstore.save_local(os.path.join(
        storage_path, file.replace(".json", "")))


if __name__ == "__main__":
    main()
