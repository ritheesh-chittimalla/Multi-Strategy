# algorithms/greedy.py
import math
from typing import List, Tuple

def euclidean(a,b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def tsp_nearest_neighbor(points: List[Tuple[float,float]]):
    if not points: return [], 0.0
    n = len(points)
    visited = [False]*n
    tour = [0]
    visited[0]=True
    cur = 0
    cost = 0.0
    for _ in range(n-1):
        best = None; bestd = float('inf')
        for j in range(n):
            if not visited[j]:
                d = euclidean(points[cur], points[j])
                if d < bestd:
                    bestd = d; best = j
        tour.append(best); visited[best]=True; cost += bestd; cur = best
    cost += euclidean(points[cur], points[tour[0]])
    tour.append(tour[0])
    return tour, cost

def knapsack_greedy(items, capacity):
    # items: list of (id, value, weight)
    items_sorted = sorted(items, key=lambda it: it[1]/it[2], reverse=True)
    total = 0
    picked = []
    cap = capacity
    for id_, val, wt in items_sorted:
        if wt <= cap:
            picked.append(id_)
            total += val
            cap -= wt
    return picked, total
