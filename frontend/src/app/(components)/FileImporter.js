'use client';
import React, { useState } from 'react';
import DataTable from './DataTable'; // Import the DataTable component
import { parseCsv } from './utils/csvUtils'; // Util function to parse CSV data

const FileUploadComponent = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [csvData, setCsvData] = useState([]);
    const [displayRowCount, setDisplayRowCount] = useState(5); // Number of rows to display
    const [uploadMessage, setUploadMessage] = useState('');

    const runService = async () => {
        try {
            console.log('Running ML service');
    
            const response = await fetch('http://localhost:5000/api/pipeline', {
                method: 'POST',  // Corrected to POST method
                headers: {
                    "Content-Type": "application/json"  // Corrected the headers format
                },
            });
    
            if (!response.ok) {
                throw new Error('Failed to run service');
            }
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error Fetching Data:', error.message);
        }
    };
    

    const handleFileChange = (e) => {
        const file = e.target.files[0];

        if (file && file.type === 'text/csv') {
            setSelectedFile(file);

            const reader = new FileReader();

            reader.onload = (event) => {
                const text = event.target.result;
                const dataArray = parseCsv(text); // Parse CSV data using util function
                setCsvData(dataArray);
            };

            reader.readAsText(file);
        } else {
            setSelectedFile(null);
            setCsvData([]);
            console.error('Please select a CSV file.');
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            console.error('No file selected.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            console.log('Uploading file:', selectedFile.name);

            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to upload file');
            }

            const data = await response.json();
            console.log('File metadata:', data);

            // Set the upload message to the message returned from the backend
            setUploadMessage(data.message);
            const service = await runService();
            console.log('File metadata:', service);

        } catch (error) {
            console.error('Error uploading file:', error.message);
            setUploadMessage(`Error uploading file: ${error.message}`);
        }
    };

    return (
        <div>
            <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="border border-gray-300 p-2 rounded-md text-sm"
            />
            {selectedFile && (
                <div className="mt-2">
                    <p className="text-sm">Selected File: {selectedFile.name}</p>
                    <button
                        onClick={handleUpload}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2 text-sm"
                    >
                        Upload File
                    </button>
                </div>
            )}
            {uploadMessage && (
                <div className="mt-2">
                    <p className="text-sm">{uploadMessage}</p>
                </div>
            )}
            {csvData.length > 0 && (
                <div className="mt-4">
                    <DataTable data={csvData} displayRowCount={displayRowCount} />
                </div>
            )}
        </div>
    );
};

export default FileUploadComponent;
