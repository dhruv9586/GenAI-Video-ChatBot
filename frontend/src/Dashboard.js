import React, { useState } from 'react';
import 'antd/dist/reset.css';
import CourseList from './CourseList';
import Chat from './Chat';

export default function Dashboard() {
    const [selectedCourse, setSelectedCourse] = useState(null);
    return (
        <div className='container mx-auto p-4 max-w-4xl'>
            <h1 className='text-2xl font-bold mb-6'>Course Chat Assistant</h1>
            <CourseList
                onSelectCourseCallback={(course) => setSelectedCourse(course)}
            />
            {selectedCourse && <Chat selectedCourse={selectedCourse} />}
        </div>
    );
}
