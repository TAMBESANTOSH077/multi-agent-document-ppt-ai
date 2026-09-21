import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],

    server: {
        host: "localhost",
        port: 5173,

        // Allows the React frontend to communicate
        // with the FastAPI backend.
        proxy: {
            "/api": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },

            "/health": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },

            "/storage": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
        },
    },
});