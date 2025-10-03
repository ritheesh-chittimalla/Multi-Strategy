# utils/datasets.py
import os, csv, json
import networkx as nx

BASE = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def list_datasets():
    files = os.listdir(DATA_DIR)
    return [f for f in files if f.lower().endswith(('.csv','.json'))]

def load_tsp(name):
    path = os.path.join(DATA_DIR, name)
    points = []
    with open(path) as f:
        reader = csv.reader(f)
        for r in reader:
            if not r: continue
            x = float(r[0]); y = float(r[1])
            points.append((x,y))
    return points

def load_knapsack(name):
    path = os.path.join(DATA_DIR, name)
    items=[]
    cap = 50
    with open(path) as f:
        reader = csv.reader(f)
        for r in reader:
            if not r: continue
            # expect id,value,weight
            items.append((r[0], int(r[1]), int(r[2])))
    return items, cap

def load_graph(name):
    path = os.path.join(DATA_DIR, name)
    G = nx.Graph()
    with open(path) as f:
        d = json.load(f)
    for u, edges in d.items():
        for v, w in edges:
            try:
                wnum = float(w)
            except:
                wnum = 1.0
            G.add_edge(u, v, weight=wnum)
    return G
