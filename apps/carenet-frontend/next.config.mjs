/** @type {import('next').NextConfig} */
const nextConfig = {
   images: {
    unoptimized: true,
  },
  // if using docker uncomment this
  // output: 'standalone'
  // for git pages use the two lines below
  output: "export",
  // when using git pages with a custom domain comment the line below
  // basePath: "/carenet",
};

export default nextConfig;
