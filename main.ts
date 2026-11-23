// news-image-20261122-v6 entrypoint.
//
// The artwork is pre-rendered in this repository as entry.png (1024x1024).
// This script only copies that image into the grader's output directory.
// It runs with the standard library only: no network, no python, and it
// never writes into the repository itself, so it works when the repo is
// mounted read-only and the working directory is somewhere else entirely.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const IMAGE = "entry.png";
const MAX_BYTES = 1024 * 1024;

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(1);
}

// Where the image lives: next to this script first, then the directory the
// grader advertises through MAKEFUN_BOT_DIR.
const here = dirname(fileURLToPath(import.meta.url));
const candidates = [join(here, IMAGE)];
const botDir = process.env.MAKEFUN_BOT_DIR;
if (botDir) candidates.push(join(botDir, IMAGE));
const source = candidates.find((p) => existsSync(p));
if (!source) {
  fail(`${IMAGE} missing next to main.ts (looked in: ${candidates.join(", ")})`);
}

const bytes = readFileSync(source);
if (bytes.length === 0 || bytes.length > MAX_BYTES) {
  fail(`${IMAGE} is ${bytes.length} bytes, expected 1..${MAX_BYTES}`);
}
// PNG signature + IHDR dimensions (bytes 16..24, big-endian).
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_SIG)) fail(`${IMAGE} is not a PNG`);
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`${IMAGE} is ${width}x${height}, expected 1024x1024`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
try {
  mkdirSync(outDir, { recursive: true });
} catch (err) {
  fail(`cannot create output directory ${outDir}: ${err.message}`);
}
const dest = join(outDir, IMAGE);
writeFileSync(dest, bytes);

// Read the copy back and confirm it landed byte-identical.
const back = readFileSync(dest);
if (!back.equals(bytes)) fail(`copy of ${IMAGE} differs from the source`);
const sha = createHash("sha256").update(bytes).digest("hex");
console.log(`source ${source} -> ${dest} (${bytes.length} bytes, 1024x1024, sha256 ${sha})`);
