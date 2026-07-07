#!/usr/bin/env node
// Validates every n8n workflow JSON in n8n/workflows/: structural integrity
// (required keys, no duplicate node ids/names, every connection points at a
// real node) and wiring completeness (no node left unreachable or dead-ended,
// aside from trigger/terminal node types).
const fs = require('fs');
const path = require('path');

const TRIGGER_HINT = /trigger|webhook/i;

function validateFile(filePath) {
  const errors = [];
  let wf;
  try {
    wf = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return [`invalid JSON: ${e.message}`];
  }

  if (!wf.name) errors.push('missing "name"');
  if (!Array.isArray(wf.nodes)) errors.push('missing "nodes[]"');
  if (typeof wf.connections !== 'object' || wf.connections === null) {
    errors.push('missing "connections{}"');
  }
  if (errors.length) return errors;

  const names = new Set();
  const ids = new Set();
  for (const n of wf.nodes) {
    for (const k of ['id', 'name', 'type', 'typeVersion', 'position', 'parameters']) {
      if (!(k in n)) errors.push(`node "${n.name || n.id}" missing "${k}"`);
    }
    if (names.has(n.name)) errors.push(`duplicate node name: ${n.name}`);
    names.add(n.name);
    if (ids.has(n.id)) errors.push(`duplicate node id: ${n.id}`);
    ids.add(n.id);
  }

  const hasIncoming = new Set();
  const hasOutgoing = new Set();
  for (const [src, outputs] of Object.entries(wf.connections)) {
    if (!names.has(src)) errors.push(`connection source not a node: ${src}`);
    let producedOutput = false;
    for (const branch of outputs.main || []) {
      for (const conn of branch || []) {
        if (!names.has(conn.node)) errors.push(`connection target not a node: ${conn.node}`);
        hasIncoming.add(conn.node);
        producedOutput = true;
      }
    }
    if (producedOutput) hasOutgoing.add(src);
  }

  for (const n of wf.nodes) {
    const isTrigger = TRIGGER_HINT.test(n.type);
    if (!isTrigger && !hasIncoming.has(n.name)) {
      errors.push(`node has no incoming connection (dead code?): ${n.name}`);
    }
    // A node with neither incoming nor outgoing connections in a multi-node
    // workflow is orphaned (never wired up at all). A node with incoming but
    // no outgoing is a normal, intentional terminal/leaf step.
    if (wf.nodes.length > 1 && !hasIncoming.has(n.name) && !hasOutgoing.has(n.name) && !isTrigger) {
      errors.push(`node is orphaned (no connections at all): ${n.name}`);
    }
  }

  return errors;
}

function main() {
  const dir = path.join(__dirname, '..', 'n8n', 'workflows');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json'));
  if (!files.length) {
    console.log('No workflow JSON files found in', dir);
    return;
  }

  let failed = false;
  for (const file of files) {
    const full = path.join(dir, file);
    const errors = validateFile(full);
    if (errors.length) {
      failed = true;
      console.error(`FAIL: ${file}`);
      for (const e of errors) console.error('  - ' + e);
    } else {
      console.log(`OK:   ${file}`);
    }
  }

  if (failed) process.exit(1);
}

main();
