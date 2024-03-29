'use client'
import { Card, Col, Row } from 'antd';


// Import necessary components and hooks from React, Next.js, and Ant Design
import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { Button } from 'antd';
import DashboardLayout from './dashboard-layout';
import { useRouter } from 'next/navigation'
import { ListResults } from './search-page/search-results';
import { SearchComponent } from './search-page/search-bar';
import { Result, SearchArgs, endpoint } from './search-page/types';


export default function SearchPage() {

  const [searchArgs, setSearchArgs] = useState<SearchArgs>({ query: "", filters: {}, threshold: 0.6 });

  const [loading, setLoading] = useState<boolean>(false);

  const [results, setResults] = useState<Result[]>([]);

  const router = useRouter()




  useEffect(() => {

    const timerId = setTimeout(() => {
      const fetchData = async () => {
        if (!searchArgs.query) return; // Only proceed if there's a query

        setLoading(true);
        try {
          const response = await fetch(`${endpoint}/documents/search`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(searchArgs)
          });

          if (!response.ok) {
            throw new Error('Network response was not ok');
          }

          const data = await response.json();
          setResults(data.results);
        } catch (error) {
          console.error('Fetch error:', error);
        } finally {
          setLoading(false); // Ensure loading is set to false both after success and error
        }
      };
      fetchData();
    }, 200)

    return () => {
      clearTimeout(timerId); // Clear the timeout if the component unmounts or if the effect re-runs
    };

  }, [searchArgs]); // Depend on searchArgs for re-fetching


  return (
    <DashboardLayout>

      <Row gutter={24} style={{ marginBottom: '10px' }}>
        <Col span={24}>
          <Card title="חיפוש טיפולים ומוסדות ברחבי הארץ" bordered={true}>
            <SearchComponent setSearchArgs={setSearchArgs} />

            <Button size='large'
              className="responsive-button" onClick={() => { router.push("/feedback") }}>
              <span>החיפוש עזר? אנא שלחו לנו משוב</span>
            </Button>

          </Card>
        </Col>

      </Row>


      <Row gutter={24}>
        <Col span={24}>

          <Card title="תוצאות" bodyStyle={{ direction: "rtl" }} bordered={true}>

            {
              (results.length > 0) && <ListResults loading={loading} results={results}></ListResults>
            }
          </Card>
        </Col>
      </Row>

    </DashboardLayout>
  )
}