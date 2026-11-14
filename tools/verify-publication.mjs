import { readdir, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';

export const allowedFiles = [
  '.gitignore', 'README.md', 'SECURITY.md', 'package.json',
  'assets/portada.svg', 'examples/facturas.demo.json',
  'src/rules.mjs', 'src/demo.mjs', 'tests/demo.test.mjs',
  'tools/build-workflow.mjs', 'tools/verify-publication.mjs',
  'workflows/cobranzas-demo.n8n.json'
].sort();
const root = new URL('../', import.meta.url);
const names = [];
async function walk(url, prefix = '') {
  for (const item of await readdir(url, { withFileTypes:true })) {
    if (item.isSymbolicLink()) throw new Error('No se admiten enlaces simbolicos');
    if (item.name === '.git' && prefix === '') continue;
    const name = prefix + item.name;
    if (item.isDirectory()) await walk(new URL(item.name + '/', url), name + '/');
    else if (item.isFile()) names.push(name);
    else throw new Error('Tipo de archivo inesperado');
  }
}
await walk(root);
if (JSON.stringify(names.sort()) !== JSON.stringify(allowedFiles)) throw new Error('La carpeta no coincide con la lista de publicacion');
const patterns = [
  /-----BEGIN [A-Z ]*PRIVATE KEY-----/,
  /\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})\b/,
  /\bBearer\s+[A-Za-z0-9._-]{20,}\b/i,
  /postgres(?:ql)?:\/\/[^\s]+/i,
  /\b[A-Za-z]:[\\/]+[A-Za-z0-9_. -]+[\\/]+/i,
  /https?:\/\/(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)/i,
  /(?:docs\.google\.com\/spreadsheets\/d\/|graph\.facebook\.com\/v\d+\.\d+\/)/i,
  /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i,
  /(?:"(?:apiKey|accessToken|clientSecret|password)"\s*:\s*")[^"]+/i
];
const manifest = [];
for (const name of allowedFiles) {
  const bytes = await readFile(new URL(name, root));
  if (patterns.some(pattern => pattern.test(bytes.toString('utf8')))) throw new Error('Posible dato sensible en ' + name);
  manifest.push({ file:name, bytes:bytes.length, sha256:createHash('sha256').update(bytes).digest('hex') });
}
const workflow = JSON.parse(await readFile(new URL('workflows/cobranzas-demo.n8n.json', root), 'utf8'));
if (workflow.active || workflow.nodes.some(node => node.credentials || /httpRequest|webhook|scheduleTrigger|gmail|postgres|googleSheets/i.test(node.type))) {
  throw new Error('El workflow contiene activacion, credenciales o conectores no admitidos');
}
const svg = await readFile(new URL('assets/portada.svg', root), 'utf8');
if (/<script|foreignObject|\bonload=|\bhref=/i.test(svg)) throw new Error('SVG con contenido no admitido');
console.log(JSON.stringify({ checkedFiles:manifest.length, nodes:workflow.nodes.length, suspiciousMatches:0, manifest }, null, 2));
