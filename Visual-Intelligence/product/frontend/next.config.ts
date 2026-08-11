import type { NextConfig } from "next";

const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
    ],
  },
  async rewrites() {
    return [
      // Routes with /api/ prefix on backend (campaigns, admin)
      { source: "/api/:path*", destination: `${BACKEND_URL}/api/:path*` },
      // Routes WITHOUT /api/ prefix on backend
      { source: "/auth/:path*", destination: `${BACKEND_URL}/auth/:path*` },
      { source: "/users/:path*", destination: `${BACKEND_URL}/users/:path*` },
      { source: "/payments/:path*", destination: `${BACKEND_URL}/payments/:path*` },
      { source: "/jobs/:path*", destination: `${BACKEND_URL}/jobs/:path*` },
      { source: "/generate/:path*", destination: `${BACKEND_URL}/generate/:path*` },
      { source: "/health/:path*", destination: `${BACKEND_URL}/health/:path*` },
      { source: "/health", destination: `${BACKEND_URL}/health` },
      { source: "/static/:path*", destination: `${BACKEND_URL}/static/:path*` },
    ];
  },
};

export default nextConfig;
