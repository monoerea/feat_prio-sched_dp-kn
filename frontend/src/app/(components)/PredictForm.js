// PredictForm.js

import React, { useState, useEffect } from 'react';

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
                setFeatures(fetchedFeatures);
            } catch (error) {
                setError('Failed to fetch features. Please try again.');
                console.error('Error:', error);
            }
        };

        getFeatures(); // Call the async function inside useEffect

    }, []); // Empty dependency array ensures this effect runs only once on mount

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
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
            setPrediction(data.prediction);
            setError(null);
        } catch (error) {
            console.error('Error predicting:', error);
            setError('Failed to predict. Please try again.');
            setPrediction(null);
        }
    };

    return (
        <div>
            <h2>Predict or Evaluate Manual Input</h2>
            <form onSubmit={handleSubmit}>
                {features.map((feature, index) => (
                    <div key={index}>
                        <label htmlFor={`feature${index + 1}`}>{`Feature ${index + 1}:`}</label>
                        <input
                            type="text"
                            id={`feature${index + 1}`}
                            name={`feature${index + 1}`}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                ))}

                <button type="submit">Predict</button>
            </form>

            {error && <p>{error}</p>}
            {prediction && (
                <div>
                    <h3>Prediction Result:</h3>
                    <p>{JSON.stringify(prediction)}</p>
                </div>
            )}
        </div>
    );
};

export default PredictForm;
