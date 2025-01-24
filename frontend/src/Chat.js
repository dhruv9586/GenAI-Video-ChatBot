import React, { useState } from 'react';
import Typewriter from 'typewriter-effect';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import 'antd/dist/reset.css';
import { axiosInstance } from './api';

const Chat = ({ selectedCourse = {} }) => {
    const [chatHistory, setChatHistory] = useState([]);
    const [userQuestion, setUserQuestion] = useState('');
    const [loadedChat, setLoadedChat] = useState(true);

    const createMarkup = (markdown) => {
        return { __html: marked(markdown) };
    };

    const handleSendMessage = async () => {
        if (!userQuestion.trim() || !selectedCourse) return;

        const newMessage = { user: userQuestion, assistant: '...' };
        setChatHistory((prev) => [...prev, newMessage]);
        setUserQuestion('');

        try {
            const { data } = await axiosInstance.post(`chat`, {
                question: userQuestion,
                course_id: selectedCourse.course_id,
                chat_history: chatHistory
            });

            setChatHistory((prev) => [
                ...prev.slice(0, -1),
                { user: userQuestion, assistant: data.response }
            ]);
            setLoadedChat(false);
        } catch (error) {
            console.error('Error sending message:', error);
            setChatHistory((prev) => [
                ...prev.slice(0, -1),
                {
                    user: userQuestion,
                    assistant: 'Error: Failed to get response'
                }
            ]);
            setLoadedChat(true);
        }
    };

    return (
        <div className='border rounded-lg'>
            <div className='p-4 border-b bg-gray-50'>
                <h2 className='font-medium'>
                    Chat about: {selectedCourse.course_name}
                </h2>
            </div>

            {/* Chat Messages */}
            <div className='h-96 overflow-y-auto p-4 space-y-4'>
                {chatHistory.map((msg, idx) => (
                    <div key={idx} className='space-y-2'>
                        <div className='bg-blue-50 p-3 rounded-lg'>
                            <p className='font-medium'>You:</p>
                            <p>{msg.user}</p>
                        </div>
                        <div className='bg-gray-50 p-3 rounded-lg'>
                            <p className='font-medium'>Assistant:</p>
                            {idx === chatHistory.length - 1 && !loadedChat ? (
                                <Typewriter
                                    options={{
                                        autoStart: true,
                                        loop: false,
                                        delay: 1,
                                        cursor: ''
                                    }}
                                    onInit={(typeWriter) => {
                                        typeWriter
                                            .typeString(
                                                DOMPurify.sanitize(
                                                    marked.parse(msg.assistant)
                                                )
                                            )
                                            .callFunction(() => {
                                                setLoadedChat(true);
                                            })
                                            .pause(20)
                                            .changeDelay(1)
                                            .start();
                                    }}
                                />
                            ) : (
                                <div
                                    dangerouslySetInnerHTML={createMarkup(
                                        msg.assistant
                                    )}
                                ></div>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Input Area */}
            <div className='p-4 border-t'>
                <div className='flex gap-2'>
                    <input
                        type='text'
                        value={userQuestion}
                        onChange={(e) => setUserQuestion(e.target.value)}
                        onKeyDown={(e) =>
                            e.key === 'Enter' && handleSendMessage()
                        }
                        placeholder='Ask a question about the course...'
                        className='flex-1 p-2 border rounded'
                    />
                    <button
                        onClick={handleSendMessage}
                        className='px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600'
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Chat;
