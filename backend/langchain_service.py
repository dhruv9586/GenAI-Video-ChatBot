import os
from typing import Dict, List
from prompts import SYSTEM_TEMPLATE

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema import StrOutputParser


class LangChainService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        # Initialize Azure OpenAI with LangChain
        self.llm = AzureChatOpenAI(
            # openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            api_version="2024-02-01",
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7,
        )
        self.embeddings = AzureOpenAIEmbeddings(
            model=os.getenv("AZURE_EMBEDDING_MODEL"),
            deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            openai_api_type="azure",
            chunk_size=8000,
        )
        self.vector_store = Chroma(
            collection_name="video_course",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db",
        )

    def list_videos(self) -> List[Dict[str, str]]:
        try:
            # Get all metadata
            results = self.vector_store.get(include=["metadatas"])
            # Use a dictionary to track unique courses
            unique_courses = {}
            for metadata in results["metadatas"]:
                if metadata is None:
                    continue
                course_id = metadata.get("course_id")
                if course_id and course_id not in unique_courses:
                    unique_courses[course_id] = {
                        "course_id": course_id,
                        "course_name": metadata.get("course_name", ""),
                    }

            # Convert to list and sort by course_id
            unique_course_list = list(unique_courses.values())
            unique_course_list.sort(key=lambda x: x["course_id"])

            return unique_course_list

        except Exception as e:
            print(f"Error retrieving unique courses: {str(e)}")
            return []

    def is_video_processed(self, course_id: str):
        try:
            results = self.vector_store.get(where={"course_id": course_id}, limit=1)
            return len(results["ids"]) > 0
        except Exception as e:
            print(f"Error checking video processing status: {str(e)}")
            return False

    def delete_video(self, course_id: str):
        try:
            # Query documents with matching course_id to get their IDs
            results = self.vector_store.get(where={"course_id": course_id})
            if not results or not results["ids"]:
                print(f"No documents found with course_id: {course_id}")
                return 0

            self.vector_store.delete(results["ids"])

            num_deleted = len(results["ids"])
            print(
                f"Successfully deleted {num_deleted} documents with course_id: {course_id}"
            )
            return num_deleted
        except Exception as e:
            print(f"Error deleting documents: {str(e)}")
            raise e

    def ingest_transcript(self, documents: list[Document]):
        try:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
        except Exception as e:
            print(f"Error during ingesting video content: {e}")
            raise e

    def qa_chain(self, course_id: str):
        try:
            retriever = self.vector_store.as_retriever(
                search_kwargs={
                    "k": 3,  # Number of relevant chunks to retrieve,
                    "filter": {"course_id": course_id},  # Filter by course_id
                },
            )

            answer_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", SYSTEM_TEMPLATE),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{question}"),
                    ("system", "Context from course content: {context}"),
                ]
            )

            answer_chain = (
                RunnablePassthrough.assign(
                    context=lambda x: retriever.get_relevant_documents(x["question"])
                )
                | answer_prompt
                | self.llm
                | StrOutputParser()
            )

            return answer_chain

        except Exception as e:
            print(f"Error during full text search: {e}")
            raise e
