const { ram_read, ram_write } = require("./RAM");

function init_display(scale) {
  const canvas = document.getElementById("display");
  const ctx = canvas.getContext("2d");

  const width = 256;
  const height = 256;

  const dpr = window.devicePixelRatio || 1;

  canvas.width = width * dpr * scale;
  canvas.height = height * dpr * scale;

  canvas.style.width = `${width * scale}px`;
  canvas.style.height = `${height * scale}px`;

  ctx.scale(dpr * scale, dpr * scale);
}

function update_display() {
  const x = ram_read(253, false);
  const y = 255 - ram_read(254, false);
  const r = ram_read(250, false);
  const g = ram_read(251, false);
  const b = ram_read(252, false);
  const mode = ram_read(255, false);

  if (mode == 1) {
    // Set pixel
    ctx.fillStyle = color;
    ctx.fillRect(x, y, 1, 1);
  } else if (mode == 2) {
    // Reset pixel
    ctx.fillStyle = "#000000";
    ctx.fillRect(x, y, 1, 1);
  } else if (mode == 3) {
    // Fill screen
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, 255, 255);
  }

  ram_write(255, 0, true);
}

module.exports = { init_display, update_display };
