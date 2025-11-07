/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/predict',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/predict`,
      },
    ];
  },
};

module.exports = nextConfig;