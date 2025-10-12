import React from 'react';
import tailwindcss from "@tailwindcss/vite";
import './SideBar.css';


export default function SideBar () {

    return (
        <div className="SideBar-body">
            <span class="SideBar-menu">
                <li>Home</li>
                <li>Map</li>
                <li>About</li>
            </span>
        </div>
    )
}


