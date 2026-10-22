// Exporta los stickers a PNG transparente de 512×512 (y los logos a PNG de 1024 de ancho).
// Uso: node exportar.js   (necesita playwright con chromium). Después, para WebP: python3 webp.py
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const raiz = __dirname;
const trabajos = [];
const stickers = JSON.parse(fs.readFileSync(path.join(raiz, 'stickers', 'stickers.json'), 'utf8'));
for (const lista of Object.values(stickers)) {
  for (const s of Object.values(lista)) {
    trabajos.push({ svg: path.join(raiz, 'stickers', s.archivo), png: path.join(raiz, 'png', 'stickers', s.archivo.replace('.svg', '.png')), ancho: 512, alto: 512 });
  }
}
for (const archivo of fs.readdirSync(path.join(raiz, 'marca'))) {
  if (!archivo.endsWith('.svg') || archivo.includes('_solo')) continue;
  trabajos.push({ svg: path.join(raiz, 'marca', archivo), png: path.join(raiz, 'png', 'marca', archivo.replace('.svg', '.png')), ancho: 1024 });
}

(async () => {
  const navegador = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  const pagina = await navegador.newPage();
  for (const t of trabajos) {
    fs.mkdirSync(path.dirname(t.png), { recursive: true });
    const svg = fs.readFileSync(t.svg, 'utf8');
    const [, , , w, h] = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/).map(Number);
    const alto = t.alto || Math.round(t.ancho * h / w);
    await pagina.setViewportSize({ width: t.ancho, height: alto });
    await pagina.setContent(`<html><body style="margin:0;background:transparent;display:grid;place-items:center;width:${t.ancho}px;height:${alto}px">`
      + `<div style="width:100%;height:100%">${svg.replace('<svg ', '<svg width="100%" height="100%" ')}</div></body></html>`);
    await pagina.screenshot({ path: t.png, omitBackground: true });
  }
  await navegador.close();
  console.log(trabajos.length, 'PNG');
})();
