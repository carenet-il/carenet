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
};

export default nextConfig;
