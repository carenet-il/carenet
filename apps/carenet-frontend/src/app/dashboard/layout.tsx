'use client'

import React from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { useRouter } from 'next/navigation'
import { usePathname } from 'next/navigation'

const { Header, Content, Footer } = Layout;

const items = [{key : "search",label : "Search"},{key : "about",label : "About"},]

export default function DashboardLayout({
  children, // will be a page or nested layout
}: {
  children: React.ReactNode
}) {

  const router = useRouter()
  const pathname = usePathname()
  const pathParts = pathname ? pathname.split('/').filter(part => part) : [];

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

   const onClick: MenuProps['onClick'] = (e) => {

    router.push(e["key"])
  };

  return (
    <Layout>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['search']}
          items={items}
          style={{ flex: 1, minWidth: 0 }}
          onClick={onClick}

        />
      </Header>
      <Content style={{ padding: '0 48px' }}>
        <Breadcrumb style={{ margin: '16px 0' }}>

          {
          pathParts.map((part, index) => {
            const path = `/${pathParts.slice(0, index + 1).join('/')}`;
            return <Breadcrumb.Item key={path} >{part}</Breadcrumb.Item>;
          })
          }


        </Breadcrumb>
        <div
          style={{
            background: colorBgContainer,
            minHeight: 280,
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

