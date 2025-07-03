import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [react()],
    define: {
      __VITE_API_URL__: JSON.stringify(
        env.VITE_API_URL || process.env.VITE_API_URL
      ),
      __VITE_SITE_URL__: JSON.stringify(
        env.VITE_SITE_URL || process.env.VITE_SITE_URL
      ),
      __VITE_NODE_ID__: JSON.stringify(
        env.VITE_NODE_ID || process.env.VITE_NODE_ID
      ),
    },
    server: {
      host: "0.0.0.0",
      port: 5173,
      strictPort: true,
    },
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: "./src/setupTests.ts",
      coverage: {
        all: false,
        include: ["src/components/**/*.tsx"],
        reporter: ["text", "html"],
        lines: 50,
        functions: 50,
        branches: 50,
        statements: 50,
      },
    },
  };
});
