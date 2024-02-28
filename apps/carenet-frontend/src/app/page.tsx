'use client'
import { Card, Col, Form, Row, Space } from 'antd';
import { MailOutlined, PhoneOutlined, GlobalOutlined } from '@ant-design/icons';
import { Avatar, List } from 'antd';
import { Slider } from 'antd';

// Import necessary components and hooks from React, Next.js, and Ant Design
import React, { useState, useEffect, Dispatch, SetStateAction } from 'react';
import { Input, Select, Button, Spin } from 'antd';
import DashboardLayout from './dashboard-layout';
import { InfoCircleOutlined } from '@ant-design/icons';
import { useRouter } from 'next/navigation'
const { Option } = Select;


enum SourceType {

  N12 = "N12",
  NAFSHI = "NAFSHI",
  MOH = 'MOH',
  BTL = "BTL",
  OTEFLEV = "OTEFLEV"
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

const hostname = "https://api-carenet.koyeb.app";
// const hostname = "http://localhost:8000";

export default function SearchPage() {

  const [searchArgs, setSearchArgs] = useState<SearchArgs>({ query: "", filters: {}, threshold: 0.6 });

  const [loading, setLoading] = useState<boolean>(false);

  const [results, setResults] = useState<Result[]>([]);

  const router = useRouter()

  useEffect(() => {
    const fetchData = async () => {
      if (!searchArgs.query) return; // Only proceed if there's a query

      setLoading(true);
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
      } catch (error) {
        console.error('Fetch error:', error);
      } finally {
        setLoading(false); // Ensure loading is set to false both after success and error
      }
    };

    fetchData();
  }, [searchArgs]); // Depend on searchArgs for re-fetching


  return (
    <DashboardLayout>

      <Row gutter={24} style={{ marginBottom: '10px' }}>
        <Col span={24}>
          <Card title="חיפוש טיפולים ברחבי הארץ" bordered={true} extra={[<Button key="feedback-button" onClick={() => {
            router.push("/feedback")
          }}>החיפוש עזר לכם ? מוזמנים לשלוח לנו משוב </Button>]}>
            <SearchComponent setSearchArgs={setSearchArgs} />
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


interface SearchArgs {
  query: string
  filters: {
    city?: string,
    radius?: number,
    state?: string[]
  },
  threshold: number
}



interface SearchComponentProps {
  setSearchArgs: Dispatch<SetStateAction<SearchArgs>>
}

const SearchComponent = (SearchComponentProps: SearchComponentProps) => {

  const { setSearchArgs } = SearchComponentProps

  const [cities, setCities] = useState<string[]>([]);
  const [states, setStates] = useState<string[]>([]);


  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedCity, setSelectedCity] = useState<string>('');
  const [selectedStates, setSelectedStates] = useState<string[]>([]);
  const [thresholdValue, setThresholdValue] = useState<number>(0.6); // Initial value of the slider
  const [radiusValue, setRadiusValue] = useState<number>(5); // Initial value of the slider

  const onChange = (value: number) => {
    setThresholdValue(value);
  };

  const onRadiusChange = (value: number) => {
    setRadiusValue(value);
  };



  // Handler for submitting the search
  const handleSubmit = () => {
    if (searchQuery !== "") {
      const searchData: SearchArgs = {
        query: searchQuery,
        filters: {},
        threshold: thresholdValue
      };

      // Check if city and radius are selected; if so, prioritize city filter
      if (selectedCity && radiusValue > 0) {
        searchData.filters.city = selectedCity;
        searchData.filters.radius = radiusValue * 1000; // Convert radius to meters or as required
        // Clear state selection if city is prioritized
        setSelectedStates([]);
      }
      // If city is not selected but states are, use state filter
      else if (selectedStates.length) {
        searchData.filters.state = selectedStates;
        // Clear city and radius if states are prioritized
        setSelectedCity('');
        setRadiusValue(5); // Reset to default or any logic you prefer
      }

      setSearchArgs(searchData);
    }
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


  return (
    <Form
      name="basic"
      labelCol={{ span: 8 }}
      wrapperCol={{ span: 16 }}
      style={{ maxWidth: 600 }}
      onFinish={handleSubmit}
      layout="vertical"
      autoComplete="off"
    >

      {/* search field  */}
      <Form.Item
        tooltip={{ title: 'ניתן לחפש בשפות שונות סוגי טיפולים, מוסדות', icon: <InfoCircleOutlined /> }}
        label="חיפוש בעלי מקצוע ומוסדות"
        name="search"
        rules={[{ required: true, message: 'שדה חובה' }]}
        wrapperCol={{ offset: 0, span: 16 }}

      >
        <Input
          size='large'
          placeholder=""
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />


      </Form.Item>


      {/* city field  */}

      <Form.Item
        label="עיר"
        wrapperCol={{ offset: 0, span: 16 }}>
        <Select
          allowClear
          showSearch
          placeholder="עיר"
          onChange={(value) => {
            setSelectedCity(value);
            if (value) {
              setSelectedStates([]); // Clear states if city is selected
            }
          }}
          value={selectedCity != '' ? selectedCity : undefined}
          // Add this to disable the select when states are selected
          disabled={selectedStates.length > 0}
        >
          {cities.map((city, index) => (
            <Option key={`city-${index}`} value={city}>{city}</Option>
          ))}
        </Select>

      </Form.Item>


      {/* radius field  */}
      <Form.Item
        label='רדיוס מהעיר בק"מ'
        wrapperCol={{ offset: 0, span: 16 }}
      >
        <Slider
          disabled={selectedStates.length > 0 || !selectedCity}
          min={10}
          max={50}
          step={20}
          onChange={onRadiusChange}
          value={typeof radiusValue === 'number' ? radiusValue : 0}
          marks={{
            10: '10 km',
            30: '30 km',
            50: '50 km',
          }}
        />
      </Form.Item>


      {/* state field  */}
      <Form.Item
        label="אזור בארץ"
        wrapperCol={{ offset: 0, span: 16 }}
      >
        <Select
          mode="multiple"
          allowClear
          placeholder="אזור בארץ"
          onChange={(value) => {
            setSelectedStates(value);
            if (value.length) {
              setSelectedCity(''); // Clear city if states are selected
              setRadiusValue(5); // Reset radius if states are selected
            }
          }}
          value={selectedStates}
          // Add this to disable the select when a city is selected
          disabled={!!selectedCity}
        >
          {states.map((state, index) => (
            <Option key={`state-${index}`} value={state}>{state}</Option>
          ))}
        </Select>
      </Form.Item>

      {/* strong match slider */}
      {/* <Form.Item
        label="חוזק התאמה"
        wrapperCol={{ offset: 0, span: 16 }}
      >
        <Slider
          // tooltip={{ open: true }}
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
      </Form.Item> */}


      {/* submit */}
      <Form.Item label=""
        wrapperCol={{ offset: 0, span: 16 }}>

        <Button htmlType='submit' className='ant-menu-item-selected' style={{ color: "white" }} onClick={handleSubmit}>
          חיפוש
        </Button>

      </Form.Item>


    </Form>
  );
};



const IconTextWithHref = ({ icon, text, href, value }: { icon: React.FC; text: string, href: string, value?: string }) => {

  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    // This code will run after the component mounts, which means it's client-side
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null; // Or a placeholder until the portal is ready
  }

  if (!value) {
    return null
  }

  return <Space>
    {React.createElement(icon)}
    <a rel="noopener noreferrer"
      target="_blank"
      href={href}>
      {text}</a>
  </Space>
}




const WazeIcon = ({ full_location }: { full_location: string }) => {


  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    // This code will run after the component mounts, which means it's client-side
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null; // Or a placeholder until the portal is ready
  }

