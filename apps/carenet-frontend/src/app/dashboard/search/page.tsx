'use client'
import { Card, Col, Row } from 'antd';

// Import necessary components and hooks from React, Next.js, and Ant Design
import React, { useState, useEffect } from 'react';
import { Input, Select, Button,Spin } from 'antd';
const { Option } = Select;

export default function Search() {

  const [searchArgs, setSearchArgs] = useState({});

  const [results, setResults] = useState([]);

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

    <Row gutter={24}>
    <Col span={12}>
      <Card title="חיפוש" bordered={false}>
          <SearchComponent setSearchArgs={setSearchArgs}/>
      </Card>
    </Col>
    <Col span={12}>
      <Card title="תוצאות" bordered={false}>
      
       {
        results.length ? <ResultsComponent results={results}/> : <div></div>
       }

      </Card>
    </Col>
  </Row>
  );
}



const SearchComponent = ({setSearchArgs}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedStates, setSelectedStates] = useState([]);

  const cities = ["באר שבע"]

  const states = ["מחוז דרום"]


  // Handler for submitting the search
  const handleSubmit = () => {
    const searchData = {
      query: searchQuery,
      filters :{}
    };

    if(selectedStates.length)
    {
        searchData["filters"]["state"] = selectedStates
    }

    if(selectedCities.length)
    {
      searchData["filters"]["city"] = selectedCities
    }

    setSearchArgs(searchData)

    console.log('Search Data:', searchData);
    // Here you can also perform an API call or any other action with searchData
  };

  return (
    <div className='flex flex-col'>
      <Input.TextArea
        placeholder="הכנס פרטים עבור מציאת טיפול מתאים - ניתן לחפש בשפות שונות"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <Select
        mode="multiple"
        placeholder="עיר"
        style={{ width: '250px', margin: '10px 0' }}
        onChange={(value) => setSelectedCities(value)}
      >
       
       {
        cities.map(city => {
          return <Option value={city}>{city}</Option>
        })
       }
      
      </Select>
      <Select
        mode="multiple"
        placeholder="מחוז"
        style={{ width: '250px', margin: '10px 0' }}
        onChange={(value) => setSelectedStates(value)}
      >

{
        states.map(state => {
          return <Option value={state}>{state}</Option>
        })
       }

      </Select>
      <Button style={{ background: "#92bbfc", color: "white" }} onClick={handleSubmit}>
        חיפוש
      </Button>
    </div>
  );
};


const ResultsComponent = ({ results }) => {
  return (
    <div>
      {results.map((result, index) => (
        <Card key={index} title={result.title} style={{ margin: '10px 0' }}>
          <p><strong>Description:</strong> {result.description}</p>
          {result.email && <p><strong>Email:</strong> {result.email}</p>}
          {result.phone_number && <p><strong>Phone:</strong> {result.phone_number}</p>}
          <p><strong>Source:</strong> {result.source}</p>
          <p><strong>Location:</strong> {result.full_location}</p>
          <p><strong>City:</strong> {result.city}</p>
          <p><strong>State:</strong> {result.state}</p>
          <p><strong>Score:</strong> {result.score.toFixed(2)}</p>
        </Card>
      ))}
    </div>
  );
};

