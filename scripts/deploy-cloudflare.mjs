// Deploy to Cloudflare Workers from this machine: build (plates come from .plate-cache, so a warm build is
// quick), then upload dist as the Worker's static assets. Cloudflare never builds: its machines have no Chrome.
//   pnpm deploy:cf             production (chronoscape-threejs.<account>.workers.dev, or your custom domain)
//   pnpm deploy:cf --preview   a preview version on its own URL, named after the current git branch;
//                              production is untouched
// First time only: `pnpm dlx wrangler@4 login`.
import { execSync } from "node:child_process";

const run = (cmd) => execSync(cmd, { stdio: "inherit" });
const preview = process.argv.includes("--preview");

run("pnpm build");
if (preview) {
  const branch = execSync("git rev-parse --abbrev-ref HEAD").toString().trim();
  // aliases: lowercase letters, digits and dashes, starting with a letter
  const alias = `b-${branch.toLowerCase().replace(/[^a-z0-9-]+/g, "-")}`.slice(0, 50).replace(/-+$/, "");
  run(`pnpm dlx wrangler@4 versions upload --preview-alias ${alias}`);
} else {
  run("pnpm dlx wrangler@4 deploy");
}
