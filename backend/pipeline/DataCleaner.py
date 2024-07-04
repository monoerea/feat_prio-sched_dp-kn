import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
class LabelEncoder:
    def __init__(self):
        self.data = None
        
    def find_categorical_columns(self, data):
        return data.select_dtypes(include=['object', 'category']).columns.tolist()

    def one_hot_encoder(self, data, columns_to_encode):
        for column in columns_to_encode:
            data.loc[:, column] = pd.factorize(data[column])[0]
        return data
    
    def get_data(self):
        return self.data
    
    def transform(self, X):
        categorical_cols = self.find_categorical_columns(X)
        self.data = self.one_hot_encoder(X.copy(), categorical_cols)
        return self.data
class DataCleaner(BaseEstimator, TransformerMixin):
    def __init__(self, strategy='mean', exclude_columns=None):
        self.strategy = strategy
        self.exclude_columns = exclude_columns if exclude_columns is not None else []  # Ensure initialization
        self.num_imputer = SimpleImputer(strategy=self.strategy)
    
    def transform(self, X):
        data = X.copy()
        
        # Handle missing values using fitted imputers (if they were fitted)
        num_cols = data.select_dtypes(include=['int64', 'float64']).columns
        if not num_cols.empty:
            self.num_imputer.fit(data[num_cols])
            data.loc[:, num_cols] = self.num_imputer.transform(data[num_cols])
        
        # Exclude specified columns from processing
        # columns_to_process = [col for col in data.columns if col not in self.exclude_columns]
        # data_to_process = data[columns_to_process].copy()  # Use .copy() to avoid SettingWithCopyWarning
        
        # Remove duplicates (if needed)
        data_cleaned = data.drop_duplicates()

        # Example: Assuming LabelEncoder is a custom utility
        encoder = LabelEncoder()
        encoded_data = encoder.transform(data_cleaned)
        
        return encoded_data
    
    def fit(self, X, y=None):
        # Fit numerical imputer on numerical columns
        num_cols = X.select_dtypes(include=['int64', 'float64']).columns
        if not num_cols.empty:
            self.num_imputer.fit(X[num_cols])

        return self
    
    def get_params(self, deep=True):
        return {
            'strategy': self.strategy,
            'exclude_columns': self.exclude_columns
        }

    def set_params(self, **params):
        if 'strategy' in params:
            self.strategy = params['strategy']
        if 'exclude_columns' in params:
            self.exclude_columns = params['exclude_columns']

        return self
