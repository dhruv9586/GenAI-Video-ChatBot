from typing import Dict, List
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

from VideoProcesser import VideoProcessor
from langchain_service import LangChainService

# Load environment variables
load_dotenv(override=True)

app = FastAPI(title="Video Transcription API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test():
    return JSONResponse({"status": "success", "message": "Ok Tested"})


class VideoUploadRequest(BaseModel):
    file: UploadFile = File(...)
    course_id: str
    course_name: str
    # video_id: str


@app.post("/process-video")
async def transcribe_video(
    file: UploadFile = File(...),
    course_id: str = Form(...),
    course_name: str = Form(...),
):
    try:
        # check if video is already processed or not
        langchain_service = LangChainService()
        already_processed = langchain_service.is_video_processed(course_id)

        if already_processed:
            raise Exception("It is already been processed")

        # processing video to extract text
        video_processor = VideoProcessor(file, course_id, course_name)
        result = video_processor.extract_text()
        documents = video_processor.process_transcript()

        # embed text to vector store
        langchain_service.ingest_transcript(documents)

        return JSONResponse(
            {
                "status": "success",
                "transcription": result["text"],
                "segments": result["segments"],
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up
        file.file.close()


class ChatInput(BaseModel):
    question: str
    course_id: str
    chat_history: List[Dict[str, str]] = []


@app.get("/courses")
async def list_courses():
    try:
        langchain_service = LangChainService()
        courses = langchain_service.list_videos()

        return JSONResponse({"status": "success", "courses": courses})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/course/{course_id}")
async def delete_coures(course_id: str):
    try:
        langchain_service = LangChainService()
        langchain_service.delete_video(course_id)

        return JSONResponse(
            {"status": "success", "message": "Courser deleted successfully."}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(chat_input: ChatInput):
    """Updated chat endpoint using modern LangChain patterns"""
    try:
        if chat_input.course_id is None:
            raise Exception("Course Id is required to chat.")

        langchain_service = LangChainService()
        # Create chat chain
        chat_chain = langchain_service.qa_chain(chat_input.course_id)
        # Format chat history for the prompt
        formatted_history = []
        for msg in chat_input.chat_history:
            formatted_history.extend(
                [("human", msg["user"]), ("assistant", msg["assistant"])]
            )

        # Get answer
        answer = await chat_chain.ainvoke(
            {"chat_history": formatted_history, "question": chat_input.question}
        )

        return {
            "response": answer,
            "chat_history": chat_input.chat_history
            + [{"user": chat_input.question, "assistant": answer}],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in chat completion: {str(e)}"
        )


@app.get("/list-documents")
async def list_documents():
    """List all documents in the vector store"""
    try:
        langchain_service = LangChainService()
        collection = langchain_service.vector_store._collection

        return {"document_count": collection.count(), "documents": collection.get()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving documents: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
