import { Form, Row, Col, Select, Slider, Button, Input } from "antd";
import {  useState, useEffect } from "react";
import { SearchArgs, SearchComponentProps, endpoint } from './types'
import { InfoCircleOutlined } from '@ant-design/icons';
const { Option } = Select;

  
 export  const SearchComponent = (SearchComponentProps: SearchComponentProps) => {
  
    const { setSearchArgs } = SearchComponentProps
  
    const [cities, setCities] = useState<string[]>([]);
    const [states, setStates] = useState<string[]>([]);
    const [audiences, setAudiences] = useState<string[]>([]);
  
  
    const [searchQuery, setSearchQuery] = useState<string>('');
    const [selectedCity, setSelectedCity] = useState<string>('');
    const [selectedStates, setSelectedStates] = useState<string[]>([]);
    const [selectedAudiences, setSelectedAudiences] = useState<string[]>([]);
  
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
  
        if (selectedAudiences) {
          searchData.filters.audience = selectedAudiences
        }
  
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
          const response = await fetch(`${endpoint}/filters/`, {
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
          setAudiences(data.results.audience)
  
        } catch (error) {
          console.error('Fetch error:', error);
        }
      };
  
      if (states.length === 0 && cities.length === 0 && audiences.length === 0) {
        fetchFilter()
      }
  
    }, [states, cities, audiences])
  
  
    return (
      <Form
        name="basic"
        // labelCol={{ span: 8 }}
        // wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600 }}
        onFinish={handleSubmit}
        layout="vertical"
        autoComplete="off"
      >
        <Row gutter={24}>
          {/* Column for search, city, and radius */}
          <Col span={12}>
            {/* search field */}
            <Form.Item
              tooltip={{ title: 'ניתן לחפש בשפות שונות סוגי טיפולים, מוסדות', icon: <InfoCircleOutlined /> }}
              label=""
              name="search"
              rules={[{ required: true, message: 'שדה חובה' }]}
            >
              <Input
                size='large'
                placeholder="חיפוש"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </Form.Item>
  
            {/* city field */}
            <Form.Item
              label=""
            >
              <Select
                allowClear
                size='large'
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
  
            {/* radius field */}
            <Form.Item
              label='רדיוס מהעיר בק"מ'
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
          </Col>
  
          {/* Column for state and age */}
          <Col span={12}>
            {/* state field */}
            <Form.Item
              label=""
            >
              <Select
                size='large'
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
  
            {/* age range field */}
            <Form.Item
              label=""
            >
              <Select
                size='large'
                mode="multiple"
                allowClear
                placeholder="טווח גילאים"
                onChange={(value) => {
                  setSelectedAudiences(value);
                }}
                value={selectedAudiences}
              >
                {audiences.map((audience, index) => (
                  <Option key={`audience-${index}`} value={audience}>{audience}</Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
        </Row>
  
        {/* Row for submit and feedback */}
        <Row>
          <Col span={24}>
            {/* submit */}
            <Form.Item>
              <Button htmlType='submit'
                size='large'
                className='ant-menu-item-selected' style={{ color: "white" }} onClick={handleSubmit}>
                חיפוש
              </Button>
            </Form.Item>
          </Col>
        </Row>
      </Form>
    );
  
  };
