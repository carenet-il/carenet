'use client'
import { Card, Col, Row, Tag } from 'antd';

// Import necessary components and hooks from React, Next.js, and Ant Design
import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { Input, Select, Button,Spin } from 'antd';
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

interface SearchArgs 
{
  query : string 
  filters : {
    city? : string[] , 
    state? : string[]
  }
}


export default function Search() {

  const [searchArgs, setSearchArgs] = useState<SearchArgs>({query : "",filters :{}});

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


interface SearchComponentProps
{
  setSearchArgs : Dispatch<SetStateAction<SearchArgs>>
}

const SearchComponent = (SearchComponentProps : SearchComponentProps) => {

  const { setSearchArgs} = SearchComponentProps

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedStates, setSelectedStates] = useState([]);

  const cities = ["באר שבע","לוד"] // TODO GET FROM SERVER

  const states = ["מחוז הדרום"]


  // Handler for submitting the search
  const handleSubmit = () => {
    const searchData : SearchArgs = {
      query: searchQuery,
      filters :{}
    };

    if(selectedStates.length)
    {
        searchData.filters.state = selectedStates
    }

    if(selectedCities.length)
    {
      searchData.filters.city = selectedCities
    }

    setSearchArgs(searchData)

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
      <Button style={{ background: "#2db7f5", color: "white" }} onClick={handleSubmit}>
        חיפוש
      </Button>
    </div>
  );
};



interface ChipsResultsComponentProps {
  result: Result;
}

const ChipsResultsComponent: React.FC<ChipsResultsComponentProps> = ({ result }) => {


  return (
    <div className='flex-wrap space-y-5'>
      {result.email && <Tag color="#2db7f5"> {result.email}</Tag>}
      {result.phone_number && <Tag color="#2db7f5">{result.phone_number}</Tag>}
      {result.full_location && <Tag color="#2db7f5"> {result.full_location}</Tag>}
      {result.city && <Tag color="#2db7f5">{result.city}</Tag>}
      {result.state && <Tag color="#2db7f5">{result.state}</Tag>}
    </div>
  );
};





export interface ResultsProps 
{
  results : Result[]
}
const ResultsComponent = (resultsProps:ResultsProps) => {

  const { results } = resultsProps

  return (
    <div className='height-screen-full'>
      {
          results.map((result, index) => (
            <Card key={index} title={result.title} style={{ margin: '10px 0' }}>
                 {result.description}

                 {
                   <ChipsResultsComponent result={result}></ChipsResultsComponent>
                 }

              </Card>

          ))
      } 
    </div>
  );
};

