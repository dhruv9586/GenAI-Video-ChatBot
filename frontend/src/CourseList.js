import React, { useState, useEffect } from 'react';
import { Trash2, Upload } from 'lucide-react';
import { Modal, notification } from 'antd';
import 'antd/dist/reset.css';
import { axiosInstance } from './api';

const CourseList = ({ onSelectCourseCallback = () => {} }) => {
    const [notificationApi, contextHolder] = notification.useNotification();
    const [courses, setCourses] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [courseToDelete, setCourseToDelete] = useState(null);

    // Fetch courses on component mount
    useEffect(() => {
        fetchCourses();
    }, []);

    const fetchCourses = async () => {
        try {
            const { data } = await axiosInstance.get(`courses`);
            setCourses(data.courses);
        } catch (error) {
            console.error('Error fetching courses:', error);
            notificationApi.error({
                message: 'Fetching Courses',
                description: `Error fetching courses: ${error.message}`
            });
        }
    };

    const handleDeleteClick = (course, event) => {
        event.stopPropagation(); // Prevent course selection when clicking delete
        setCourseToDelete(course);
    };

    const handleDeleteConfirm = async () => {
        try {
            await axiosInstance.delete(`course/${courseToDelete.course_id}`);

            // Remove course from state
            setCourses(
                courses.filter(
                    (course) => course.course_id !== courseToDelete.course_id
                )
            );

            // If the deleted course was selected, clear the selection and chat history
            if (selectedCourse?.course_id === courseToDelete.course_id) {
                setSelectedCourse(null);
            }

            // Show success message
            notificationApi.success({
                message: 'Course Deleted',
                description: 'The course has been successfully deleted.'
            });
        } catch (error) {
            console.error('Error deleting course:', error);
            notificationApi.error({
                message: 'Error: Course Deleted',
                description: 'Failed to delete course. Please try again.'
            });
        } finally {
            setCourseToDelete(null); // Close the dialog
        }
    };

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        // Generate simple IDs
        const courseId = `course-${Date.now()}`;
        const courseName = file.name.split('.')[0]; // Use filename as course name

        formData.append('course_id', courseId);
        formData.append('course_name', courseName);

        try {
            await axiosInstance.post(`process-video`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            fetchCourses(); // Refresh course list

            notificationApi.success({
                message: 'Course Uploaded',
                description: 'The course has been successfully uploaded.'
            });
        } catch (error) {
            console.error('Error uploading video:', error);
            notificationApi.error({
                message: 'Error: Course Uploaded',
                description: 'The course upload has been failed.'
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {contextHolder}
            {/* Delete Confirmation Modal */}
            <Modal
                title='Delete Course'
                open={!!courseToDelete}
                onOk={handleDeleteConfirm}
                onCancel={() => setCourseToDelete(null)}
                okText='Delete'
                cancelText='Cancel'
                okButtonProps={{
                    danger: true
                }}
                centered
            >
                <p>
                    Are you sure you want to delete "
                    {courseToDelete?.course_name}"? This action cannot be
                    undone.
                </p>
            </Modal>
            {/* Upload Section */}
            <div className='mb-8'>
                <label className='flex flex-col items-center p-4 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50'>
                    <Upload className='w-8 h-8 mb-2 text-gray-600' />
                    <span className='text-sm text-gray-500'>
                        Upload Course Video
                    </span>
                    <input
                        type='file'
                        className='hidden'
                        accept='video/*'
                        onChange={handleFileUpload}
                        disabled={loading}
                    />
                </label>
                {loading && (
                    <p className='text-center mt-2'>Processing video...</p>
                )}
            </div>

            <div className='grid grid-cols-2 gap-4 mb-8'>
                {courses.map((course) => (
                    <div
                        key={course.course_id}
                        onClick={() => {
                            setSelectedCourse(course);
                            onSelectCourseCallback(course);
                        }}
                        className={`p-4 rounded-lg cursor-pointer border ${
                            selectedCourse?.course_id === course.course_id
                                ? 'border-blue-500 bg-blue-50'
                                : 'border-gray-200 hover:border-blue-300'
                        }`}
                    >
                        <div className='flex justify-between items-center'>
                            <h3 className='font-medium'>
                                {course.course_name}
                            </h3>
                            <button
                                onClick={(e) => handleDeleteClick(course, e)}
                                className='p-1 text-gray-500 hover:text-red-500 rounded-full hover:bg-gray-100'
                                title='Delete course'
                            >
                                <Trash2 className='w-4 h-4' />
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </>
    );
};

export default CourseList;
