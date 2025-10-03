# algorithms/branch_and_bound.py
import heapq
from typing import List, Tuple

class Node:
    def __init__(self, level, value, weight, bound, taken):
        self.level = level; self.value = value; self.weight = weight; self.bound = bound; self.taken = taken
    def __lt__(self, other):
        return self.bound > other.bound

def bound(node, items, capacity):
    if node.weight >= capacity: return 0
    val_bound = node.value
    j = node.level + 1
    totw = node.weight
    n = len(items)
    while j < n and totw + items[j][2] <= capacity:
        totw += items[j][2]; val_bound += items[j][1]; j += 1
    if j < n:
        val_bound += (capacity - totw) * (items[j][1] / items[j][2])
    return val_bound

def knapsack_bnb(items: List[Tuple[str,int,int]], capacity: int):
    items_sorted = sorted(items, key=lambda it: it[1]/it[2], reverse=True)
    n = len(items_sorted)
    Q = []
    v = Node(-1, 0, 0, 0.0, [])
    v.bound = bound(v, items_sorted, capacity)
    heapq.heappush(Q, v)
    max_value = 0; best_taken = []
    while Q:
        v = heapq.heappop(Q)
        if v.bound <= max_value:
            continue
        u_level = v.level + 1
        if u_level < n:
            wt = v.weight + items_sorted[u_level][2]
            val = v.value + items_sorted[u_level][1]
            taken = v.taken + [items_sorted[u_level][0]]
            u = Node(u_level, val, wt, 0.0, taken)
            if wt <= capacity and val > max_value:
                max_value = val; best_taken = taken[:]
            u.bound = bound(u, items_sorted, capacity)
            if u.bound > max_value:
                heapq.heappush(Q, u)
            u2 = Node(u_level, v.value, v.weight, 0.0, v.taken[:])
            u2.bound = bound(u2, items_sorted, capacity)
            if u2.bound > max_value:
                heapq.heappush(Q, u2)
    return best_taken, max_value

# A simple branch & bound TSP placeholder using naive B&B (works for very small n)
def tsp_branch_bound(points, time_limit=5.0):
    # Convert to distance matrix then simple best-first exploring partial tours
    import math, time, heapq
    n = len(points)
    if n==0: return [], 0.0
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = points[i][0]-points[j][0]; dy=points[i][1]-points[j][1]
            dist[i][j] = math.hypot(dx,dy)
    start = time.perf_counter()
    # priority queue: (cost_so_far, path, visited_set)
    pq = [(0.0, [0], {0})]
    best = float('inf'); best_path = []
    while pq and time.perf_counter()-start < time_limit:
        cost, path, visited = heapq.heappop(pq)
        if len(path) == n:
            total = cost + dist[path[-1]][0]
            if total < best:
                best = total; best_path = path + [0]
            continue
        for nxt in range(n):
            if nxt in visited: continue
            newcost = cost + dist[path[-1]][nxt]
            if newcost >= best: continue
            heapq.heappush(pq, (newcost, path + [nxt], visited | {nxt}))
    return best_path, best
