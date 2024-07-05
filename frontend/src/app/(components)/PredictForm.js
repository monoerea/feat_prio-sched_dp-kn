// PredictForm.js

import React, { useState, useEffect } from 'react';
import DynamicForm from './DynamicForm';
import { dynamicGrouper } from './utils/uiUtils';

const PredictForm = () => {
    const [formData, setFormData] = useState({});
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState(null);
    const [features, setFeatures] = useState([]);

    // Function to fetch features from the backend
    const fetchFeatures = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/get_features');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching features:', error.message);
            throw error; // Rethrow the error to handle it further up the call stack
        }
    };

    // useEffect to fetch features when component mounts
    useEffect(() => {
        const getFeatures = async () => {
            try {
                const fetchedFeatures = await fetchFeatures();
                const feats = dynamicGrouper(fetchedFeatures);
                setFeatures(feats);
            } catch (error) {
                setError('Failed to fetch features. Please try again.');
                console.error('Error:', error);
            }
        };

        getFeatures(); // Call the async function inside useEffect

    }, []); // Empty dependency array ensures this effect runs only once on mount

    const handleInputChange = (e) => {
        console.log(e);
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/api/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch');
            }

            const data = await response.json();
            setPrediction(data);
            setError(null);
        } catch (error) {
            console.error('Error predicting:', error);
            setError('Failed to predict. Please try again.');
            setPrediction(null);
        }
    };

    return (
        <div className='absolute inset-0 flex flex-col max-w-screen-lg max-h-screen mt-20 bg-slate-800 rounded-2xl shadow-md px-24  py-3 mx-auto overflow-auto'>
            <div className='bg-slate-600 rounded-md m-10'>
                  <h2 className="text-slate-800 text-4xl font-semibold text-center p-5">Predict Manual Input</h2>
            </div>
            
            <form onSubmit={handleSubmit} className="justify-around" >
                {features.length > 0 && (
                    <DynamicForm
                        fields={features}
                        handleFormDataChange={handleInputChange}
                    />
                )}
                <div className='flex justify-center'>
                    <button className='bg-slate-500 text-sky-100 py-2 px-4 rounded focus:outline-none focus:bg-slate-400
                        text-sm font-semibold shadow-sm ring-1 ring-inset ring-slate-300 hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50' type='submit'>
                        Predict
                    </button>
                </div>

            </form>

            {error && <p className="text-red-500 mt-4 text-center">{error}</p>}
            {prediction && (
                <div className="mt-4">
                    
                    <pre className="bg-gray-800 p-4 rounded-lg text-white flex flex-row justify-center">
                    <div className='m-3 p-5'>
                        <h3 className="text-white text-lg font-semibold text-center">Prediction Result</h3>
                        <h1 className='text-center text-5xl'>
                            {JSON.stringify(prediction.prediction[0])}
                        </h1>
                    </div>
                    <div className='m-3 p-5'>
                        <h3 className="text-white text-lg font-semibold text-center">Probability of Result</h3>
                        <h1 className='text-center text-5xl'>
                            {JSON.stringify(prediction.probability[0][0])*100}% 
                        </h1>
                    </div>
                    
                    </pre>
                </div>
            )}
        </div>
    );
};

export default PredictForm;
