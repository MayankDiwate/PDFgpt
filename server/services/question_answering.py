import os
from typing import Optional
from utils import get_text_chunks, get_vectorstore
from huggingface_hub import InferenceClient
from transformers import pipeline
from fastapi import HTTPException

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
            if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
                raise ValueError("HuggingFace API token not found")
            
            # Initialize HuggingFace Hub client
            client = InferenceClient(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
            
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
                model="google/flan-t5-large",  # You could also use larger models like flan-t5-large
                max_new_tokens=250,  # Increased token limit
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
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OpenAI API key not found")
            
            from langchain_openai import OpenAI
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

        elif model_type == "local":
            # Using local HuggingFace pipeline
            qa_pipeline = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad",
                tokenizer="distilbert-base-cased-distilled-squad"
            )
            
            # For local model, we'll use a simpler approach
            most_relevant_doc = vectorstore.similarity_search(question, k=1)[0]
            
            result = qa_pipeline(
                question=question,
                context=most_relevant_doc.page_content
            )
            return result['answer']

        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer: {str(e)}"
        )
