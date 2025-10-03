# algorithms/divide_and_conquer.py
from typing import List, Tuple
import math, itertools, bisect, time

def euclidean(a,b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def tour_cost(points, tour):
    c=0.0
    if not tour: return 0.0
    for i in range(len(tour)-1):
        c += euclidean(points[tour[i]], points[tour[i+1]])
    return c

# simple partition + merge tsp as heuristic
def tsp_divide_and_conquer(points: List[Tuple[float,float]], max_leaf: int = 8, time_limit=3.0):
    start = time.perf_counter()
    n = len(points)
    if n==0: return [], 0.0
    idxs = list(range(n))
    def greedy_subsolve(idxs_local):
        if not idxs_local: return [], 0.0
        pts = [points[i] for i in idxs_local]
        # reuse greedy
        from algorithms.greedy import tsp_nearest_neighbor
        tour_local, cost = tsp_nearest_neighbor(pts)
        # map back to global indices
        if tour_local:
            return [idxs_local[i] for i in tour_local], cost
        return [], 0.0
    def recurse(idxs_subset):
        if time.perf_counter() - start > time_limit:
            return greedy_subsolve(idxs_subset)
        m = len(idxs_subset)
        if m <= max_leaf:
            return greedy_subsolve(idxs_subset)
        pts_sorted = sorted(idxs_subset, key=lambda i: points[i][0])
        mid = m//2
        left = pts_sorted[:mid]; right = pts_sorted[mid:]
        tourL, costL = recurse(left); tourR, costR = recurse(right)
        merged, merged_cost = splice_tours(points, tourL, tourR)
        return merged, merged_cost
    final_tour, final_cost = recurse(idxs)
    if final_tour and final_tour[-1] != final_tour[0]:
        final_tour.append(final_tour[0])
    return final_tour, final_cost

def splice_tours(points, tourA, tourB):
    if not tourA: return tourB, tour_cost(points, tourB)
    if not tourB: return tourA, tour_cost(points, tourA)
    A = tourA[:-1]; B = tourB[:-1]
    best = None; bestc = float('inf')
    for i in range(len(A)):
        a1 = A[i]; a2 = A[(i+1)%len(A)]
        for j in range(len(B)):
            b1 = B[j]; b2 = B[(j+1)%len(B)]
            new = []
            new.extend(A[:i+1])
            new.extend(B[j+1:]+B[:j+1])
            new.extend(A[i+1:])
            if new[0] != new[-1]:
                new.append(new[0])
            c = tour_cost(points, new)
            if c < bestc:
                bestc = c; best = new
    if best is None:
        best = A + B + [A[0]]
        bestc = tour_cost(points, best)
    return best, bestc

def knapsack_meet_in_middle(items, capacity):
    n = len(items)
    if n==0: return [], 0
    mid = n//2
    left = items[:mid]; right = items[mid:]
    def subsets(arr):
        res=[]
        m=len(arr)
        for mask in range(1<<m):
            w=0; v=0; picked=[]
            for i in range(m):
                if (mask>>i)&1:
                    id_, val, wt = arr[i]
                    w += wt; v += val; picked.append(id_)
            if w <= capacity:
                res.append((w,v,picked))
        return res
    L = subsets(left); R = subsets(right)
    R.sort(key=lambda x:(x[0], -x[1]))
    Rf=[]; maxv=-1
    for w,v,p in R:
        if v>maxv:
            Rf.append((w,v,p)); maxv=v
    import bisect
    Rw = [x[0] for x in Rf]
    Rv = [x[1] for x in Rf]
    bestv=0; bestset=[]
    for wL, vL, pL in L:
        rem = capacity - wL
        idx = bisect.bisect_right(Rw, rem) - 1
        if idx >=0:
            tot = vL + Rv[idx]
            if tot > bestv:
                bestv = tot; bestset = pL + list(Rf[idx][2])
        else:
            if vL > bestv:
                bestv = vL; bestset = pL[:]
    return bestset, bestv
