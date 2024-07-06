import threading
import time

from joblib import load
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from backend.pipeline import FeatureSelector
class PriorityQueue:
    """
    A simple priority queue implementation using a list.
    """
    def __init__(self):
        self._queue = []

    def enqueue(self, priority, item):
        """
        Push an item with a priority into the queue.
        """
        for index, (p, _) in enumerate(self._queue):
            if p > priority:
                self._queue.insert(index, (priority, item))
                return
        self._queue.append((priority, item))

    def dequeue(self):
        """
        Pop the item with the highest priority from the queue.
        """
        if self.empty():
            raise IndexError("pop from empty queue")
        return self._queue.pop(0)[1]

    def peek(self):
            return self._queue[0]
    def empty(self):
        """
        Check if the queue is empty.
        """
        return len(self._queue) == 0
    
import time

class Process:
    def __init__(self, pid, priority, burst_time, process):
        self.pid = pid
        self.priority = priority
        self.burst_time = burst_time
        self.process = process

    def run(self):
        start_time = time.time()
        results = self.process.run()
        self.burst_time -= time.time() - start_time  # Decrease burst_time by elapsed real time
        return results

class Scheduler:
    def __init__(self):
        self.time = 0
        self.waiting_time = {}
        self.turn_around_time = {}
        self.process_queue = PriorityQueue()
        self.running = False
        self.results = {'costs': [], 'values': []}

    def add_process(self, process):
        self.process_queue.enqueue(process.priority, process)

    def run(self):
        self.running = True
        time.sleep(1)
        while self.running or not self.process_queue.empty():
            if not self.process_queue.empty():
                current_process = self.process_queue.dequeue()
                print(f"Time {self.time}: Process {current_process.pid} with priority {current_process.priority} is running")

                start_time = time.time()
                elapsed_time = 0
                results = ()
                while elapsed_time < current_process.burst_time and len(results)==0:
                    results = current_process.run()
                    print(results)
                    # Increment time and elapsed_time
                    self.time += 1
                    elapsed_time = time.time() - start_time

                    # Check for higher priority processes
                    if not self.process_queue.empty() and self.process_queue.peek()[0] < current_process.priority:
                        print(f"Process {current_process.pid} preempted due to higher priority.")
                        self.process_queue.enqueue(current_process.priority, current_process)
                        return

                costs, values = results
                self.results['costs'].extend(costs)
                self.results['values'].extend(values)
                print(len(self.results['costs']) == len(self.results['values']))
                self.turn_around_time[current_process.pid] = elapsed_time
                self.waiting_time[current_process.pid] = max(0, self.turn_around_time[current_process.pid] - current_process.burst_time)

                print(f"Process {current_process.pid} finished. Turnaround Time: {self.turn_around_time[current_process.pid]}, Waiting Time: {self.waiting_time[current_process.pid]}")

            else:
                self.stop()

        self.print_statistics()
        return self.results

    def stop(self):
        self.running = False

    def print_statistics(self):
        print("\nProcess Execution Complete.\n")
        for pid in self.waiting_time:
            print(f"Process {pid}: Waiting Time = {self.waiting_time[pid]}, Turnaround Time = {self.turn_around_time[pid]}")
        
        if self.waiting_time:
            avg_waiting_time = sum(self.waiting_time.values()) / len(self.waiting_time)
        else:
            avg_waiting_time = 0

        if self.turn_around_time:
            avg_turnaround_time = sum(self.turn_around_time.values()) / len(self.turn_around_time)
        else:
            avg_turnaround_time = 0

        print(f"\nAverage Waiting Time: {avg_waiting_time}")
        print(f"Average Turnaround Time: {avg_turnaround_time}")
if __name__ == "__main__":
    #Load dataset and preprocess
    data = pd.read_csv('backend/data/dataset.csv')
    preprocessor = load('backend/scripts/preprocessor.joblib')
    data = preprocessor.fit_transform(data)
    y = data['churn']  # Assuming 'churn' is your target variable
    X = data.drop(columns=['churn'])  # Assuming 'churn' column is dropped for features
    feature_sizes = [100]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create the scheduler
    scheduler = Scheduler()
    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()

    # Simulate adding processes dynamically in a loop
    try:
        for i in range(2):
            time.sleep(10)  # Simulate a 10-second interval before adding a new process
            new_pid = len(scheduler.waiting_time) + 1
            new_priority = 2  # Example priority (replace with actual logic)
            feature_selector = FeatureSelector(model=RandomForestClassifier, cv=5)
            feature_selector.run(X_train=X_train, y_train=y_train, feature_sizes=feature_sizes, step=50)
            new_process = Process(new_pid, new_priority, feature_selector)
            scheduler.add_process(new_process)
            print(f"Added Process {new_pid} with priority {new_priority} and burst time {new_process.burst_time}")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Stopping scheduler...")
        scheduler.stop_periodic_process_arrival()
        scheduler_thread.join()
        print("Scheduler stopped.")
