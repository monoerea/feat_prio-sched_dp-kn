'use client';
import React, { useState } from 'react';
import DataTable from './DataTable'; // Import the DataTable component
import { parseCsv } from './utils/csvUtils'; // Util function to parse CSV data
import Image from 'next/image';


const FileUploadComponent = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [csvData, setCsvData] = useState([]);
    const [displayRowCount, setDisplayRowCount] = useState(5); // Number of rows to display
    const [uploadMessage, setUploadMessage] = useState('');
    const [successMessage, setsuccessMessage] = useState('');

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
            setsuccessMessage(data);
            return data;

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
    
        // Check if the file type is CSV before proceeding
        if (selectedFile.type !== 'text/csv') {
            console.error('Selected file is not a CSV file.');
            setUploadMessage('Please select a valid CSV file.');
            return;
        }
    
        // Read the file content using FileReader
        const reader = new FileReader();
        reader.onload = async (event) => {
            const fileContent = event.target.result;
    
            try {
                // Parse the CSV data
                const dataArray = parseCsv(fileContent); // Implement parseCsv according to your utility function
                console.log(Object.keys(dataArray[0]).includes('churn'));
                // Check if the parsed data contains the necessary fields
                if (dataArray.length === 0 || (!Object.keys(dataArray[0]).includes('target') && !Object.keys(dataArray[0]).includes('label') && !Object.keys(dataArray[0]).includes('churn'))) {
                    throw new Error('No required field (target, label, churn) found in the uploaded CSV file.');
                }
                
    
                // Proceed with file upload
                const formData = new FormData();
                formData.append('file', selectedFile);
    
                console.log('Uploading file:', selectedFile.name);
    
                const response = await fetch('http://localhost:5000/api/upload', {
                    method: 'POST',
                    body: formData,
                });
    
                if (!response.ok) {
                    throw new Error('Failed to upload file');
                }
    
                const responseData = await response.json();
                console.log('File metadata:', responseData);
    
                // Set the upload message to the message returned from the backend
                setUploadMessage(responseData.message);
    
                // Assuming runService is a function that returns a promise or async function
                const service = await runService();
                const state = await service;
                console.log('Service state:', state);
    
            } catch (error) {
                console.error('Error handling file upload:', error.message);
                setUploadMessage(`Error handling file upload: ${error.message}`);
            }
        };
    
        // Read the file as text to parse its contents
        reader.readAsText(selectedFile);
    };
    
    
    
    

    return (
    <section class="bg-white dark:bg-gray-900 min-h-screen overflow-y-auto">
    <div class="grid max-w-screen-xl px-4 py-5 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12 place-self-center">
        <div className="lg:col-span-7 xl:pt-20">
            <div class="m-auto place-self-center ">
                <h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white">Feature Selection Pipeline</h1>
                <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">Utilizing Priority Task Scheduling for Batch Procesing and 0/1 Dynamic Programming Knapsack for Enhanced Feature Selection</p>
                
            </div>
        <div>
            <input
                id="file_input"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="block mb-5 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400
                file:mr-5 file:py-3 file:px-3 file:border-0
                    file:font-medium file:text-white file:p-20
                hover:file:cursor-pointer hover:file:bg-gray-500
                    file:bg-gray-600 file:text-foreground file:text-md placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:opacity-50"
            />
            {selectedFile && (
                <div className="mt-2">
                    <p className="text-sm mb-2">Selected File: {selectedFile.name}</p>
                    <button
                        onClick={handleUpload}
                        className="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 dark:focus:ring-gray-800"
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
        </div>            
        </div>
        <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
                <Image src="bg.svg" alt="mockup" width={400} height={400}/>
        </div>
        {csvData.length > 0 && (
        <div className="lg:mt-5 lg:col-span-12 lg:flex mt-4">
            <DataTable data={csvData} displayRowCount={displayRowCount} />
        </div>
        )}
        {Object.keys(successMessage).length > 0 && (
        <div className='rounded-lg  bg-slate-700 lg:mt-5 lg:col-span-12'>
            <h1 className=' text-slate-300 text-4xl p-5 bg-slate-600 rounded-lg text-center font-semibold'>
                    Random Forest Model Statistics
                    </h1>
            <div className='rounded-lg  bg-slate-700 lg:col-span-12 lg:flex p-3'>
                {Object.keys(successMessage).map((key, index) => (
                    <h1 className='m-3 text-slate-300 text-4xl p-5 bg-slate-600 rounded-lg text-center font-semibold' key={index}>{key.toUpperCase()} {successMessage[key]}</h1>
                ))}
                
            </div>
        </div>
        )}
    </div>
    </section>
    );
};

export default FileUploadComponent;
