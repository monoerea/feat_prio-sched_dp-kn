import heapq
from joblib import load
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tqdm import tqdm
import time
class FeatureSelector:
    def __init__(self, model, X_train, y_train, X_test, chunk_columns, feature_sizes):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.chunk_columns = chunk_columns
        self.feature_sizes = feature_sizes
        self.best_model = None
        self.best_features = None
        self.best_accuracy = 0.0
        self.all_features = None
        self.accuracies = []
        self.costs = []  # Initialize dictionary to store fitting times for each feature
        self.results = []

    def run(self):
        self.all_features = self.X_train.columns.tolist()

        # Calculate fitting times for all individual features once
        self.calculate_all_feature_fitting_times()

        pbar_feature_sizes = self.initialize_progress_bar(self.feature_sizes)
        
        for k in pbar_feature_sizes:
            remaining_features = self.all_features.copy()

            self.evaluate_feature_elimination(remaining_features, k)

        # Close the progress bar for feature sizes
        pbar_feature_sizes.close()

        # best_feature_costs = [self.costs[feature] for feature in self.best_features]
        # best_feature_importances = self.get_feature_importances(self.X_train[self.best_features])
        # # Apply knapsack selection on the best features
        # selected_features = self.apply_knapsack_selection()

        return self.costs, self.get_feature_importances(self.X_train[self.best_features])
    def initialize_progress_bar(self, feature_sizes):
        return tqdm(feature_sizes, desc="Feature Sizes", ncols=100)

    def evaluate_feature_elimination(self, remaining_features, k, step=1):
        """
        Evaluate feature elimination process.
        """
        pbar_feature_elimination = tqdm(total=len(self.all_features), desc="Feature Elimination", leave=False, postfix="")
        
        while len(remaining_features) >= k:
            pbar_feature_elimination.update(step)

            X_train_selected = self.X_train[remaining_features]

            performance, n_features = self.evaluate_feature_performance(X_train_selected, self.y_train)

            if performance > self.best_accuracy:
                self.best_accuracy = performance
                self.best_features = remaining_features.copy()
                self.accuracies.append(performance)

            importances = self.get_feature_importances(X_train_selected)
            least_important_feature_indices = np.argsort(importances)[:step]
            least_important_features = [remaining_features[i] for i in least_important_feature_indices]

            for feature in least_important_features:
                remaining_features.remove(feature)
                
            self.update_progress_bar(pbar_feature_elimination, k, remaining_features)

        pbar_feature_elimination.close()

        self.results.append({
            'Feature_Size': k,
            'Accuracies': self.accuracies,
            'Best_Accuracy': self.best_accuracy,
            'Best_Features': self.best_features,
            'Features': remaining_features,
            'Feature_Importances': importances.tolist(),  # Convert numpy array to list for serialization
            #'Costs': [self.costs[feature] for feature in self.best_features]  # Store fitting times for the best features
        })

    def evaluate_feature_performance(self, X_train_selected, y_train):
        """
        Evaluate feature performance (accuracy).
        """
        model = self.model()
        model.fit(X_train_selected, y_train)
        y_pred = model.predict(X_train_selected)
        accuracy = accuracy_score(y_train, y_pred)
        return accuracy, X_train_selected.shape[1]

    def calculate_all_feature_fitting_times(self):
        """
        Calculate and store fitting time for each feature.
        """
        for feature in self.X_train.columns:
            
            model = self.model()
            model.fit(self.X_train[[feature]], self.y_train)
            start_time = time.time()
            model.predict(self.X_test[[feature]])
            fitting_time = time.time() - start_time
            self.costs.append(fitting_time)

    def get_feature_importances(self, X_train_selected):
        """
        Get feature importances from the model.
        """
        model = self.model()
        model.fit(X_train_selected, self.y_train)
        importances = model.feature_importances_
        return importances

    def update_progress_bar(self, pbar, k, remaining_features):
        """
        Update progress bar with current status.
        """
        pbar.set_postfix_str(f"Accuracies: {self.accuracies[-k:]}, Mean: {np.mean(self.accuracies[-k:])}, Features: {remaining_features}")
        pbar.total = len(remaining_features)
        pbar.refresh()

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
