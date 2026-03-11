import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'

function App() {
  
const [data, setData] = useState(null);
const [isLoading, setIsLoading] = useState(true);
const [ticker, setTicker] = useState('AAPL'); /* AAPL is the default here */

useEffect(()=> {
  axios.get(`http://127.0.0.1:8000/data/${AAPL}`)
  .then(response=>{
    setData(response.data)
    setIsLoading(false)
  })

  .catch(error=>{
    console.log(error)
  })
}, [ticker])

if (isLoading){
  return <p>Loading...</p>
}

  
  return (
    <>
      <div>
        <h1>{ticker}Market Data</h1>
        <input 
          value={ticker}
          onChange={
            e=> {setTicker(e.target.value)}
          }
        />
      </div>
    </>
  )
}

export default App
