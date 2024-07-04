

def heuristic_knapsack(weights, values, capacity, n):
    capacity = int(capacity * 1000)  # Convert capacity to integer and scale
    weights = [int(w * 1000) for w in weights]  # Scale weights to integers for more granularity
    t = [[-1 for i in range(capacity + 1)] for j in range(n + 1)]

    if n == 0 or capacity == 0:
        return 0
    if t[n][capacity] != -1:
        return t[n][capacity]

    # choice diagram code
    if weights[n-1] <= capacity:
        t[n][capacity] = max(
            values[n-1] + heuristic_knapsack(
                weights, values, capacity-weights[n-1], n-1),
            heuristic_knapsack(weights, values, capacity, n-1))
        return t[n][capacity]
    elif weights[n-1] > capacity:
        t[n][capacity] = heuristic_knapsack(weights, values, capacity, n-1)
        return t

def select_features_using_knapsack(weights, values, capacity):
    n = len(weights)
    k = heuristic_knapsack(weights, values, capacity, n)
    
    # Backtracking to find the selected items
    selected_items = []
    res = k[n][int(capacity * 1000)]
    w = int(capacity * 1000)
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == k[i-1][w]:
            continue
        else:
            selected_items.append(i-1)
            res = res - values[i-1]
            w = w - int(weights[i-1] * 1000)
    
    return selected_items