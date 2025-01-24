# GenAI Video Chatbot

The **GenAI Video Chatbot** is an AI-powered web application designed to assist users in clarifying their doubts about specific courses instantly. The app leverages a React-based frontend and a FastAPI-powered Python backend deployed on Azure. By combining cutting-edge Generative AI technology with seamless integration, this app offers an intuitive platform for course-related queries and support.

---

## Features

-   **AI-Powered Chatbot**: Instant answers to user queries using Generative AI models.
-   **Video and Text-Based Interaction**: Supports both text and video chat for an engaging experience.
-   **Course-Specific Support**: Tailored responses based on the selected course content.
-   **Real-Time Performance**: Built for speed and efficiency to ensure a smooth user experience.
-   **Secure and Scalable**: Deployed on Azure with robust security and scalability features.

---

## Monorepo Structure

This project follows a monorepo structure, organizing the frontend and backend into separate folders:

```
GenAI-Video-Chatbot/
├── frontend/
│   └── README.md
├── backend/
│   └── README.md
└── README.md
```

### 1. **Frontend**

-   **Technology**: React.js with supporting libraries like Tailwind CSS for styling.
-   **Purpose**: Provides the user interface for interacting with the chatbot.
-   **Features**:
    -   Course selection and real-time query handling.
    -   Seamless video integration.

[See the detailed Frontend README](./frontend/README.md)

### 2. **Backend**

-   **Technology**: Python, FastAPI, Azure.
-   **Purpose**: Handles AI model operations, user queries, and integrations with external APIs.
-   **Features**:
    -   Integration with Azure OpenAI services for generating responses.
    -   RESTful APIs for seamless communication with the frontend.

[See the detailed Backend README](./backend/README.md)
