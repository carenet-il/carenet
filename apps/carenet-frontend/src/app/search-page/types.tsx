import { Dispatch, SetStateAction } from "react";
import { AvatarSource } from "./helpers";

export enum SourceType {

    N12 = "N12",
    NAFSHI = "NAFSHI",
    MOH = 'MOH',
    BTL = "BTL",
    OTEFLEV = "OTEFLEV",
    MACCABI_ART_THERAPY = "MACCABI_ART_THERAPY"

}

export interface SimilarityTitleProps {
    title:string;
    formattedScore:string;
}

export interface Result {
    title: string;
    website?: string;
    description: string;
    email?: string;          // Optional property
    phone_number?: string;   // Optional property
    source: SourceType;
    full_location: string;
    audience: string[]
    city: string;
    state: string;
    score: number;           // Assuming score is a numeric value
}



export interface SearchArgs {
    query: string
    filters: {
        city?: string,
        radius?: number,
        audience?: string[],
        state?: string[]
    },
    threshold: number
}


export interface ResultsProps {
    results: Result[],
    loading: boolean
}

export interface SearchComponentProps {
    setSearchArgs: Dispatch<SetStateAction<SearchArgs>>
  }



  export interface AvatarSourceProps {
    url: string
  }

  export const sourceMapAvatar = {
    [SourceType.N12]: <AvatarSource url={"https://img.mako.co.il/2020/02/17/SHAREIMG.png"}></AvatarSource>,
    [SourceType.MOH]: <AvatarSource url={"https://i.ibb.co/qCMFSM8/moh.jpg"} ></AvatarSource>,
    [SourceType.NAFSHI]: <AvatarSource url={"https://static.wixstatic.com/media/12ddcf_dd9eec1e62e1470b9d358a04db980fdc~mv2.png/v1/fill/w_400,h_400,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/AdobeStock_529317698-%5BConverted%5D.png"}>
    </AvatarSource>,
    [SourceType.BTL]: <AvatarSource url={"https://lirp.cdn-website.com/6acf9e61/dms3rep/multi/opt/66-320w.jpg"} ></AvatarSource>,
    [SourceType.OTEFLEV]: <AvatarSource url={"https://static.wixstatic.com/media/46c8a1_e579417c72394b0295fe9c107ec45da5~mv2.png/v1/fill/w_2500,h_2500,al_c/46c8a1_e579417c72394b0295fe9c107ec45da5~mv2.png"} ></AvatarSource>,
    [SourceType.MACCABI_ART_THERAPY]: <AvatarSource url={"https://www.maccabi4u.co.il/new/media/mjtdunor/newapp.png"} ></AvatarSource>,

}


export const endpoint = "https://api-carenet.koyeb.app";
//export const endpoint = "http://localhost:8000";