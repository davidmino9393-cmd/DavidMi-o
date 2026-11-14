// Funciones puras: no red, credenciales, teléfono real ni escritura en servicios.
export function classifyInvoice(input, referenceDate = '2026-01-15') {
  const value = input && typeof input === 'object' ? input : {};
  const validDate = value => {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    const parsed = new Date(value + 'T00:00:00Z');
    return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
  };
  const result = { invoiceId: 'DATO-DESCARTADO', customer: 'Dato descartado',
    status: 'datos_invalidos', eligibleForPreview: false, simulation: true };
  // La demo rechaza IDs y clientes ajenos al conjunto de ejemplos.
  if (!/^DEMO-INV-\d{3}$/.test(value.id ?? '') ||
      !/^Cliente Demo [A-Z]$/.test(value.customer ?? '')) return result;
  result.invoiceId = value.id;
  result.customer = value.customer;
  if (value.manualReview === true) return { ...result, status: 'revision_manual' };
  if (value.paid === true) return { ...result, status: 'pagada' };
  if (typeof value.amount !== 'number' || !Number.isFinite(value.amount) ||
      value.amount <= 0 || !validDate(value.dueDate) || !validDate(referenceDate)) return result;
  result.amount = value.amount;
  result.dueDate = value.dueDate;
  if (!/^CONTACTO-DEMO-[A-Z]$/.test(value.contactReference ?? '')) {
    return { ...result, status: 'sin_contacto_demo' };
  }
  if (value.dueDate > referenceDate) return { ...result, status: 'pendiente' };
  return { ...result, status: value.dueDate === referenceDate ? 'vence_hoy' : 'vencida',
    eligibleForPreview: true };
}

export function blockDuplicates(items) {
  const counts = new Map();
  for (const item of items) counts.set(item.invoiceId, (counts.get(item.invoiceId) || 0) + 1);
  // Se bloquea todo el grupo; no se escoge un registro posiblemente contradictorio.
  return items.map(item => counts.get(item.invoiceId) > 1
    ? { ...item, status: 'duplicada', eligibleForPreview: false }
    : { ...item });
}

export function preparePreviews(items) {
  return items.map(item => ({ ...item, sent: false,
    preview: item.eligibleForPreview
      ? `SIMULACION: recordatorio de ${item.invoiceId} para ${item.customer}. Sin envio.`
      : null }));
}

export function summarize(items) {
  return { referenceDate: '2026-01-15', inputRecords: items.length,
    previews: items.filter(item => item.preview !== null).length,
    duplicateRecords: items.filter(item => item.status === 'duplicada').length,
    sentMessages: 0, networkRequests: 0, simulation: true, items };
}
