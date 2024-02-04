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
  // if using docker uncomment this
  // output: 'standalone'
  // for git pages use the two lines below
//   output: "export",
//   basePath: "/carenet",
};

export default nextConfig;
