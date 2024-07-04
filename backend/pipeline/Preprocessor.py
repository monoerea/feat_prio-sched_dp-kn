import os
import pandas as pd
from joblib import dump
from sklearn.pipeline import Pipeline
from DataCleaner import DataCleaner
from DataTransformer import DataTransformer

if __name__ == "__main__":
    try:
        # Example data loading
        data = pd.read_csv('backend/data/dataset.csv')
        y = data['churn']  # Assuming 'churn' is your target variable
        X = data.drop(columns=['churn'])  # Drop 'churn' column as it's the target variable

        # Define the pipeline components
        preprocessor = Pipeline([
            ('cleaner', DataCleaner(strategy='mean', exclude_columns=None)),  
            ('transformer', DataTransformer(num_features=40, num_init_feats=40, exclude_columns=['churn'])),  # Example parameters
        ])


        # Fit and transform data with the preprocessor pipeline
        X_processed = preprocessor.fit_transform(data)
        print(X_processed.columns)
        # Define path to save the preprocessor model
        current_dir = os.path.dirname(os.path.abspath(__file__))
        preprocessor_path = os.path.join(current_dir, 'preprocessor.joblib')

        # Save the preprocessor model to the specified path
        dump(preprocessor, preprocessor_path)
        print(f"Preprocessor saved successfully to {preprocessor_path}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
