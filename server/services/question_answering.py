from typing import Optional

from env import HUGGINGFACEHUB_API_TOKEN, OPENAI_API_KEY
# from transformers import pipeline
from fastapi import HTTPException
from huggingface_hub import InferenceClient
from utils import get_text_chunks, get_vectorstore
from langchain_openai import OpenAI

def generate_answer(question: str, document_content: str, model_type: Optional[str] = "huggingface") -> str:
    """
    Generate an answer to a question based on document content using different models.
    
    Args:
        question (str): The question to be answered
        document_content (str): The source document content
        model_type (str): Type of model to use ("huggingface", "openai", or "local")
    
    Returns:
        str: Generated answer
    """
    try:
        # Split the document into chunks
        text_chunks = get_text_chunks(document_content)
        texts = [chunk for chunk in text_chunks if chunk]

        # Create embeddings using sentence-transformers
        vectorstore = get_vectorstore(texts)
        
        if model_type == "huggingface":
            if not HUGGINGFACEHUB_API_TOKEN:
                raise ValueError("HuggingFace API token not found")
            
            # Initialize HuggingFace Hub client
            client = InferenceClient(token=HUGGINGFACEHUB_API_TOKEN)
            
            # Get more relevant documents and combine with weights
            relevant_docs = vectorstore.similarity_search_with_score(question, k=5)
            
            # Sort by relevance score and format context
            sorted_docs = sorted(relevant_docs, key=lambda x: x[1], reverse=True)
            formatted_contexts = []
            
            for doc, score in sorted_docs:
                formatted_contexts.append(f"Relevant text (confidence: {score:.2f}):\n{doc.page_content}")
            
            context = "\n\n".join(formatted_contexts)
            
            # Enhanced prompt template with specific instructions
            prompt = f"""Based on the provided context, give a detailed and comprehensive answer to the question. 
            Include relevant information from the context and explain your reasoning.
            If the context doesn't contain enough information, acknowledge what isn't known.
            
            Context:
            {context}
            
            Question: {question}
            
            Detailed answer:"""
            
            # Configure generation parameters for longer, more detailed output
            response = client.text_generation(
                prompt,
                model="meta-llama/Llama-3.2-3B-Instruct",  # You could also use larger models like flan-t5-large
                max_new_tokens=2048,  # Increased token limit
                temperature=0.7,  # Slightly increased for more creative responses
                do_sample=True,
            )
            
            # Post-process response
            cleaned_response = response.strip()
            
            # # Add confidence disclaimer if response is too short
            # if len(cleaned_response.split()) < 20:
            #     cleaned_response += "\n\nNote: The model provided a brief response. You may want to:\n" \
            #                     "1. Rephrase the question\n" \
            #                     "2. Provide more context\n" \
            #                     "3. Try a larger model variant"
            
            return cleaned_response

        elif model_type == "openai":
            # Using OpenAI
            if not OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found")
            
            llm = OpenAI(
                temperature=0.7,
                max_tokens=500
            )
            
            # Get relevant documents
            relevant_docs = vectorstore.similarity_search(question, k=3)
            context = " ".join([doc.page_content for doc in relevant_docs])
            
            prompt = f"""Answer the question based on the following context:
            
            Context: {context}
            
            Question: {question}
            
            Answer: """
            
            response = llm.predict(prompt)
            return response


        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer: {str(e)}"
        )
