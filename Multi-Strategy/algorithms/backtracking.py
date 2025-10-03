# algorithms/backtracking.py
import math, time
from typing import List, Tuple

def tsp_backtracking(points: List[Tuple[float,float]], time_limit=5.0):
    n = len(points)
    if n==0: return [], 0.0
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx=points[i][0]-points[j][0]; dy=points[i][1]-points[j][1]
            dist[i][j] = math.hypot(dx,dy)
    best_cost = float('inf'); best_tour = []
    visited = [False]*n; visited[0]=True; path=[0]
    start = time.perf_counter()
    def dfs(curr, cost):
        nonlocal best_cost, best_tour
        if time.perf_counter() - start > time_limit:
            return
        if len(path)==n:
            total = cost + dist[curr][0]
            if total < best_cost:
                best_cost = total; best_tour = path[:] + [0]
            return
        for nxt in range(1,n):
            if not visited[nxt]:
                nc = cost + dist[curr][nxt]
                if nc >= best_cost: continue
                visited[nxt]=True; path.append(nxt)
                dfs(nxt, nc)
                path.pop(); visited[nxt]=False
    dfs(0, 0.0)
    return best_tour, best_cost

def knapsack_backtracking(items: List[Tuple[str,int,int]], capacity: int, time_limit=5.0):
    start = time.perf_counter()
    n = len(items)
    best_val = 0; best_set = []
    def dfs(i, cw, cv, chosen):
        nonlocal best_val, best_set
        if time.perf_counter() - start > time_limit:
            return
        if i==n:
            if cv > best_val:
                best_val = cv; best_set = chosen[:]
            return
        dfs(i+1, cw, cv, chosen)
        id_, val, wt = items[i]
        if cw + wt <= capacity:
            chosen.append(id_); dfs(i+1, cw+wt, cv+val, chosen); chosen.pop()
    dfs(0,0,0,[])
    return best_set, best_val
