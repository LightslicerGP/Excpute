const canvas = document.getElementById("display");
const ctx = canvas.getContext("2d");

const scale = 3;
const width = 256;
const height = 256;

const dpr = window.devicePixelRatio || 1;

canvas.width = width * dpr * scale;
canvas.height = height * dpr * scale;

canvas.style.width = `${width * scale}px`;
canvas.style.height = `${height * scale}px`;

ctx.scale(dpr * scale, dpr * scale);

function plotPixel(x, y, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, 1, 1);
}

function readPixel(x, y) {
  const pixelData = ctx.getImageData(x, y, 1, 1).data;
  return { r: pixelData[0], g: pixelData[1], b: pixelData[2] };
}

// function drawPattern() {
//   ctx.fillStyle = "black";
//   ctx.fillRect(0, 0, canvas.width, canvas.height);
//   for (let x = 0; x < width; x++) {
//     let y = x;
//     plotPixel(x, y, "white");
//   }
// }

// drawPattern();
plotPixel(10, 15, "#0080ff");
