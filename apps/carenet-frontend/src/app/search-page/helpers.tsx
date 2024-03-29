import { Space, Avatar } from "antd";
import React from "react";
import { useState, useEffect } from "react";
import { AvatarSourceProps } from "./types";

export const IconTextWithHref = ({ icon, text, href, value }: { icon: React.FC; text: string, href: string, value?: string }) => {

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

        <a rel="noopener noreferrer"
            target="_blank"
            href={href}>
            {React.createElement(icon)}  {text}</a>
    </Space>
}


export const AvatarSource = (props: AvatarSourceProps) => {

    return <Avatar shape='square'
        size={{ xs: 24, sm: 32, md: 40, lg: 80, xl: 96, xxl: 120 }}
        src={props.url}></Avatar>
}

