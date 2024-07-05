from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from joblib import load
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)  # Set log level to DEBUG for all loggers

from sklearn.pipeline import Pipeline

# Add the project root directory to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
sys.path.insert(0, project_root)

from backend.pipeline import DataCleaner, DataTransformer, TaskDispatcher, Scheduler, Process, FeatureSelector, Knapsack

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)  # Set Flask app logger to DEBUG level

# Define the directory where files will be uploaded
UPLOAD_DIRECTORY = os.path.join(project_root, 'backend', 'data', 'uploads')
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Global variables
global final_features
final_features = None  # Initialize final_features
filepath = ''
global rfa
rfa = None  # Initialize rfa

# Route for getting features
@app.route('/api/get_features', methods=['GET'])
def get_features():
    global final_features
    if final_features is None:
        return jsonify({'error': 'Features not available. Please run the pipeline first.'}), 400
    
    app.logger.info(f"Final Features: {final_features}")
    return jsonify(final_features)

# Route for handling file upload
@app.route('/api/upload', methods=['POST'])
def upload_file():
    global filepath
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file
        filename = file.filename
        filepath = os.path.join(UPLOAD_DIRECTORY, filename)
        file.save(filepath)

        app.logger.info(f"File uploaded successfully: {filepath}")
        return jsonify({'message': 'File uploaded successfully', 'filepath': filepath}), 200

    except Exception as e:
        app.logger.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Route for running the machine learning pipeline
@app.route('/api/pipeline', methods=['POST'])
def run_service():
    try:
        global rfa, final_features

        app.logger.info("Running ML service...")

        # Read uploaded file into a pandas DataFrame
        data = pd.read_csv(filepath)
        app.logger.info("Data loaded successfully")
       
        target = next((col for col in ['target', 'label', 'churn'] if col in data.columns), 'target')

        preprocessor = Pipeline([
            ('cleaner', DataCleaner(strategy='mean', exclude_columns=None)),  
            ('transformer', DataTransformer(num_features=5, num_init_feats=40, exclude_columns=[target])),  # Example parameters
        ])
        data = preprocessor.transform(data)
        app.logger.info('Preprocessor loaded successfully')
        app.logger.info("Data preprocessed successfully")
        app.logger.info(data.columns)

        y = data[target]  # Assuming 'churn' is your target variable
        X = data.drop(columns=[target])  # Drop 'churn' column as it's the target variable
        # Split data into train and test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        app.logger.info("Data split into train and test sets")

        # Run machine learning pipeline
        results = run_pipeline(X_train, X_test, y_train, y_test)
        app.logger.info("Pipeline run successfully")
        app.logger.debug(f"Pipeline results: {results}")

        return jsonify(results), 200

    except Exception as e:
        app.logger.error(f"Error in running ML service: {e}")
        return jsonify({'error': str(e)}), 500

# Function to run the machine learning pipeline
def run_pipeline(X_train, X_test, y_train, y_test):
    try:
        # Task Dispatcher
        tasker = TaskDispatcher(int(len(X_train.columns) / 10))
        priorities, chunks = tasker.run(X_train)
        app.logger.info("TaskDispatcher executed successfully.")

        # Initialize Scheduler
        scheduler = Scheduler()
        pids = [i for i in range(10)]

        # Add processes to Scheduler
        for pid, priority, chunk in zip(pids, priorities, chunks):
            feat_selector = FeatureSelector(RandomForestClassifier, chunk, y_train, X_test, X_test.columns.tolist(), [5])
            process = Process(pid, priority, feat_selector)
            scheduler.add_process(process)
            app.logger.info(f"Added Process {pid} with priority {priority}")

        # Run Scheduler
        scheduler.run()
        app.logger.info("Scheduler executed successfully.")
        app.logger.debug(f"Scheduler results: {scheduler.results}")

        # Knapsack Transformation
        kn = Knapsack(scheduler.results['costs'], scheduler.results['values'], .1)
        final = kn.transform(X_train)
        app.logger.info("Knapsack transformation completed.")

        # Train RandomForestClassifier
        global rfa
        rfa = RandomForestClassifier()
        rfa.fit(final, y_train)
        app.logger.info("RandomForestClassifier trained successfully.")

        global final_features
        final_features = final.columns.tolist()

        # Make predictions on test set
        y_pred = rfa.predict(X_test[final.columns])

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')

        app.logger.info("Metrics calculated.")

        
        return {
            'accuracy': round(accuracy,5),
            'f1_score': round(f1,5),
            'precision': round(precision,5),
            'recall': round(recall,5)
        }

    except Exception as e:
        app.logger.error(f"Error in pipeline execution: {str(e)}")
        return {'error': str(e)}

# Route for evaluating manual input using the trained model
@app.route('/api/evaluate', methods=['POST'])
def evaluate_manual_input():
    try:
        global rfa, final_features

        if rfa is None or final_features is None:
            return jsonify({'error': 'Model not trained yet. Please upload a file and run pipeline first.'}), 400

        input_data = request.json  # Assuming JSON input like {"feature1": value1, "feature2": value2, ...}

        # Convert input data to DataFrame with selected features
        input_df = pd.DataFrame([input_data])[final_features]

        # Log input data for debugging
        app.logger.debug(f"Input data: {input_df}")

        # Make prediction using the trained model
        prediction = rfa.predict(input_df)
        prediction_probability = rfa.predict_proba(input_df)

        # Log prediction for debugging
        app.logger.debug(f"Prediction: {prediction},Prediction probablitiy: {prediction_probability} ")

        return jsonify({'prediction': prediction.tolist(), 'probability':prediction_probability.tolist()}), 200

    except Exception as e:
        app.logger.error(f"Error in evaluating manual input: {str(e)}")
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)