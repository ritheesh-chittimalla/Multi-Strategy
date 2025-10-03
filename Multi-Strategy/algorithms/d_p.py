# algorithms/d_p.py
from typing import List, Tuple
import math, itertools

def knapsack_dp(items: List[Tuple[str,int,int]], capacity: int):
    # items: (id, value, weight)
    n = len(items)
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1, n+1):
        _, val, wt = items[i-1]
        for w in range(capacity+1):
            dp[i][w] = dp[i-1][w]
            if wt <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-wt] + val)
    w = capacity
    picked = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            picked.append(items[i-1][0])
            w -= items[i-1][2]
    picked.reverse()
    return picked, dp[n][capacity]

def tsp_held_karp(points):
    n = len(points)
    if n == 0: return [], 0.0
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx=points[i][0]-points[j][0]; dy=points[i][1]-points[j][1]
            dist[i][j] = math.hypot(dx,dy)
    C = {}
    for k in range(1, n):
        C[(1<<k, k)] = dist[0][k]
    for s in range(2, n):
        for subset in itertools.combinations(range(1,n), s):
            mask=0
            for x in subset: mask |= 1<<x
            for j in subset:
                prev = mask ^ (1<<j)
                best = float('inf')
                for k in subset:
                    if k==j: continue
                    best = min(best, C[(prev,k)] + dist[k][j])
                C[(mask,j)] = best
    full = (1<<n) - 1
    best_cost = float('inf'); last = None
    for j in range(1,n):
        cost = C[(full ^ 1, j)] + dist[j][0]
        if cost < best_cost:
            best_cost = cost; last = j
    # reconstruct path (simple approximate)
    # here we return only cost and None tour for large n to avoid complexity
    return None, best_cost
