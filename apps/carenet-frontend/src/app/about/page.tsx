'use client'

import { Card } from "antd";
import DashboardLayout from "../dashboard-layout";

export default function About() {
  return (
    <DashboardLayout>
    <Card title="אודות Carenet" className="large-font"   style={{ width: '100%', padding: '20px' }}>
    <h2 className="large-font" >ברוכים הבאים ל-Carenet</h2>
    <p className="large-font">המרכז המוביל לשירותים בתחום בריאות הנפש בישראל. ב-Carenet, אנו מחויבים להקל על הדרך אל טיפול נפשי איכותי ומתאים לכל אדם.</p>

    <br></br>

    <h3 className="large-font"><strong>המטרה שלנו</strong>   </h3>
    <p className="large-font">לפשט את התהליך של מציאת טיפול נפשי. מערכת חיפוש חכמה ויעילה, המאפשרת למצוא את הטיפול המתאים בצורה הטובה ביותר.</p>

    <br className="large-font"></br>

    <h3 className="large-font"><strong>שירותים ויכולות</strong>   </h3>

    <ul className="large-font">
        <li><strong>חיפוש מהיר וחכם:</strong> מערכת החיפוש מותאמת להעדפות האישיות וצרכים ספציפיים.</li>
        <li><strong>נגישות בשפות שונות:</strong> מערכת החיפוש תומכת במגוון שפות, לנגישות מירבית.</li>
    </ul>

    <br></br>
    <h3 className="large-font"><strong>התחייבות לאיכות</strong>   </h3>

    <p className="large-font">מרכזים את המודעות ממגוון מקורות, עם הזכויות שמורות למקור ההודעה. מידע איכותי ומהימן.</p>

    <br></br>

    <h3 className="large-font"><strong>צרו קשר</strong>   </h3>

    <p className="large-font">לכל שאלה או התעניינות, אל תהססו לפנות אלינו.</p>
</Card>
</DashboardLayout>
);
}
