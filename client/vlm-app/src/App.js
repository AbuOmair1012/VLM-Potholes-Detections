// import logo from './logo.svg';
import './App.css';

// import React from 'react'; 

import SideBar from './components/SideBar';


function App() {
  return (
    <div className="App">
              {/* --- Start Header Bar --- */}
        <div className='App-heaser-bar'> 
          <h2>VLM</h2>
        </div>
        {/* --- End Header Bar --- */}
      <header className="App-header">

        {/* --- Start Side Bar ---  */}
        <div className='App-SideBar'>
          <SideBar />
        </div>
        {/* --- End Side Bar --- */}

        {/* --- Start Body --- */}
        <div className="App-body">
          <h1>
            This is the body area
          </h1>
        </div>
        {/* --- End Body --- */}
        
      </header>
    </div>
  );
}

export default App;
