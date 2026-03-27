const btn = d3.select("body").append("button")
  .text("💾 Export SVG")
  .style("position", "absolute")
  .style("top", "10px")
  .style("left", "10px")
  .style("padding", "5px 10px")
  .style("background", "#333")
  .style("color", "#fff")
  .style("border", "1px solid #555")
  .on("click", () => {
    const svg = document.querySelector("svg");
    const blob = new Blob([svg.outerHTML], {type: "image/svg+xml"});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "infect_map.svg";
    a.click();
  });
