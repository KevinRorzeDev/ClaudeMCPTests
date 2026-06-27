import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { execSync } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
import { z } from "zod";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const server = new McpServer({
  name: "bom-check",
  version: "1.0.0"
});

server.tool(
  "get_secret_code",
  "Runs the secret code generator and returns a unique code",
  {},
  async () => {
    const binaryPath = path.join(__dirname, "dist", "bom_check.exe");
    const output = execSync(binaryPath).toString().trim();
    return {
      content: [{ type: "text", text: output }]
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);