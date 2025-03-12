/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; frame-src 'self' https://pdf-easy-edits.vercel.app https://pdf-easy-edits.onrender.com; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
          },
        ],
      },
    ];
  }
};

export default nextConfig; 