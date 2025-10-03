// static/app.js
async function loadDatasets(){
  const res = await fetch('/datasets');
  const list = await res.json();
  const sel = document.getElementById('dataset');
  sel.innerHTML = '';
  list.forEach(f => {
    const o = document.createElement('option');
    o.value = f; o.innerText = f;
    sel.appendChild(o);
  });
}

document.getElementById('uploadForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const f = document.getElementById('fileInput').files[0];
  if(!f){ document.getElementById('uploadMsg').innerText='Choose a file'; return; }
  const form = new FormData(); form.append('file', f);
  const r = await fetch('/upload', {method:'POST', body: form});
  const j = await r.json();
  if(j.ok){ document.getElementById('uploadMsg').innerText = 'Uploaded: ' + j.filename; await loadDatasets(); }
  else document.getElementById('uploadMsg').innerText = 'Error: ' + (j.error || 'upload failed');
});

document.getElementById('runForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const problem = document.getElementById('problem').value;
  const method = document.getElementById('method').value;
  const dataset = document.getElementById('dataset').value;
  document.getElementById('resultText').innerText = 'Running...';
  const r = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({problem, method, dataset})});
  const j = await r.json();
  if(j.error){ document.getElementById('resultText').innerText = 'Error: ' + j.error; return; }
  document.getElementById('resultText').innerText = JSON.stringify(j, null, 2);
});

document.getElementById('benchBtn').addEventListener('click', async ()=>{
  const problem = document.getElementById('problem').value;
  const dataset = document.getElementById('dataset').value;
  const methods = ['greedy','d_p','backtracking','branch_and_bound','divide_and_conquer'];
  document.getElementById('benchResult').innerText = 'Benchmarking...';
  const r = await fetch('/benchmark', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({problem, dataset, methods})});
  const j = await r.json();
  document.getElementById('benchResult').innerText = 'Done. See chart.';
  drawBenchChart(j.results);
});

function drawBenchChart(results){
  const ctx = document.getElementById('benchChart').getContext('2d');
  const labels = results.map(r=>r.method);
  const times = results.map(r=>r.time_mean);
  if(window._chart) window._chart.destroy();
  window._chart = new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Mean time (s)', data: times }]},
    options: { responsive: true, maintainAspectRatio: false }
  });
}
