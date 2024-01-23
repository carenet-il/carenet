'use client'
import { Card } from 'antd';

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
    <div>
       <SearchComponent setSearchArgs={setSearchArgs}/>
       {
        results.length ? <ResultsComponent results={results}/> : <div>  <Spin /></div>
       }


    </div>
  );
}



const SearchComponent = ({setSearchArgs}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedStates, setSelectedStates] = useState([]);

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
    <div>
      <Input
        placeholder="Enter search text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <Select
        mode="multiple"
        placeholder="Select cities"
        style={{ width: '100%', margin: '10px 0' }}
        onChange={(value) => setSelectedCities(value)}
      >
        {/* Options for cities */}
        {/* Replace these options with real city data */}
        <Option value="city1">City1</Option>
        <Option value="city2">City2</Option>
        {/* ... other cities */}
      </Select>
      <Select
        mode="multiple"
        placeholder="Select states"
        style={{ width: '100%', margin: '10px 0' }}
        onChange={(value) => setSelectedStates(value)}
      >
        {/* Options for states */}
        {/* Replace these options with real state data */}
        <Option value="state1">State1</Option>
        <Option value="state2">State2</Option>
        {/* ... other states */}
      </Select>
      <Button onClick={handleSubmit}>
        Search
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

