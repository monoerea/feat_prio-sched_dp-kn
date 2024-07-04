import pandas as pd
import numpy as np


class TaskDispatcher:
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size
        self.chunks = None  # Placeholder for storing chunks after chunking

    def run(self, df):
        """
        Method to run the task dispatcher, which includes chunking and computing priorities.
        """
        self.chunks = self.chunker(df, self.chunk_size)
        priorities = []
        
        min_load_metric = float('inf')  # Initialize with a large number
        
        # Calculate priorities
        for chunk in self.chunks:
            load_metric = self.compute_load_metric(chunk)
            
            # Update minimum load metric encountered
            if load_metric < min_load_metric:
                min_load_metric = load_metric
            
            # Determine priority based on load metric and number of columns
            priority = len(chunk.columns) / min_load_metric
            
            priorities.append(priority)
        
        # Rank priorities from 1 to 10
        ranked_priorities = []
        sorted_indices = sorted(range(len(priorities)), key=lambda k: priorities[k])
        num_chunks = len(sorted_indices)
        rank_step = num_chunks // 10  # Calculate the step size for each rank
        
        current_rank = 1
        for i, index in enumerate(sorted_indices):
            rank = current_rank
            if i + 1 < len(sorted_indices) and priorities[sorted_indices[i + 1]] > priorities[index]:
                current_rank += 1
            ranked_priorities.append(rank)
        
        return ranked_priorities, self.chunks

    
    def chunker(self, df, chunk_size):
        """
        Chunker function that generates chunks of data based on chunk_size.
        """
        # Generate chunks of data based on chunk_size
        chunks = [df.iloc[:, i:i + chunk_size] for i in range(0, len(df.columns), chunk_size)]
        
        return chunks
    
    def compute_load_metric(self, chunk):
        """
        Function to compute the load metric for a chunk of data.
        Modify this function based on your specific load computation requirements.
        """
        # Example: Compute load metric based on data characteristics
        # Example factors influencing load metric:
        
        # 1. Standard deviation of data values
        std_dev = np.std(chunk.values)
        
        # 2. Range of data values (difference between max and min)
        data_range = np.max(chunk.values) - np.min(chunk.values)
        
        # 3. Complexity of operations (e.g., mean computation)
        complexity_factor = np.mean(chunk).sum()  # Example of a computational factor
        
        # Combine factors to compute the load metric
        load_metric = std_dev + data_range + complexity_factor
        
        return load_metric
