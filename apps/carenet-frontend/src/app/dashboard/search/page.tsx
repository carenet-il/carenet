'use client'
import { Card, Col, Form, Row, Tag } from 'antd';

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

export default function SearchPage() {

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


  return (<>

    <Row gutter={24} className='pb-5'>
      <Col span={12}>
      <Card title="חיפוש" bordered={true}>
          <SearchComponent setSearchArgs={setSearchArgs}/>
      </Card>
      </Col>

    </Row>

    <Row gutter={24}>
    <Col>

      <Card title="תוצאות" bodyStyle={{maxHeight : 500 , overflowY:"auto",direction:"rtl"}} bordered={true}>
      {
       results.length ? <ResultsComponent results={results}/> : <div></div>
      }
     </Card>
     </Col>
  </Row>
  </>);
}


interface SearchArgs 
{
  query : string 
  filters : {
    city? : string[] , 
    state? : string[]
  }
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

    if (searchQuery !== "")
    {
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
        >
        <Input
            placeholder="הכנס פרטים עבור מציאת טיפול מתאים - ניתן לחפש בשפות שונות"
            style={{fontSize : "18px" ,width : 800}}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />


        </Form.Item>


        <Form.Item label="">
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
        </Form.Item>


        <Form.Item label="">
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
        </Form.Item>


        
      <Button htmlType='submit' style={{ background: "#001529", color: "white",width:250 }} onClick={handleSubmit}>
        חיפוש
      </Button>

        </Form>




      
      
     
    </div>
  );
};



interface ChipsResultsComponentProps {
  result: Result;
}

const ChipsResultsComponent: React.FC<ChipsResultsComponentProps> = ({ result }) => {


 return (
  <div className='flex flex-wrap space-y-2 space-x-2 large-font-padding' style={{width:300}}>
    {result.email && <div><Tag color="#2db7f5" className="large-font-padding">{result.email}</Tag> </div>}
    {result.phone_number && <div> <Tag color="#2db7f5" className="large-font-padding">{result.phone_number}</Tag>  </div>}
    {result.full_location &&<div> <Tag color="#2db7f5" className="large-font-padding">{result.full_location}</Tag>  </div>}
    {result.city && <div> <Tag color="#2db7f5" className="large-font-padding">{result.city}</Tag>  </div>}
    {result.state &&<div> <Tag color="#2db7f5" className="large-font-padding">{result.state}</Tag>  </div>}
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
    <div>
      {
          results.map((result, index) => (
            <Card type="inner" className='custom-card' key={index} title={<div style={{ fontSize: '18px' }}>{result.title}</div>} style={{ margin: '10px 0' }}>
                 <div style={{ fontSize: '18px' }}>{result.description}</div>

                 {
                   <ChipsResultsComponent result={result}></ChipsResultsComponent>
                 }

              </Card>

          ))
      } 
    </div>
  );
};

