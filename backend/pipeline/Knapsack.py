import math
import pandas as pd
import random

class Knapsack:
    def __init__(self, weights, values, capacity):
        self.weights = [math.floor(w * 100) for w in weights]  # Convert weights to the same scale
        self.values = values
        self.capacity = int(capacity * 100)  # Convert capacity to an integer scale
        self.n = len(weights)
        self.t = [[-1 for _ in range(self.capacity + 1)] for _ in range(self.n + 1)]

    def heuristic_knapsack(self, weights, values, capacity, n):
        # Base condition
        if n == 0 or capacity == 0:
            return 0
        
        # If the subproblem is already solved, return the stored result
        if self.t[n][capacity] != -1:
            return self.t[n][capacity]

        # Choice diagram code
        if weights[n - 1] <= capacity:
            self.t[n][capacity] = max(
                values[n - 1] + self.heuristic_knapsack(weights, values, capacity - weights[n - 1], n - 1),
                self.heuristic_knapsack(weights, values, capacity, n - 1)
            )
        else:
            self.t[n][capacity] = self.heuristic_knapsack(weights, values, capacity, n - 1)

        return self.t[n][capacity]

    def select_features_using_knapsack(self, X):
        # Trace back the solution
        res = self.t[self.n][self.capacity]
        selected_items = []
        for i in range(self.n, 0, -1):
            if res <= 0:
                break
            if res == self.t[i-1][self.capacity]:
                continue
            else:
                selected_items.append(i-1)
                res = res - self.values[i-1]
                self.capacity = self.capacity - self.weights[i-1]

        selected_items.reverse()
        selected_features = [X.columns[i] for i in selected_items]
        transformed_data = X[selected_features] if selected_items else pd.DataFrame()

        print(f'Selected features using knapsack: {selected_features}')
        if selected_items:
            print(f'Total computational cost: {sum(self.weights[i] for i in selected_items)/100}')  # Convert back to original scale
            print(f'Total value (accuracy): {sum(self.values[i] for i in selected_items)}')
            print(f'Avg Feature Importance Value: {sum(self.values[i] for i in selected_items) / len(selected_items)}')
        else:
            print("No features were selected.")

        return transformed_data, selected_features

    def transform(self, X):
        # Example heuristic knapsack selection
        heuristic_value = self.heuristic_knapsack(self.weights, self.values, self.capacity, self.n)

        print(f'Heuristic knapsack value: {heuristic_value}')

        # Example dynamic programming knapsack selection
        dp_transformed_data, dp_selected_features = self.select_features_using_knapsack(X)

        return dp_transformed_data

def main():
    # Example usage
    # Load data and preprocess as needed
    print("Loading data...")
    data = pd.read_csv('backend/data/dataset.csv')
    print("Data loaded successfully.")
    
    # Assuming 'churn' is your target variable
    y = data['churn']
    X = data.drop(columns=['churn'])  # Assuming 'churn' column is dropped for features

    # Randomize costs and accuracies for features
    num_features = len(X.columns)
    weights = [random.uniform(0.1, 1.0) for _ in range(num_features)]
    values = [random.uniform(0.5, 1.0) for _ in range(num_features)]
    capacity = .1#random.uniform(0.5, 1.0) * num_features  # Random capacity based on number of features

    print(f"Randomized weights: {weights}")
    print(f"Randomized values: {values}")
    print(f"Randomized capacity: {capacity}")

    # Initialize and use Knapsack class
    knapsack_process = Knapsack(weights=weights, values=values, capacity=capacity)
    print("Knapsack initialized.")

    print("Transforming features using different methods...")
    dp_transformed_data = knapsack_process.transform(X)
    print("Feature transformation complete.")

    print("Selected Features (Dynamic Programming):")
    print(dp_transformed_data.columns)

if __name__ == '__main__':
    main()
