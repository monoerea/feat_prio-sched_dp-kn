import random
from joblib import load
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from tqdm import tqdm
import time
import threading
from Scheduler import Process, Scheduler
from Knapsack import Knapsack
from TaskDispatcher import TaskDispatcher
from FeatureSelector import FeatureSelector

# Example Usage
if __name__ == "__main__":
    # Load dataset and preprocess
    data = pd.read_csv('backend/data/dataset.csv')
    preprocessor = load('backend/pipeline/preprocessor.joblib')
    data = preprocessor.fit_transform(data)

    # Split data into train and test
    X = data.drop(columns=['churn'])
    y = data['churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    tasker = TaskDispatcher(int(len(X_train.columns)/10))

    priorities, chunks = tasker.run(X_train)

    # Define chunk columns and feature sizes
    chunk_columns = X_test.columns.tolist()
    feature_sizes = [5]  # Example list of feature sizes

    # Initialize scheduler and add processes
    scheduler = Scheduler()
    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()
    processes = []

    pids = [i for i in range(10)]

    for pid, priority, chunks in zip(pids,priorities, chunks):
        feat_selector = FeatureSelector(RandomForestClassifier, chunks, y_train, X_test, chunk_columns, feature_sizes)
        process = Process(pid, priority,  feat_selector)
        scheduler.add_process(process)
        print(f"Added Process {pid} with priority {priority}")

    # Wait for the scheduler thread to complete (optional)
    scheduler_thread.join()
    print(scheduler.results)
    print('Completed')

    kn = Knapsack(weights=scheduler.results['costs'], values=scheduler.results['values'], capacity=0.1)
    final=kn.transform(X_train)
    
    # Assuming `final` is the DataFrame with selected features from the knapsack algorithm
    # and `y_train` is the training target variable
    rfa = RandomForestClassifier()
    rfa.fit(final, y_train)

    # Make predictions on the test set using the selected features
    y_pred = rfa.predict(X_test[final.columns])

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')

    # Print the metrics
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")

    # Additional operations after scheduler completes (if needed)
