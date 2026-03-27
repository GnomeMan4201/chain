const tooltip = d3.select("body")
  .append("div")
  .attr("id", "tooltip")
  .style("position", "absolute")
  .style("padding", "5px 10px")
  .style("background", "#000")
  .style("color", "#fff")
  .style("border", "1px solid #555")
  .style("font-family", "monospace")
  .style("display", "none");

node.on("mouseover", (event, d) => {
  tooltip.style("display", "block")
         .style("left", (event.pageX + 10) + "px")
         .style("top", (event.pageY - 20) + "px")
         .html(\`<b>💥 IP:</b> \${d.id}<br><b>Gen:</b> \${d.gen}<br><b>Payload:</b> \${d.payload}\`);
});

node.on("mouseout", () => {
  tooltip.style("display", "none");
});
