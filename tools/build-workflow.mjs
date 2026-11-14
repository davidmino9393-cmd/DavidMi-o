import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { classifyInvoice, blockDuplicates, preparePreviews, summarize } from '../src/rules.mjs';

const records = JSON.parse(await readFile(new URL('../examples/facturas.demo.json', import.meta.url), 'utf8'));
const names = ['Inicio manual', 'Facturas ficticias', 'Clasificar', 'Bloquear duplicados', 'Vistas previas', 'Resumen'];
const codes = [null,
  `return ${JSON.stringify(records)}.map(json => ({json}));`,
  `const classifyInvoice = ${classifyInvoice.toString()};\nreturn $input.all().map(item => ({json: classifyInvoice(item.json)}));`,
  `const blockDuplicates = ${blockDuplicates.toString()};\nreturn blockDuplicates($input.all().map(item => item.json)).map(json => ({json}));`,
  `const preparePreviews = ${preparePreviews.toString()};\nreturn preparePreviews($input.all().map(item => item.json)).map(json => ({json}));`,
  `const summarize = ${summarize.toString()};\nreturn [{json: summarize($input.all().map(item => item.json))}];`
];
const nodes = names.map((name, index) => ({
  id: `demo-node-${index + 1}`, name,
  type: index === 0 ? 'n8n-nodes-base.manualTrigger' : 'n8n-nodes-base.code',
  typeVersion: index === 0 ? 1 : 2,
  position: [240 + index * 240, 320],
  parameters: index === 0 ? {} : { mode: 'runOnceForAllItems', jsCode: codes[index] }
}));
const connections = Object.fromEntries(names.slice(0, -1).map((name, index) =>
  [name, { main: [[{ node: names[index + 1], type: 'main', index: 0 }]] }]));
const workflow = { name: 'Cobranzas - demo con datos ficticios', active: false,
  nodes, connections, settings: { executionOrder: 'v1', timezone: 'UTC' }, pinData: {}, tags: [] };
await mkdir(new URL('../workflows/', import.meta.url), { recursive: true });
await writeFile(new URL('../workflows/cobranzas-demo.n8n.json', import.meta.url), JSON.stringify(workflow, null, 2) + '\n');
console.log(JSON.stringify({ generated: 'workflows/cobranzas-demo.n8n.json', nodes: nodes.length, active: false }));