  if (!full_location) return null;


  const generateWazeLink = (address: string) => {
    return `https://waze.com/ul?q=${encodeURIComponent(address)}&navigate=yes`;
  };

  return <> <a href={generateWazeLink(full_location)} target="_blank"
    rel="noopener noreferrer" >
    <Avatar
      key="waze icon"
      src="https://www.myteacherlanguages.com/wp-content/uploads/2018/11/Waze-Icon-copy_Link.jpg"
      alt="Waze Icon"
    />
  </a>
  </>
}


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

  return (
    <div className="grid-container">
      {resultsProps.loading ? (
        <div className="loading-container">
          <Spin size="large" />
        </div>
      ) : (
        <Row gutter={[16, 16]}>
          {resultsProps.results.map((item, index) => (
            <Col xs={24} sm={12} md={8} lg={6} xl={4} key={index} style={{ display: "flex" }}>
              <ResultCard item={item}></ResultCard>
            </Col>
          ))}
        </Row>
      )}
    </div>)

}



const ResultCard = ({ item }: { item: Result }) => {

  const sourceMapAvatar = {
    [SourceType.N12]: <AvatarSource url={"https://img.mako.co.il/2020/02/17/SHAREIMG.png"}></AvatarSource>,
    [SourceType.MOH]: <AvatarSource url={"https://i.ibb.co/qCMFSM8/moh.jpg"} ></AvatarSource>,
    [SourceType.NAFSHI]: <AvatarSource url={"https://static.wixstatic.com/media/12ddcf_dd9eec1e62e1470b9d358a04db980fdc~mv2.png/v1/fill/w_400,h_400,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/AdobeStock_529317698-%5BConverted%5D.png"}>
    </AvatarSource>,
    [SourceType.BTL]: <AvatarSource url={"https://lirp.cdn-website.com/6acf9e61/dms3rep/multi/opt/66-320w.jpg"} ></AvatarSource>,
    [SourceType.OTEFLEV]: <AvatarSource url={"https://static.wixstatic.com/media/46c8a1_e579417c72394b0295fe9c107ec45da5~mv2.png/v1/fill/w_2500,h_2500,al_c/46c8a1_e579417c72394b0295fe9c107ec45da5~mv2.png"} ></AvatarSource>,
  }

  const actions = []
  if (item.email) {
    actions.push(<IconTextWithHref
      href={`mailto:${item.email}`}
      icon={MailOutlined} value={item.email} text='איימל'></IconTextWithHref>)
  }

  if (item.phone_number) {
    actions.push(<IconTextWithHref
      href={`tel:${item.phone_number}`}
      icon={PhoneOutlined} value={item.phone_number} text='טלפון'></IconTextWithHref>)
  }


  if (item.website) {
    actions.push(
      <IconTextWithHref
        href={`${item.website}`}
        icon={GlobalOutlined} value={item.website} text='אתר'></IconTextWithHref>,

    )
  }

  if (item.full_location) {
    actions.push(
      <WazeIcon full_location={item.full_location}></WazeIcon>

    )
  }

  actions.push(<>{item.source}</>)

  return (
    <Card
      style={{ display: 'flex', flexDirection: 'column', width: "100%" }}
      className='flexible-card'
      title={item.title} actions={actions}>
      <Card.Meta avatar={sourceMapAvatar[SourceType[item.source]]}>
      </Card.Meta>

      <br></br>

      <div className='break-words'>
        {item.description}
        <address className='break-words'>
          {
            [item.full_location, item.city, item.state].filter(x => x).join(",")
          }
        </address>

        {item.phone_number}
      </div>

    </Card >)


} 
