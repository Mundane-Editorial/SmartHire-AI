import React, { useState } from 'react';
import './UploadResume.css';  // Import CSS file

function UploadResume() {
    const [file, setFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [score, setScore] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.type === 'application/pdf') {
            setFile(selectedFile);
            setMessage('');
        } else {
            setMessage('Please upload a valid PDF file.');
            setFile(null);
        }
    };

    const handleSubmit = async () => {
        if (!file) return setMessage('Please select a PDF file.');
        if (!jobDescription) return setMessage('Please enter a job description.');
    
        setLoading(true);
        setScore(null);
        setMessage('');
    
        const formData = new FormData();
        formData.append('file', file);
        formData.append('job_description', jobDescription);
    
        try {
            const res = await fetch('http://127.0.0.1:5000/upload', { method: 'POST', body: formData });
            const data = await res.json();
    
            if (res.status !== 200) {
                setLoading(false);
                setMessage('Upload failed. Please try again.');
                return;
            }
    
            const fileId = data.file_id;
            const interval = setInterval(async () => {
                const response = await fetch(`http://127.0.0.1:5000/get-score/${fileId}`);
                const result = await response.json();
    
                if (response.status === 200) {
                    setScore(result.score);
                    setLoading(false);
                    clearInterval(interval);
                }
            }, 2000);
        } catch (error) {
            setMessage('Error uploading file.');
            setLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <h2>Upload Your Resume</h2>
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            <textarea 
                placeholder="Enter Job Description" 
                value={jobDescription} 
                onChange={(e) => setJobDescription(e.target.value)}
            ></textarea>
            <button onClick={handleSubmit} disabled={loading}>Submit</button>
            {loading && <p className="processing">Processing...</p>}
            {message && <p className="error">{message}</p>}
            {score !== null && <p className="score">Score: {score}</p>}
        </div>
    );
}

export default UploadResume;
