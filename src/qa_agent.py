import os
import logging

from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document, ChatMessage,SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter

class QAModule:
    """A module for answering questions based on PDF content using OpenAI and FAISS for retrieval-augmented generation (RAG)."""

    def __init__(self, model_name: str = "gpt-4o-mini", embedding_model: str = "text-embedding-ada-002"):
        """
        Initializes the QAModule with a language model and embedding model for question answering.

        Args:
            model_name (str): The name of the OpenAI model to use for question answering.
            embedding_model (str): The name of the embedding model for vector store indexing.
        """
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OpenAI API key is not set. Please set it as an environment variable.")
        
        # Initialize LLM for question answering
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        
        # Initialize embedding model and vector store
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
        self.vector_store = None  # Initialized later with build_index()

    def build_index(self, text: str):
        """
        Splits and indexes the provided text into vectorized chunks for retrieval.
        
        Args:
            text (str): The text content to index.
        """
        try:
            documents = [Document(page_content=chunk) for chunk in self.text_splitter.split_text(text)]
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            logging.info("Successfully built vector index for provided text.")
        except Exception as e:
            logging.exception("Error building vector index: %s", e)
            raise RuntimeError("Failed to build vector index.")

    def retrieve_relevant_chunks(self, question: str, k: int = 3) -> List[Document]:
        """
        Retrieves the top-k relevant chunks for a given question.

        Args:
            question (str): The question to find relevant chunks for.
            k (int): The number of top relevant chunks to retrieve.

        Returns:
            List[Document]: A list of Documents containing the relevant chunks.
        """
        if not self.vector_store:
            raise ValueError("Vector store is not initialized. Call 'build_index' first.")

        try:
            return self.vector_store.similarity_search(question, k=k)
        except Exception as e:
            logging.exception("Error during chunk retrieval: %s", e)
            return []

    def answer_question(self, question: str) -> Optional[str]:
        """
        Generates an answer based on retrieved chunks.

        Args:
            question (str): The question to answer.

        Returns:
            Optional[str]: The generated answer or None if an error occurs.
        """
        relevant_chunks = self.retrieve_relevant_chunks(question)
        if not relevant_chunks:
            logging.warning("No relevant chunks found for the question: %s", question)
            return "Data Not Available"

        # Combine chunks into a single context for the LLM prompt
        context = "\n".join([chunk.page_content for chunk in relevant_chunks])

        # Formulate the prompt with RAG structure
        prompt_template = PromptTemplate(
            template="Context: {context}\n\nQuestion: {question}\nAnswer:",
            input_variables=["context", "question"]
        )
        prompt = prompt_template.format(context=context, question=question)
        system_message = SystemMessage(content="If the information is not directly available in the context, respond with 'Data Not Available'.")

        # Create the user message with the prompt
        user_message = ChatMessage(role="user", content=prompt)

        # Compile messages for the ChatOpenAI model
        messages = [system_message, user_message]
        
        try:
            response = self.llm(messages)
            answer_text = response.content.strip()
            logging.info("Generated response for question: %s", question)
            return answer_text
        except Exception as e:
            logging.exception("Error generating answer: %s", e)
            return "Data Not Available"

    def answer_questions(self, text: str, questions: List[str]) -> Dict[str, Optional[str]]:
        """
        Answers a list of questions based on the indexed text.

        Args:
            text (str): The text content to index and search.
            questions (List[str]): A list of questions to answer.

        Returns:
            Dict[str, Optional[str]]: A dictionary mapping questions to their answers.
        """
        try:
            self.build_index(text)  # Build vector store for the provided text
            results = {question: self.answer_question(question) for question in questions}
            logging.info("Successfully answered all questions.")
            return results
        except Exception as e:
            logging.exception("Error in answering questions: %s", e)
            return {question: "Data Not Available" for question in questions}
