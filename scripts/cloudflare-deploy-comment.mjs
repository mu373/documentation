#!/usr/bin/env node
/**
 * Render a Markdown table for deploy status in English.
 *
 * Usage example:
 *   bun scripts/render-deploy-comment.mjs \
 *     --status "Ready" \
 *     --preview-url "https://<version>-<worker>.<subdomain>.workers.dev" \
 *     --context "pull_request" \
 *     --updated "Oct 1, 2025 1:23pm" \
 *     --out "comment.txt"
 *
 * Inputs:
 *   --status       Deployment status text (e.g., "Ready")
 *   --preview-url  Preview (or Production) URL
 *   --context      "pull_request" | "production"
 *   --updated      Human readable UTC string
 *   --out          Output file path (required)
 */

import { writeFileSync } from "node:fs";

function getArg(flag, fallback = "") {
  const i = process.argv.indexOf(flag);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const statusText = getArg("--status", "Ready");
const previewUrl = getArg("--preview-url", "");
const context = getArg("--context", "pull_request");
const updated = getArg("--updated", new Date().toUTCString());
const out = getArg("--out", "");

if (!out) {
  console.error("[error] --out is required (path to write the markdown).");
  process.exit(1);
}

const statusBadge = `![${statusText}](https://vercel.com/static/status/ready.svg) ${statusText}`;
const linkLabel = context === "production" ? "Production" : "Preview";
const previewLink = previewUrl ? `[${linkLabel}](${previewUrl})` : "N/A";

const md =
  "| Deployment | Preview | Updated (UTC) |\n" +
  "| :--- | :------ | :------ |\n" +
  `| ${statusBadge} | ${previewLink} | ${updated} |\n\n`;

writeFileSync(out, md, "utf8");
console.log(`[info] Wrote markdown to ${out}`);
