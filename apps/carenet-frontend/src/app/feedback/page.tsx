'use client'
import React from 'react';
import { Button, Card } from 'antd';
import DashboardLayout from '../dashboard-layout';
import { useRouter } from 'next/navigation';

export default function FeedBack() {
  
  const router = useRouter()

  return (
    <DashboardLayout>
      <Card className="flexible-card" style={{ width: '100%'}}>
           
        <div className='flex flex-col items-center justify-center'>
        <p>
          למתחברים דרך הטלפון - ניתן להפוך את הטלפון בצורה אופקית לתצוגה נוחה של טופס המשוב. 
        </p>
        <iframe 
              width="100%"
              height="700px"
              src="https://docs.google.com/forms/d/e/1FAIpQLSdIt2xYssR3GWfjjbwa_dsLjmzYOqim6U300bN1q1W_r2_OdQ/viewform?embedded=true" 
              allowFullScreen>
                Loading…
            </iframe>

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
