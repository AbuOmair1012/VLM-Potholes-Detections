import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'


function App() {
  const [count, setCount] = useState(0);

  return (
    <>
    {/* START Here is the header  */}
    <div className="border-5 border-gray-1000 rounded-lg p-3 grid grid-cols-1 grid-rows-1 width-full mb-4 mx-4">
      <div className="border border-blue-400 rounded-md p-5 flex items-center justify-center">
          This is the header
        </div>
      </div>
    {/* END Here is the header  */} 


    <div className="flex">

      {/* START here is the sidebar */}
      <div className=" border-5 border-gray-1000 rounded-md p-3 grid  h-screen ">
        <div className="border border-yellow-400 rounded-md p-5 flex items-center justify-center">
          This is the sidebar
        </div>
      </div>
      {/* END here is the sidebar */}
      
    
      {/* START here is the body */}
      <div className="border-5 border-blue-1000 rounded-lg p-4 grid h-screen flex-1 mb-4 mx-4">
        <div className="border border-green-400 rounded-md p-5 flex items-center justify-center">
          This is the body
        </div>
      </div>
      {/* END here is the body */}

      
      {/* START here is the footer */}
      <div className="border-5 border-blue-1000 rounded-lg p-4 grid  h-screen">
        <div className="border border-red-400 rounded-md p-5 flex items-center justify-center">
          This is the footer
        </div>
      </div>
      {/* END here is the footer */}
     
    </div>

        {/* START Here is the header  */}
    <div className="border-5 border-gray-1000 rounded-lg p-3  grid-cols-1 grid-rows-1 width-full mb-4 mx-4">
      <div className="border border-orange-400 rounded-md p-5 flex items-center justify-center">
          This is the footer
        </div>
      </div>
    {/* END Here is the header  */} 
    </>
  );
}

export default App;

