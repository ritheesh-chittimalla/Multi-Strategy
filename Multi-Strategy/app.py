# app.py
import os, time, json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from utils.datasets import list_datasets, load_tsp, load_knapsack, load_graph, DATA_DIR
from utils.bench import run_benchmarks_for_problem
from algorithms import greedy, d_p, backtracking, branch_and_bound, divide_and_conquer

ALLOWED_EXT = {'csv', 'json'}
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = DATA_DIR
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route('/')
def index():
    datasets = list_datasets()
    return render_template('index.html', datasets=datasets)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'No file uploaded'}), 400
    filename = secure_filename(f.filename)
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({'error': 'Unsupported file type'}), 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(path)
    return jsonify({'ok': True, 'filename': filename})

@app.route('/datasets')
def datasets():
    return jsonify(list_datasets())

@app.route('/run', methods=['POST'])
def run():
    payload = request.json
    problem = payload.get('problem')
    method = payload.get('method')
    dataset = payload.get('dataset')
    params = payload.get('params', {})

    start = time.perf_counter()
    try:
        if problem == 'tsp':
            points = load_tsp(dataset)
            if method == 'greedy':
                tour, cost = greedy.tsp_nearest_neighbor(points)
            elif method == 'd_p':
                tour, cost = d_p.tsp_held_karp(points)
            elif method == 'backtracking':
                tour, cost = backtracking.tsp_backtracking(points, time_limit=params.get('time_limit', 5.0))
            elif method == 'branch_and_bound':
                tour, cost = branch_and_bound.tsp_branch_bound(points, time_limit=params.get('time_limit', 5.0))
            elif method == 'divide_and_conquer':
                tour, cost = divide_and_conquer.tsp_divide_and_conquer(points, max_leaf=params.get('max_leaf', 8), time_limit=params.get('time_limit', 5.0))
            else:
                return jsonify({'error': 'Unknown method'}), 400
            elapsed = time.perf_counter() - start
            return jsonify({'tour': tour, 'cost': cost, 'time': elapsed})

        elif problem == 'knapsack':
            items, capacity = load_knapsack(dataset)
            # items: list of (id, value, weight)
            if method == 'greedy':
                picked, val = greedy.knapsack_greedy(items, capacity)
            elif method == 'd_p':
                picked, val = d_p.knapsack_dp(items, capacity)
            elif method == 'backtracking':
                picked, val = backtracking.knapsack_backtracking(items, capacity, time_limit=params.get('time_limit', 5.0))
            elif method == 'branch_and_bound':
                picked, val = branch_and_bound.knapsack_bnb(items, capacity)
            elif method == 'divide_and_conquer':
                picked, val = divide_and_conquer.knapsack_meet_in_middle(items, capacity)
            else:
                return jsonify({'error': 'Unknown method'}), 400
            elapsed = time.perf_counter() - start
            return jsonify({'picked': picked, 'value': val, 'capacity': capacity, 'time': elapsed})
        elif problem == 'matching':
            G = load_graph(dataset)
            import networkx as nx
            startb = time.perf_counter()
            matching = nx.max_weight_matching(G)
            elapsed = time.perf_counter() - startb
            return jsonify({'matching': [list(x) for x in matching], 'time': elapsed})
        else:
            return jsonify({'error': 'Unknown problem'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/benchmark', methods=['POST'])
def benchmark():
    payload = request.json
    problem = payload.get('problem')
    dataset = payload.get('dataset')
    methods = payload.get('methods', [])
    res = run_benchmarks_for_problem(problem, dataset, methods)
    return jsonify(res)

# serve uploaded data files
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
