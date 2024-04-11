import { Spin, Row, Col, Card, Avatar } from "antd"
import { Result, ResultsProps, SimilarityTitleProps, SourceType, sourceMapAvatar } from "./types"
import { AvatarSource, IconTextWithHref } from "./helpers"
import { GoogleOutlined } from '@ant-design/icons';
import { MailOutlined, PhoneOutlined, GlobalOutlined } from '@ant-design/icons';
import { MeterSpeedIcon } from "./meter-speed-icon";


export const ListResults = (resultsProps: ResultsProps) => {

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



export const ResultCard = ({ item }: { item: Result }) => {

   

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
    else {
        const googleDescriptionHref = encodeURI(`https://www.google.com/search?q=${item.title}`)
        actions.push(<IconTextWithHref
            href={`${googleDescriptionHref}`}
            icon={GoogleOutlined} value={googleDescriptionHref} text=''></IconTextWithHref>,

        )
    }




    if (item.audience?.length > 0) {
        item.audience.forEach((audience: string) => {
            actions.push(
                <>
                    {audience}
                </>
            )
        })

    }

    

    const formattedScore = item.score.toFixed(2);

    return (
        <Card
            style={{ display: 'flex', flexDirection: 'column', width: "100%" }}
            className='flexible-card'
            title={
            <div>

            <Similarity title={item.title} formattedScore={(item.score * 100).toFixed(0)}/> 
            </div>
            
             } actions={actions}>
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



const Similarity = ({ formattedScore ,title } : SimilarityTitleProps) => (
    <Row  gutter={24}>
      <Col span={12}>
        <div>{title}</div>
      </Col>
      <Col span={12} >
      <div className="flex flex-col items-end">
          <Avatar shape='square'
                  size={{ xs: 24, sm: 24, md: 24, lg: 24, xl: 24, xxl: 24 }}
                  src={"/icons/speed-meter.svg"} />
          <div>{formattedScore}%</div>
        </div>
      </Col>
    </Row>
  );
  
