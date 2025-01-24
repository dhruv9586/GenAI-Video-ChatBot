# Course Chat Assistant

## Overview

A React-based web application that allows users to upload course videos and interact with an AI assistant about the course content.

## Features

-   Video course upload
-   AI-powered course chat
-   Course management (list, delete)
-   Markdown-supported responses
-   Typewriter effect for AI responses

## Prerequisites

-   Node.js (v16+)
-   npm or yarn
-   Backend server running on localhost:8000

## Tech Stack

-   React
-   Axios
-   Ant Design
-   Typewriter Effect
-   Marked (Markdown parsing)
-   DOMPurify
-   Tailwind CSS
-   Lucide React Icons

## Installation

### Frontend Setup

1. Clone the repository

```bash
git clone https://your-repository-url.git
cd course-chat-frontend
```

2. Install dependencies

```bash
npm install
```

3. Start the development server

```bash
npm start
```

### Backend Requirements

-   Requires a backend server with these endpoints:
    -   GET `/courses`
    -   POST `/process-video`
    -   DELETE `/courses/:courseId`
    -   POST `/chat`

## Configuration

-   Update `API_BASE_URL` in the component for different backend endpoints
-   Ensure CORS is configured on the backend

## Environment Variables

-   Create a `.env` file if needed for API endpoint configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a pull request

## License

[MIT]

## Contact

[dhruv9586@gmail.com]
