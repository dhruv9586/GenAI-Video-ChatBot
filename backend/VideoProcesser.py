from typing import List
from fastapi import UploadFile
import shutil
import tempfile
import whisper
from pathlib import Path
from moviepy import VideoFileClip
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class VideoProcessor:
    def __init__(self, file: UploadFile, course_id: str, course_name: str):
        self.file = file
        self.course_id = course_id
        self.course_name = course_name
        self.transcript = ""
        # Initialize whisper model (using the "base" model for balance of speed and accuracy)
        self.model = whisper.load_model("base")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def extract_text(self):
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded video file
            temp_video_path = Path(temp_dir) / "temp_video.mp4"
            with open(temp_video_path, "wb") as buffer:
                shutil.copyfileobj(self.file.file, buffer)

            # Extract audio from video
            temp_audio_path = Path(temp_dir) / "temp_audio.mp3"
            video = VideoFileClip(str(temp_video_path))
            video.audio.write_audiofile(str(temp_audio_path))
            video.close()

            # Transcribe audio using whisper
            result = self.model.transcribe(str(temp_audio_path))
            self.transcript = result["text"]
            return result

    def process_transcript(self) -> List[Document]:
        """Split transcript and create documents with metadata"""
        texts = self.text_splitter.split_text(self.transcript)
        documents = []
        for i, text in enumerate(texts):
            # Add metadata to each chunk for filtering
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        # "video_id": self.video_id,
                        "course_id": self.course_id,
                        "course_name": self.course_name,
                        "chunk_id": i,
                    },
                )
            )
        return documents
