# Course AI Chatbot Backend

## Project Overview

A Python-based backend for an AI-powered course chatbot that processes video courses and enables interactive Q&A using Azure AI services.

## Features

-   Video to text conversion
-   Text embedding with Azure AI
-   FastAPI-based backend
-   Course management
-   AI-powered chat interface

## Prerequisites

-   Python 3.9+
-   Azure AI Services account
-   FFmpeg
-   Required libraries in `requirements.txt`

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file with:

```
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_deploymen_name
AZURE_EMBEDDING_MODEL=your_embedding_deployment_model_name
AZURE_EMBEDDING_DEPLOYMENT_NAME=your_embedding_deployment_name
```

### 3. Run the Application

```bash
uvicorn main:app --reload
```

## Project Structure

```
backend/
│
├── main.py             # FastAPI application entry point
├── VideoProcessor.py  # Video to text conversion
├── langchain_service.py   # Azure AI integration and Conversational AI logic
├── chat_cli            # Test file to Chat with CLI
└── requirements.txt    # Project dependencies
```

## Key Components

-   **Video Processing**: Convert course videos to text
-   **Embedding**: Use Azure AI to create vector representations
-   **Chat Interface**: Interactive Q&A with course content

## Technologies

-   FastAPI
-   MoviePy
-   Azure OpenAI
-   Pydantic
-   Uvicorn
-   Chroma DB

## Future Improvements

-   Advanced video processing
-   Multilingual support
-   Enhanced embedding techniques

## Troubleshooting

-   Ensure Azure credentials are correctly configured
-   Check FFmpeg installation
-   Verify video file compatibility

## Contribution

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push and create pull request
