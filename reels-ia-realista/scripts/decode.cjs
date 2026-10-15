// Lê o QR code de quadros PNG (jsQR). Uso:
//   node scripts/decode.cjs <quadro.png> [mais.png ...]
// Um arquivo: imprime só o conteúdo do QR (ou "nenhum QR"). Vários: "arquivo: conteúdo".
// Sai com código 1 se algum quadro não tiver QR legível (bom para usar em checklist).
//
// Dependências: pasta de ferramentas $FERR do preâmbulo da skill, FORA do projeto do vídeo
// (instalação única; precisa de rede na 1ª vez):
//   export FERR="$HOME/hyperframes/_ferramentas" NODE_PATH="$HOME/hyperframes/_ferramentas/qr/node_modules"
//   [ -d "$FERR/qr/node_modules/jsqr" ] || (mkdir -p "$FERR/qr" && cd "$FERR/qr" && npm i qrcode@1.5.4 jsqr@1.4.0 pngjs@7.0.0)
// Onde o require procura, nesta ordem:
//   1) QR_NODE_MODULES (variável explícita, ex.: QR_NODE_MODULES="$FERR/qr/node_modules")
//   2) node_modules ao lado deste script ou em pastas acima dele
//   3) NODE_PATH (o preâmbulo exporta NODE_PATH="$FERR/qr/node_modules")
// Para extrair o quadro: ffmpeg -ss 18.6 -i final.mp4 -frames:v 1 q.png   (PNG; jsQR lê RGBA via pngjs)
const fs = require("fs");
const path = require("path");

function load(name) {
  const tries = [];
  if (process.env.QR_NODE_MODULES) tries.push(path.join(process.env.QR_NODE_MODULES, name));
  tries.push(name); // NODE_PATH + node_modules ao lado/acima do script
  for (const t of tries) {
    try {
      return require(t);
    } catch (e) {
      if (e.code !== "MODULE_NOT_FOUND") throw e;
    }
  }
  console.error(
    `falta o pacote "${name}". Instale uma vez (precisa de rede):\n` +
      `  export FERR="$HOME/hyperframes/_ferramentas"; mkdir -p "$FERR/qr" && cd "$FERR/qr" && npm i qrcode@1.5.4 jsqr@1.4.0 pngjs@7.0.0\n` +
      `Depois rode com NODE_PATH="$FERR/qr/node_modules" (ou QR_NODE_MODULES="$FERR/qr/node_modules").`
  );
  process.exit(2);
}

const { PNG } = load("pngjs");
const jsQR = load("jsqr");

const files = process.argv.slice(2);
if (!files.length) {
  console.error("uso: node decode.cjs <quadro.png> [mais.png ...]");
  process.exit(2);
}
let falhou = 0;
for (const f of files) {
  const png = PNG.sync.read(fs.readFileSync(f));
  const res = jsQR(new Uint8ClampedArray(png.data), png.width, png.height);
  const txt = res ? res.data : "nenhum QR";
  if (!res) falhou++;
  console.log(files.length > 1 ? `${f}: ${txt}` : txt);
}
process.exit(falhou ? 1 : 0);
