'use client'
import { Card, Col, Form, Row, Tag } from 'antd';

// Import necessary components and hooks from React, Next.js, and Ant Design
import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { Input, Select, Button, Spin } from 'antd';
const { Option } = Select;

interface Result {
  title: string;
  description: string;
  email?: string;          // Optional property
  phone_number?: string;   // Optional property
  source: string;
  full_location: string;
  city: string;
  state: string;
  score: number;           // Assuming score is a numeric value
}

export default function SearchPage() {

  const [searchArgs, setSearchArgs] = useState<SearchArgs>({ query: "", filters: {} });

  const [results, setResults] = useState<Result[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('https://api-carenet.koyeb.app/documents/search', {
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
      }
    };

    if (searchArgs) {
      setResults([]);

      fetchData();
    }
  }, [searchArgs]);


  return (
  <div>

    <Row gutter={24}>
      <Col span={24}>
        <Card title="חיפוש" bordered={true}>
          <SearchComponent setSearchArgs={setSearchArgs} />
        </Card>
      </Col>

    </Row>

    <Row gutter={24}>
      <Col span={24}>

        <Card title="תוצאות" bodyStyle={{ maxHeight:"50vh", overflowY:"auto", direction: "rtl" }} bordered={true}>
          {
            results.length ? <ResultsComponent results={results} /> : <div></div>
          }
        </Card>
       </Col>
    </Row> 
    
    </div>
  )

}


interface SearchArgs {
  query: string
  filters: {
    city?: string[],
    state?: string[]
  }
}



interface SearchComponentProps {
  setSearchArgs: Dispatch<SetStateAction<SearchArgs>>
}

const SearchComponent = (SearchComponentProps: SearchComponentProps) => {

  const { setSearchArgs } = SearchComponentProps

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedStates, setSelectedStates] = useState([]);

  const cities = ["באר שבע", "לוד"] // TODO GET FROM SERVER

  const states = ["מחוז הדרום"]


  // Handler for submitting the search
  const handleSubmit = () => {

    if (searchQuery !== "") {
      const searchData: SearchArgs = {
        query: searchQuery,
        filters: {}
      };

      if (selectedStates.length) {
        searchData.filters.state = selectedStates
      }

      if (selectedCities.length) {
        searchData.filters.city = selectedCities
      }

      setSearchArgs(searchData)
    }


  };

  return (
    <div className='flex flex-col'>
      <Form
        name="basic"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600 }}
        initialValues={{ remember: true }}
        onFinish={handleSubmit}
        autoComplete="off"
      >

        <Form.Item
          label=""
          name="search"
          rules={[{ required: true, message: 'שדה חובה' }]}
          wrapperCol={{ offset: 0, span: 16 }}

        >
          <Input
            size='large'
            placeholder="הכנס פרטים עבור מציאת טיפול מתאים"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />


        </Form.Item>


        <Form.Item
          label=""
          wrapperCol={{ offset: 0, span: 16 }}>
          <Select
            mode="multiple"
            placeholder="עיר"
            onChange={(value) => setSelectedCities(value)}

          >

            {
              cities.map((city, index) => {
                return <Option key={`city-${index}`} value={city}>{city}</Option>
              })
            }

          </Select>
        </Form.Item>


        <Form.Item
          label=""
          wrapperCol={{ offset: 0, span: 16 }}
        >
          <Select
            mode="multiple"
            placeholder="מחוז"
            onChange={(value) => setSelectedStates(value)}
          >

            {
              states.map((state, index) => {
                return <Option key={`state-${index}`} value={state}>{state}</Option>
              })
            }

          </Select>
        </Form.Item>


        <Form.Item label=""
          wrapperCol={{ offset: 0, span: 16 }}

        >
          <Button htmlType='submit' style={{ background: "#291F68", color: "white" }} onClick={handleSubmit}>
            חיפוש
          </Button>

        </Form.Item>


      </Form>
    </div>
  );
};



interface ChipsResultsComponentProps {
  result: Result;
}

const ChipsResultsComponent: React.FC<ChipsResultsComponentProps> = ({ result }) => {


  return (
    <div className='pt-5'>
      <Row gutter={[16, 16]} wrap>
        {result.email && (
          <Col>
            <Tag className='custom-tag'>{result.email}</Tag>
          </Col>
        )}
        {result.phone_number && (
          <Col>
            <Tag className='custom-tag'>{result.phone_number}</Tag>
          </Col>
        )}
        {result.full_location && (
          <Col>
            <Tag className='custom-tag '>{result.full_location}</Tag>
          </Col>
        )}
        {result.city && (
          <Col>
            <Tag className='custom-tag'>{result.city}</Tag>
          </Col>
        )}
        {result.state && (
          <Col>
            <Tag className='custom-tag'>{result.state}</Tag>
          </Col>
        )}
        {result.source && (
          <Col>
            <Tag className='custom-tag'>{result.source}</Tag>
          </Col>
        )}
      </Row>
    </div>

  );
};







export interface ResultsProps {
  results: Result[]
}
const ResultsComponent = (resultsProps: ResultsProps) => {

  const { results } = resultsProps

  return (
    <div>
      {
        results.map((result, index) => (
          <div className='pb-5'  key={index}>

          <Card type="inner"
            headStyle={{
              backgroundColor: "#291F68", /* Change to your desired background color */
              borderColor: "rgb(71, 176, 220)", /* Change to your desired border color */

            }}
            bodyStyle={{
              backgroundColor: "#DFE2FF", /* Change to your desired background color */
              borderColor: "rgb(71, 176, 220)", /* Change to your desired border color */
            }
            }
          

            title={<div className='text-wrap text-white'>{result.title}</div>}

          >
            <div className='text-wrap'>{result.description}</div>

            {
              <ChipsResultsComponent result={result}></ChipsResultsComponent>
            }

          </Card>
          </div>

        ))
      }
    </div>
  );
};

