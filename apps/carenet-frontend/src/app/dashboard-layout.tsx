'use client'

import React from 'react';
import { Layout, Menu, theme, MenuProps, Carousel } from 'antd';
import { useRouter } from 'next/navigation'
import Image from 'next/image';
import { Typography } from 'antd';

const { Title } = Typography;

const { Header, Content, Footer } = Layout;

const items = [{ key: "/", label: "חיפוש טיפולים \\ מוסדות" }, { key : "feedback", label : "משוב"}, { key: "about", label: "אודות" }
  , { key: "terms-conditions", label: "תנאי שימוש" }]


export default function DashboardLayout({
  children, // will be a page or nested layout
}: {
  children: React.ReactNode
}) {

  const router = useRouter()

  const onClick: MenuProps['onClick'] = (e) => {

    router.push(e["key"])
  };

  return (
    <Layout className="layout background-style">
      <Header className='flex flex-row items-center header-style'>

        <div>
          <img alt="CareNet Logo" className="logo-img" onClick={() => {
            router.push("/")
          }}  src="https://i.ibb.co/yfKtz4w/DALL-E-2024-02-25-12-17-37-Revise-the-logo-for-Care-Net-a-mental-health-finder-service-by-adding-the.jpg" />
        </div>

        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['/']}
          items={items}
          className='header-style'
          style={{ flex: 1, minWidth: 0 }}
          onClick={onClick}

        />



      </Header>

      <Carousel autoplay>
        <div>
          <img className="carousel-img" src="https://wallpapers.com/images/hd/israel-flag-on-vast-desert-t4ftsydbv2t0a1oq.jpg"></img>

        </div>



      </Carousel>

      <div className='flex flex-row items-center justify-center p-4'>
        <div className='flex flex-col items-center justify-center'>


          <Title level={4} style={{ color: 'white' }} className='w-screen/2'>
            המאורעות מה-7 באוקטובר והקרבות שנפתחו מאז יצרו רעידת אדמה רגשית בקרב האוכלוסייה בישראל.


          </Title>

          <Title level={4} style={{ color: 'white' }} className='w-screen/2'>
            CareNet -  מנוע חיפוש המרכז את כל טיפולי בריאות הנפש בישראל, מספק גישה ישירה ומהירה למגוון רחב של שירותים ומטפלים בתחום.

          </Title>

          <Title level={4} style={{ color: 'white' }} className='w-screen/2'>

            הפלטפורמה נועדה להקל על החיפוש אחר סיוע נפשי, תוך שיתוף פעולה עם מוסדות וארגונים מובילים בתחום בריאות הנפש במדינה.
          </Title>


          <Title level={4} style={{ color: 'white' }} className='w-screen/2'>
            פרויקט זה נוצר בשיתוף פעולה עם קהילת ההייטק הישראלית ובתמיכת שלוותה, מרכז לבריאות הנפש.
          </Title>

          <div>
            <img style={{height : "100%" , width : "250px"}} src={"https://hospitals.clalit.co.il/shalvata/he/PublishingImages/hospital_logo.png"}></img>

            <img  style={{height : "100%" , width : "250px"}} src={"https://www.hotzvim.org.il/wp-content/uploads/2013/10/%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99-%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA-%D7%9B%D7%9C%D7%9C%D7%99%D7%AA.png"}></img>
          </div>

          
        </div>


      </div>

      <Content className='p-5'>

        <div
          className='background-style'
        >
          {children}
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }} className='background-style'>
        {
          `כל הזכויות שמורות © CareNet ${new Date().getFullYear()}`
        }
      </Footer>
    </Layout>
  );
};

