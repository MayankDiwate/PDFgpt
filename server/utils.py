from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
    
def get_text_chunks(document_content):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    texts = text_splitter.split_text(document_content)
    return texts

def get_vectorstore(text_chunks):

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    # embedding_model = SentenceTransformer(model_name)
    # embeddings_list = embedding_model.encode(texts)
    
    # Create embeddings instance for FAISS
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # Create a FAISS index from texts
    vectorstore = FAISS.from_texts(
        texts=text_chunks,
        embedding=embeddings
    )
    return vectorstore