import { readFile } from 'node:fs/promises';
import { classifyInvoice, blockDuplicates, preparePreviews, summarize } from './rules.mjs';

const records = JSON.parse(await readFile(new URL('../examples/facturas.demo.json', import.meta.url), 'utf8'));
const result = summarize(preparePreviews(blockDuplicates(records.map(record => classifyInvoice(record)))));
console.log(JSON.stringify(result, null, 2));
