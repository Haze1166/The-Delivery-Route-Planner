def solve(weights, priorities, capacity):
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    priorities[i-1] + dp[i-1][w - weights[i-1]],
                    dp[i-1][w]
                )
            else:
                dp[i][w] = dp[i-1][w]

    max_priority_val = dp[n][capacity]
    included_items_indices = []
    w = capacity
    for i in range(n, 0, -1):
        if max_priority_val <= 0: break
        if max_priority_val == dp[i-1][w]: continue
        else:
            included_items_indices.append(i-1)
            max_priority_val -= priorities[i-1]
            w -= weights[i-1]

    included_items_indices.reverse()
    return dp[n][capacity], included_items_indices