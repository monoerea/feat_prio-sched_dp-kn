import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class DataTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, num_init_feats=5, num_features=5, exclude_columns=None):
        self.num_init_feats = num_init_feats
        self.num_features = num_features
        self.exclude_columns = exclude_columns or ''

    def fit(self, X, y=None):
        return self  # Since no fitting is needed

    def transform(self, X):
        data = X.copy()
        data = self.dynamic_feature_generator(data, self.num_init_feats, self.num_features)
        return data

    def generate_new_feature(self, df, columns_to_combine, operation, operation_name):
        selected_data = df[columns_to_combine].apply(pd.to_numeric, errors='coerce')
        selected_data.fillna(0, inplace=True)
        new_feature_values = operation(selected_data.values.sum(axis=1))
        new_feature_values = np.clip(new_feature_values, -1e6, 1e6)  # Clipping to avoid extreme values
        new_feature_name = '_'.join(columns_to_combine) + '_' + operation_name
        return new_feature_values, new_feature_name

    def dynamic_feature_generator(self, data, num_initial_features=5, num_features=5):
        df = data.copy()

        operations = [
            lambda x: x + 2 * np.sin(np.clip(x, -1e6, 1e6)),
            lambda x: np.cos(np.clip(x, -1e6, 1e6)) / (np.abs(x) + 1e-6),
            lambda x: np.exp(np.clip(x, -700, 700)) / (np.sqrt(np.abs(x)) + 1e-6),
            lambda x: np.log(np.abs(x) + 1e-6),
            lambda x: np.sqrt(np.abs(x)),
            lambda x: np.tanh(np.clip(x, -1e6, 1e6)),
            lambda x: np.arcsin(np.clip(x, -1, 1)),
            lambda x: np.arccos(np.clip(x, -1, 1)),
            lambda x: np.tan(np.clip(x, -1e6, 1e6)),
            lambda x: np.clip(x, -1e6, 1e6)**2,
            lambda x: x * np.log(np.abs(x) + 1e-6),
            lambda x: np.abs(x) ** 0.25,
            lambda x: np.clip(x, -1, 1),
            lambda x: np.sign(x) * np.log(np.abs(x) + 1e-6),
            lambda x: np.arctan(np.clip(x, -1e6, 1e6)),
        ]
        
        operation_names = [
            'add_2sin', 'cos_div_abs', 'exp_div_sqrt', 'log_abs', 'sqrt_abs', 'tanh',
            'arcsin_clip', 'arccos_clip', 'tan', 'square', 'x_log_abs', 'abs_pow_0.25',
            'clip', 'sign_x_log_abs', 'arctan',
        ]

        initial_feature_values = {}
        for i in range(num_initial_features):
            columns_to_combine = np.random.choice(df.columns.difference(self.exclude_columns), size=np.random.randint(2, 10), replace=False)
            operation_idx = np.random.randint(len(operations))
            operation = operations[operation_idx]
            operation_name = operation_names[operation_idx]
            new_feature_values, new_feature_name = self.generate_new_feature(df, columns_to_combine, operation, operation_name)
            initial_feature_values[new_feature_name] = new_feature_values

        new_data = pd.DataFrame(initial_feature_values, index=df.index)

        features_generated = 0
        while df.isnull().any().any() and features_generated < num_features:
            columns_with_nan = df.columns[df.isnull().any()]

            for i in range(num_features):
                if len(columns_with_nan) > 0:
                    columns_to_combine = np.random.choice(columns_with_nan.drop(self.exclude_columns), size=np.random.randint(2, 10), replace=False)
                else:
                    columns_to_combine = np.random.choice(df.columns.drop(self.exclude_columns), size=np.random.randint(2, 10), replace=False)

                operation_idx = np.random.randint(len(operations))
                operation = operations[operation_idx]
                operation_name = operation_names[operation_idx]

                selected_data = df[columns_to_combine].apply(pd.to_numeric, errors='coerce')
                selected_data.fillna(selected_data.mean(), inplace=True)
                new_feature_values = operation(selected_data.values.sum(axis=1))
                new_feature_values = np.clip(new_feature_values, -1e6, 1e6)  # Clipping to avoid extreme values
                new_feature_name = '_'.join(columns_to_combine) + '_' + operation_name

                df[new_feature_name] = new_feature_values
                features_generated += 1

                if features_generated >= num_features:
                    break

        # Clip to avoid infinity or very large values
        df = df.clip(lower=-1e6, upper=1e6)

        self.data = pd.concat([df, new_data], axis=1)

        return self.data
