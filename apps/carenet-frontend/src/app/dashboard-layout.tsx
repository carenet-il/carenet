'use client'

import React from 'react';
import {  Avatar, Layout, Menu, theme, MenuProps } from 'antd';
import { useRouter } from 'next/navigation'
import { usePathname } from 'next/navigation'
import Image from 'next/image';

const { Header, Content, Footer } = Layout;

const items = [{key : "/",label : "חיפוש"},{key : "about",label : "אודות"},]

export default function DashboardLayout({
  children, // will be a page or nested layout
}: {
  children: React.ReactNode
}) {

  const router = useRouter()

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

   const onClick: MenuProps['onClick'] = (e) => {

    router.push(e["key"])
  };

  return (
    <Layout className="layout">
      <Header  className='flex flex-row items-center'>

      <Image alt="Carenet Logo" height={64}  width={64} unoptimized  src="https://i.ibb.co/6bC8ndt/carenet.webp" />

            <Menu
              theme="dark"
              mode="horizontal"
              defaultSelectedKeys={['/']}
              items={items}
              style={{ flex: 1, minWidth: 0 }}
              onClick={onClick}

            />

      </Header>
      <Content className='p-5'>

        <div
          style={{
            background: colorBgContainer,
            padding: 24,
            borderRadius: borderRadiusLG,
          }}
        >
          { children }
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        Carenet ©{new Date().getFullYear()}
      </Footer>
    </Layout>
  );
};

