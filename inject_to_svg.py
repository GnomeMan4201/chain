#!/usr/bin/env python3
from pathlib import Path
import re
import json

log_file = Path("inject_silent.log")
html_out = Path("infect_map.html")

nodes = {}
links = []
infect_times = {}

with log_file.open() as f:
    for line in f:
        m = re.search(r"\[(.*?)\] silent: Host compromised by (\d+\.\d+\.\d+\.\d+) \[ *(\d+\.\d+\.\d+\.\d+) *\]", line)
        if m:
            time, src, tgt = m.groups()
            infect_times[tgt] = time
            nodes[src] = {"id": src, "gen": 0}
            nodes[tgt] = {"id": tgt, "gen": 1}
            links.append({"source": src, "target": tgt, "time": time})

# Assign deeper generations
for _ in range(3):
    for link in links:
        s = nodes[link["source"]]["gen"]
        t = nodes[link["target"]]["gen"]
        if t <= s:
            nodes[link["target"]]["gen"] = s + 1

html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>LANIMORPH Infection Map</title>
  <style>
    body {{
      background: #000;
      color: #fff;
      margin: 0;
      font-family: monospace;
    }}
    svg {{
      width: 100vw;
      height: 100vh;
      display: block;
      background: #111;
    }}
    .node {{
      stroke: white;
      stroke-width: 0.5px;
    }}
    .label {{
      fill: white;
      font-size: 11px;
      pointer-events: none;
    }}
    .gen0 {{ fill: lime; }}
    .gen1 {{ fill: yellow; }}
    .gen2 {{ fill: orange; }}
    .gen3 {{ fill: red; }}
  </style>
</head>
<body>
<svg></svg>
<div style="position:absolute;top:6px;left:6px;">
  <span id="tstamp">—</span>
  <input id="range" type="range" min="0" max="0" step="1"/>
  <button id="play">▶</button>
</div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const NODES = {json.dumps(list(nodes.values()))};
const LINKS = {json.dumps(links)};
const svg = d3.select("svg");
const g = svg.append("g");
const width = window.innerWidth;
const height = window.innerHeight;

const sim = d3.forceSimulation(NODES)
  .force("link", d3.forceLink(LINKS).id(d => d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-200))
  .force("center", d3.forceCenter(width / 2, height / 2));

const linkSel = g.selectAll("line")
  .data(LINKS)
  .join("line")
  .attr("stroke", "#444");

const nodeSel = g.selectAll("circle")
  .data(NODES)
  .join("circle")
  .attr("r", 8)
  .attr("class", d => "node gen" + d.gen)
  .on("click", (e,d) => {{
    alert("📡 Host: " + d.id + "\\nGeneration: " + d.gen + (d.time ? "\\nTime: " + d.time : ""));
  }});

const labelSel = g.selectAll("text")
  .data(NODES)
  .join("text")
  .attr("class", "label")
  .text(d => d.id);

sim.on("tick", () => {{
  linkSel
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
  nodeSel
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
  labelSel
    .attr("x", d => d.x + 10)
    .attr("y", d => d.y + 3);
}});

// --- Timeline ---
const times = Array.from(new Set(LINKS.map(l => l.time).filter(Boolean))).sort();
const range = document.getElementById("range");
const tstamp = document.getElementById("tstamp");
range.max = Math.max(0, times.length - 1);
range.value = range.max;
tstamp.textContent = times.length ? times[range.value] : "—";

function applyTime(idx) {{
  if (!times.length) return;
  const cutoff = times[idx];
  tstamp.textContent = cutoff;
  const active = new Set();
  LINKS.forEach(l => {{
    if (l.time <= cutoff) {{
      active.add(l.source);
      active.add(l.target);
    }}
  }});
  nodeSel.style("opacity", n => active.has(n.id) ? 1 : 0.08);
  labelSel.style("opacity", n => active.has(n.id) ? 1 : 0.08);
  linkSel.style("opacity", l => l.time <= cutoff ? 0.9 : 0.05);
}}

range.addEventListener("input", e => applyTime(+e.target.value));

document.getElementById("play").addEventListener("click", () => {{
  if (!times.length) return;
  playing = !playing;
  document.getElementById("play").textContent = playing ? "⏸" : "▶";
  if (playing) {{
    let i = +range.value;
    playTimer = setInterval(() => {{
      applyTime(i);
      range.value = i;
      if (++i > +range.max) i = 0;
    }}, 450);
  }} else {{
    clearInterval(playTimer);
  }}
}});

applyTime(+range.value);
</script>
</body>
</html>
"""

html_out.write_text(html)
print(f"[✓] Map rebuilt to: {html_out}")
