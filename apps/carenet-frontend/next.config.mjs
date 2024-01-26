/** @type {import('next').NextConfig} */
const nextConfig = {
 async redirects() {
    return [
      {
        source: '/',
        destination: '/dashboard/search',
        permanent: true,
      },
    ]
  },
  output: 'standalone'
};

export default nextConfig;
