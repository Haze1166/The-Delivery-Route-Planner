# algorithms/knapsack.py

def solve(weights, values, capacity):
    """
    Solves the 0/1 Knapsack problem using Dynamic Programming.
    Returns the maximum value and the list of indices of items included.
    """
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Build table dp[][] in bottom-up manner
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # If the current item's weight is less than or equal to the current capacity
            if weights[i-1] <= w:
                # Decide whether to include the item or not
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w - weights[i-1]], # Include item
                    dp[i-1][w]                                 # Don't include item
                )
            else:
                # If the item's weight is more than the capacity, it cannot be included
                dp[i][w] = dp[i-1][w]

    # Backtrack to find which items were included
    max_value = dp[n][capacity]
    included_items_indices = []
    w = capacity
    for i in range(n, 0, -1):
        if max_value <= 0:
            break
        if max_value == dp[i-1][w]:
            continue
        else:
            # This item was included
            included_items_indices.append(i-1)
            max_value -= values[i-1]
            w -= weights[i-1]

    included_items_indices.reverse()
    return dp[n][capacity], included_items_indices