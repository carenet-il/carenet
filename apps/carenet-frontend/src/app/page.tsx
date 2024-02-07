'use client'
import { Card, Col, Form, Row } from 'antd';
import { MailOutlined, PhoneOutlined, GlobalOutlined } from '@ant-design/icons';
import { Avatar, List } from 'antd';
import { Slider } from 'antd';

// Import necessary components and hooks from React, Next.js, and Ant Design
import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { Input, Select, Button, Spin } from 'antd';
import DashboardLayout from './dashboard-layout';
const { Option } = Select;


enum SourceType {

  N12 = "N12",
  NAFSHI = "NAFSHI",
  MOH = 'MOH',
  BTL = "BTL"
}


interface Result {
  title: string;
  website?: string;
  description: string;
  email?: string;          // Optional property
  phone_number?: string;   // Optional property
  source: SourceType;
  full_location: string;
  city: string;
  state: string;
  score: number;           // Assuming score is a numeric value
}

export default function SearchPage() {

  const [searchArgs, setSearchArgs] = useState<SearchArgs>({ query: "", filters: {},threshold : 0.8  });

  const [loading, setLoading] = useState<boolean>(false);

  const [results, setResults] = useState<Result[]>([]);


  const hostname = "https://api-carenet.koyeb.app";
//   const hostname = "http://localhost:8000";

  useEffect(() => {
    const fetchData = async () => {

      setLoading(true)
      try {
        const response = await fetch(`${hostname}/documents/search`, {
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
        setLoading(false)
      } catch (error) {
        console.error('Fetch error:', error);
        setLoading(true)
      }
    };

    if (searchArgs) {
      fetchData();
    }
  }, [searchArgs]);


  return (

    <DashboardLayout>
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

          <Card title="תוצאות" bodyStyle={{ maxHeight: "50vh", overflowY: "auto", direction: "rtl" }} bordered={true}>

            {
              (results.length > 0) && <ListResults loading={loading} results={results}></ListResults>
            }
          </Card>
        </Col>
      </Row>

    </div>
    </DashboardLayout>
  )

}


interface SearchArgs {
  query: string
  filters: {
    city?: string[],
    state?: string[]
  },
  threshold:number
}



interface SearchComponentProps {
  setSearchArgs: Dispatch<SetStateAction<SearchArgs>>
}

const SearchComponent = (SearchComponentProps: SearchComponentProps) => {

  const { setSearchArgs } = SearchComponentProps

  const [cities, setCities] = useState<string[]>([]);
  const [states, setStates] = useState<string[]>([]);


  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCities, setSelectedCities] = useState([]);
  const [selectedStates, setSelectedStates] = useState([]);
  const [thresholdValue, setThresholdValue] = useState(0.8); // Initial value of the slider

  const onChange = (value:number) => {
        setThresholdValue(value);
  };

  useEffect(() => {

    const fetchFilter = async () => {
      try {
        const response = await fetch(`${hostname}/filters/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setCities(data.results.city)
        setStates(data.results.state)
      } catch (error) {
        console.error('Fetch error:', error);
      }
    };

    if (states.length === 0 && cities.length === 0) {
      fetchFilter()
    }

  }, [states, cities])


  // Handler for submitting the search
  const handleSubmit = () => {

    if (searchQuery !== "") {
      const searchData: SearchArgs = {
        query: searchQuery,
        filters: {},
        threshold : thresholdValue
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
        layout="vertical"
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
            placeholder="אזור בארץ"
            onChange={(value) => setSelectedStates(value)}
          >

            {
              states.map((state, index) => {
                return <Option key={`state-${index}`} value={state}>{state}</Option>
              })
            }

          </Select>
        </Form.Item>


        <Form.Item

         label="חוזק התאמה"

        >
        <Slider
              min={0.6}
              max={0.8}
              step={0.1}
              onChange={onChange}
              value={typeof thresholdValue === 'number' ? thresholdValue : 0}
              marks={{
                0.6: '0.6',
                0.7: '0.7',
                0.8: '0.8',
              }}
            />
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

  const generateWazeLink = (address: string) => {
    return `https://waze.com/ul?q=${encodeURIComponent(address)}&navigate=yes`;
  };

  return (
    <div className='pt-5'>
      <Row gutter={[16, 16]} wrap>
        {result.email && (
          <Col>
            <Button
              href={`mailto:${result.email}`}
              size='large'
              icon={<MailOutlined />}
            >
            </Button>
          </Col>
        )}
        {result.phone_number && (
          <Col>
            <Button
              href={`tel:${result.phone_number}`}
              size='large'
              icon={<PhoneOutlined />}
            >
            </Button>
          </Col>
        )}



        {result.full_location && (
          <Col>
            <a href={generateWazeLink(result.full_location)} target="_blank"
              rel="noopener noreferrer" >
              <img
                key="waze icon"
                src="https://www.myteacherlanguages.com/wp-content/uploads/2018/11/Waze-Icon-copy_Link.jpg"
                alt="Waze Icon"
                style={{ width: '40px', height: '40px' }}
              />
            </a>


          </Col>
        )}


        {result.website && (
          <Col>
            <Button
              size='large'
              href={result.website}
              target="_blank"
              rel="noopener noreferrer"
              icon={<GlobalOutlined />}
            >
              אתר
            </Button>
          </Col>
        )}


      </Row>
    </div>
  );
};







export interface ResultsProps {
  results: Result[],
  loading: boolean
}



interface AvatarSourceProps {
  url: string
}
const AvatarSource = (props: AvatarSourceProps) => {

  return <Avatar shape='square'
    size={{ xs: 24, sm: 32, md: 40, lg: 80, xl: 96, xxl: 120 }}
    src={props.url}></Avatar>
}


const ListResults = (resultsProps: ResultsProps) => {

  const sourceMapAvater = {
    [SourceType.N12]: <AvatarSource url={"https://img.mako.co.il/2020/02/17/SHAREIMG.png"}></AvatarSource>,
    [SourceType.MOH]: <AvatarSource url={"https://www.ihud.org.il/wp-content/uploads/2018/07/unnamed.jpg"} ></AvatarSource>,
    [SourceType.NAFSHI]: <AvatarSource url={"https://static.wixstatic.com/media/12ddcf_dd9eec1e62e1470b9d358a04db980fdc~mv2.png/v1/fill/w_400,h_400,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/AdobeStock_529317698-%5BConverted%5D.png"}>
    </AvatarSource>,
    [SourceType.BTL]: <AvatarSource url={"https://lirp.cdn-website.com/6acf9e61/dms3rep/multi/opt/66-320w.jpg"} ></AvatarSource>

  }

  return <>
    <List
      loading={resultsProps.loading}
      itemLayout="horizontal"
      dataSource={resultsProps.results}
      renderItem={(item, index) => (
        <List.Item actions={
          [

            <ChipsResultsComponent key={index} result={item}></ChipsResultsComponent>


          ]}>
          <List.Item.Meta
            avatar={sourceMapAvater[SourceType[item.source]]}
            title={item.title}
            description={<div className='flex flex-col space-y-2 break-words'>
              <div className='break-words'>
                {
                  item.description
                }
              </div>
              <div className='break-words'>
                {
                  item.full_location
                }
              </div>
              <div className='break-words'>
                {
                  item.city
                }
              </div>
              <div className='break-words'>
                {
                  item.state
                }
              </div>



            </div>
            }></List.Item.Meta>

        </List.Item>
      )}
    />
  </>
}

