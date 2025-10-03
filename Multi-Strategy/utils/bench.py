# utils/bench.py
import time, statistics
from algorithms import greedy, d_p, backtracking, branch_and_bound, divide_and_conquer
from utils.datasets import load_tsp, load_knapsack, load_graph

def run_single(problem, method, dataset, runs=3):
    times=[]; result=None
    for _ in range(runs):
        start = time.perf_counter()
        if problem=='tsp':
            pts = load_tsp(dataset)
            if method=='greedy':
                out = greedy.tsp_nearest_neighbor(pts)
            elif method=='d_p':
                out = d_p.tsp_held_karp(pts)
            elif method=='backtracking':
                out = backtracking.tsp_backtracking(pts, time_limit=2.0)
            elif method=='branch_and_bound':
                out = branch_and_bound.tsp_branch_bound(pts, time_limit=2.0)
            elif method=='divide_and_conquer':
                out = divide_and_conquer.tsp_divide_and_conquer(pts, max_leaf=6, time_limit=2.0)
            else:
                out = None
        elif problem=='knapsack':
            items, cap = load_knapsack(dataset)
            if method=='greedy':
                out = greedy.knapsack_greedy(items, cap)
            elif method=='d_p':
                out = d_p.knapsack_dp(items, cap)
            elif method=='backtracking':
                out = backtracking.knapsack_backtracking(items, cap, time_limit=2.0)
            elif method=='branch_and_bound':
                out = branch_and_bound.knapsack_bnb(items, cap)
            elif method=='divide_and_conquer':
                out = divide_and_conquer.knapsack_meet_in_middle(items, cap)
            else:
                out = None
        else:
            out = None
        times.append(time.perf_counter() - start)
        result = out
    return {'method': method, 'time_mean': statistics.mean(times), 'time_stdev': statistics.stdev(times) if len(times)>1 else 0.0, 'result': result}

def run_benchmarks_for_problem(problem, dataset, methods):
    results=[]
    for m in methods:
        results.append(run_single(problem, m, dataset))
    return {'problem': problem, 'dataset': dataset, 'results': results}
