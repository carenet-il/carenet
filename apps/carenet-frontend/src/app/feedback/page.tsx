'use client'
import React from 'react';
import { Button, Card } from 'antd';
import DashboardLayout from '../dashboard-layout';
import { useRouter } from 'next/navigation';

export default function FeedBack() {
  
  const router = useRouter()

  return (
    <DashboardLayout>
      <Card title="משוב CareNet" style={{ width: '100%', padding: '20px' }}>
        <div className='flex flex-col items-center justify-center'>
          {/* Wrap your iframe with a div and apply the responsive styles */}
          <div className="responsive-iframe-container">
            <iframe 
              className="responsive-iframe" 
              src="https://docs.google.com/forms/d/e/1FAIpQLSdIt2xYssR3GWfjjbwa_dsLjmzYOqim6U300bN1q1W_r2_OdQ/viewform?embedded=true" 
              allowFullScreen>
                Loading…
            </iframe>
          </div>
          <div>
            <Button onClick={() => {
                router.push("/")
            }}>בחזרה לחיפוש</Button>
          </div>
        </div>
      </Card>
    </DashboardLayout>
  );
}
