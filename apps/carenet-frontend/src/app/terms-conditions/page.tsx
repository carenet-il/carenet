'use client'
import React from 'react';
import { List, Card, Typography } from 'antd';
import DashboardLayout from '../dashboard-layout';
import { ExclamationCircleOutlined } from '@ant-design/icons';
const { Title } = Typography;

export default function About() {
  const data = [
    "מטרת האתר: CareNet מספק פלטפורמה למשתמשים למציאת סיוע ומידע בתחום בריאות הנפש. האתר משמש כמנוע חיפוש המרכז מודעות ומידע על מוסדות ושירותים שונים בתחום זה. אנו עצמנו איננו מספקים שירותים רפואיים או ייעוץ.",
    "זכויות יוצרים: כל התכנים המוצגים באתר, לרבות מידע, תמונות וטקסט, הינם בבעלות המלאה ובאחריות המקורות המקוריים של התכנים. CareNet אינה נושאת באחריות לזכויות יוצרים עבור תכנים אלו. המשתמשים מתבקשים לכבד את זכויות היוצרים והקניין הרוחני של הגורמים השונים.",
    "שימוש הוגן: השימוש באתר מותר למטרות אישיות ולא מסחריות בלבד. אין להעתיק, לשכפל, לשדר, למכור או להפיץ כל חלק מהמידע או התכנים המוצגים באתר ללא הרשאה מפורשת.",
    "הגבלת אחריות: CareNet משתדלת להציג מידע אמין ועדכני אך אינה יכולה להבטיח כי כל המידע באתר נכון, שלם או עדכני. השימוש באתר ובמידע המוצג בו הוא על אחריות המשתמש בלבד.",
    "פרטיות: CareNet מכבדת את פרטיות המשתמשים ומתחייבת לשמור על סודיות המידע שנאסף במהלך השימוש באתר.",
    "שינויים בתנאי השימוש: CareNet שומרת לעצמה את הזכות לשנות את תנאי השימוש בכל עת וללא הודעה מוקדמת. המשך השימוש באתר לאחר פרסום השינויים יחשב כהסכמה לתנאים החדשים.",
    "Google Analytics: אנו משתמשים ב-Google Analytics לצורך איסוף נתונים סטטיסטיים על שימוש באתר. המידע שאנו אוספים אינו מכיל מידע פרטי.",
  ];

  return (
    <DashboardLayout>
      <Card title="תנאי שימוש באתר CareNet" style={{ width: '100%', padding: '20px' }}>
        <Typography>
          <Title level={4}>ברוכים הבאים ל-CareNet</Title>
          <p>מנוע החיפוש המוקדש למרכז מוסדות וטיפולים בתחום בריאות הנפש. בשימושכם באתר זה, אתם מסכימים לכבד את התנאים וההגבלות המפורטים להלן:</p>
        </Typography>
        <List
          size="large"
          dataSource={data}
          renderItem={(item) => (
            <List.Item>
              <Typography.Text> <ExclamationCircleOutlined /> {item}</Typography.Text>
            </List.Item>
          )}
        />
        <Typography>
          <p>בשימושכם באתר זה, אתם מאשרים ומסכימים לתנאים אלו.</p>
        </Typography>
      </Card>
    </DashboardLayout>
  );
}
