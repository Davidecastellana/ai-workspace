// tina/config.ts
import { defineConfig } from "tinacms";
var config_default = defineConfig({
  branch: process.env.HEAD || "main",
  // For local-only mode, clientId and token are not required
  clientId: process.env.NEXT_PUBLIC_TINA_CLIENT_ID || "",
  token: process.env.TINA_TOKEN || "",
  build: {
    outputFolder: "admin",
    publicFolder: "public"
  },
  media: {
    tina: {
      mediaRoot: "public/uploads",
      publicFolder: "public"
    }
  },
  schema: {
    collections: [
      // ─── Layer 1: Knowledge & Context ───────────────────────────────────────
      {
        label: "Context & Knowledge",
        name: "context",
        path: "context",
        format: "md",
        fields: [
          {
            type: "string",
            label: "Title",
            name: "title",
            isTitle: true,
            required: true
          },
          {
            type: "string",
            label: "Description",
            name: "description"
          },
          {
            type: "rich-text",
            label: "Body",
            name: "body",
            isBody: true
          }
        ]
      },
      // ─── Layer 2: Pipeline Definitions ──────────────────────────────────────
      {
        label: "Pipelines",
        name: "pipeline",
        path: "pipelines",
        format: "yaml",
        fields: [
          {
            type: "string",
            label: "Name",
            name: "name",
            isTitle: true,
            required: true
          },
          {
            type: "string",
            label: "Description",
            name: "description"
          },
          {
            type: "string",
            label: "Trigger",
            name: "trigger",
            options: ["on-push", "scheduled", "manual"]
          },
          {
            type: "object",
            label: "Steps",
            name: "steps",
            list: true,
            fields: [
              {
                type: "string",
                label: "Step Name",
                name: "name",
                required: true
              },
              {
                type: "string",
                label: "Type",
                name: "type",
                options: ["claude-code", "shell"],
                required: true
              },
              {
                type: "string",
                label: "Prompt (for claude-code steps)",
                name: "prompt"
              },
              {
                type: "string",
                label: "Command (for shell steps)",
                name: "command"
              }
            ]
          }
        ]
      }
    ]
  }
});
export {
  config_default as default
};
