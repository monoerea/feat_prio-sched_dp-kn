from joblib import load
import pandas as pd

class Knapsack:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity

    @staticmethod
    def heuristic_knapsack(weights, values, capacity):
        n = len(weights)
        capacity = int(capacity * 100)  # Convert capacity to an integer scale
        weights = [int(w * 100) for w in weights]  # Convert weights to the same scale
        k = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i - 1] <= w:
                    k[i][w] = max(values[i - 1] + k[i - 1][w - weights[i - 1]], k[i - 1][w])
                else:
                    k[i][w] = k[i - 1][w]
        
        return k
    def select_features_using_knapsack(self, weights, values, capacity):
        print(f"Number of weights: {len(weights)}, Number of values: {len(values)}, Capacity: {capacity}")
        k = self.heuristic_knapsack(weights, values, capacity)
        n = len(weights)
        selected_items = []
        res = k[n][int(capacity * 100)]
        w = int(capacity * 100)
        
        for i in range(n, 0, -1):
            print(f"Current i: {i}, res: {res}, w: {w}")
            if res <= 0:
                break
            if res == k[i - 1][w]:
                continue
            else:
                selected_items.append(i - 1)
                res = res - values[i - 1]
                if i > 1 and w >= int(weights[i - 1] * 100):
                    w = w - int(weights[i - 1] * 100)
        
        return selected_items
    def transform(self, X):
            selected_features_indices = self.select_features_using_knapsack(self.weights, self.values, self.capacity)
            selected_features = [X.columns[i] for i in selected_features_indices]

            print(f'Selected features: {selected_features}')
            print(f'Total computational cost: {sum(self.weights[i] for i in selected_features_indices)}')
            print(f'Total value (accuracy): {sum(self.values[i] for i in selected_features_indices)}')
            print(f'Avg Feature Importance Value: {sum(self.values[i] for i in selected_features_indices) / len(selected_features_indices)}')

            return X[selected_features]

if __name__ == '__main__':
    # Load data and preprocess as needed
    print("Loading data...")
    data = pd.read_csv('backend/data/dataset.csv')
    print("Data loaded successfully.")
    
    print("Loading preprocessor...")
    preprocessor = load('backend/scripts/preprocessor.joblib')
    print("Preprocessor loaded successfully.")
    
    print("Transforming data...")
    data = preprocessor.fit_transform(data)
    print("Data transformed successfully.")
    
    # Assuming 'churn' is your target variable
    y = data['churn']
    X = data.drop(columns=['churn'])  # Assuming 'churn' column is dropped for features

    # Example costs and accuracies for features (replace with actual values)
    # Replace with your actual feature costs and accuracies
    weights = [0.1] * len(X.columns)  # Example costs for each feature
    values = [0.8] * len(X.columns)   # Example accuracies for each feature
    capacity = 0.8  # Example capacity (time-based)

    print("Initializing Knapsack...")
    # Initialize and use Knapsack class
    knapsack_process = Knapsack(weights=weights, values=values, capacity=capacity)
    print("Knapsack initialized.")

    print("Transforming features...")
    selected_features = knapsack_process.transform(X)
    print("Feature transformation complete.")

    print("Selected Features:", selected_features.columns)
