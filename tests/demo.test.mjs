import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { classifyInvoice, blockDuplicates, preparePreviews, summarize } from '../src/rules.mjs';

const records = JSON.parse(await readFile(new URL('../examples/facturas.demo.json', import.meta.url), 'utf8'));
const workflow = JSON.parse(await readFile(new URL('../workflows/cobranzas-demo.n8n.json', import.meta.url), 'utf8'));
const sample = records[0];
const result = summarize(preparePreviews(blockDuplicates(records.map(record => classifyInvoice(record)))));

test('el lote ficticio produce 2 vistas previas y bloquea los 2 duplicados', () => {
  assert.equal(result.inputRecords, 8);
  assert.equal(result.previews, 2);
  assert.equal(result.duplicateRecords, 2);
});
test('la revision manual prevalece aunque la factura este vencida', () => {
  assert.equal(classifyInvoice({ ...sample, manualReview: true }).eligibleForPreview, false);
  assert.equal(classifyInvoice({ ...sample, manualReview: true }).status, 'revision_manual');
});
test('una factura pagada o futura no produce vista previa', () => {
  assert.equal(classifyInvoice({ ...sample, paid: true }).eligibleForPreview, false);
  assert.equal(classifyInvoice({ ...sample, dueDate: '2026-02-01' }).eligibleForPreview, false);
});
test('sin contacto ficticio no se prepara recordatorio', () => {
  assert.equal(classifyInvoice({ ...sample, contactReference: null }).eligibleForPreview, false);
});
test('fechas imposibles e importes invalidos se bloquean', () => {
  for (const changed of [{dueDate:'2026-02-30'}, {amount:0}, {amount:Infinity}, {amount:'1000'}]) {
    assert.equal(classifyInvoice({ ...sample, ...changed }).status, 'datos_invalidos');
  }
});
test('datos ajenos a los ejemplos no se reproducen en la salida', () => {
  const value = classifyInvoice({ ...sample, id: 'EXTERNO', customer: 'dato privado' });
  assert.equal(value.invoiceId, 'DATO-DESCARTADO');
  assert.equal(value.customer, 'Dato descartado');
});
test('un duplicado con revision manual bloquea tambien la otra copia', () => {
  const items = blockDuplicates([classifyInvoice(sample), classifyInvoice({...sample, manualReview:true})]);
  assert.ok(items.every(item => item.eligibleForPreview === false));
});
test('ningun resultado simulado se marca como enviado', () => {
  assert.equal(result.sentMessages, 0);
  assert.ok(result.items.every(item => item.sent === false && item.simulation === true));
});
test('el workflow solo contiene inicio manual y codigo sin credenciales ni disparadores externos', () => {
  assert.equal(workflow.active, false);
  assert.equal(workflow.nodes.length, 6);
  assert.deepEqual(workflow.pinData, {});
  assert.ok(workflow.nodes.every(node => !node.credentials));
  assert.ok(workflow.nodes.every(node => ['n8n-nodes-base.manualTrigger','n8n-nodes-base.code'].includes(node.type)));
});
test('los cinco nodos Code ejecutan la misma simulacion sin acceso a modulos ni red', () => {
  let current = [];
  for (const node of workflow.nodes.slice(1)) {
    const context = vm.createContext({ $input: { all: () => current } });
    current = vm.runInContext(`(function(){${node.parameters.jsCode}\n})()`, context, { timeout: 1000 });
    assert.ok(Array.isArray(current));
  }
  assert.deepEqual(JSON.parse(JSON.stringify(current[0].json)), result);
});
