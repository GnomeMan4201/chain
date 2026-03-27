const stats = {
  totalNodes: nodes.length,
  totalLinks: links.length,
  maxGeneration: Math.max(...nodes.map(n => n.gen)),
};

const panel = d3.select("body")
  .append("div")
  .attr("id", "stats-panel")
  .style("position", "absolute")
  .style("top", "10px")
  .style("right", "10px")
  .style("background", "#222")
  .style("color", "#fff")
  .style("padding", "10px")
  .style("border", "1px solid #444")
  .style("font-family", "monospace");

panel.html(`
  <b>📊 Infection Stats</b><br>
  Hosts Infected: ${stats.totalNodes}<br>
  Injections: ${stats.totalLinks}<br>
  Max Generation: ${stats.maxGeneration}
`);
