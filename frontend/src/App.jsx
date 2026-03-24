import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import StockChart from './StockChart';

function App() {
  
const [data, setData] = useState(null);
const [isLoading, setIsLoading] = useState(true);
const [ticker, setTicker] = useState('META'); /* AAPL is the default here */
const[searchTicker, setSearchTicker] = useState('META')
const[startDate, setStartDate] = useState('')
const[endDate, setEndDate] = useState('')
const [searchTrigger, setSearchTrigger] = useState(0)

useEffect(()=> {
  axios.get(`http://127.0.0.1:8000/data/${searchTicker}?start_date=${startDate}&end_date=${endDate}`)
  .then(response=>{
    console.log(response.data.data)
    setData(response.data.data)
    setIsLoading(false)
  })

  .catch(error=>{
    console.log(error)
  })
}, [searchTicker,searchTrigger])

if (isLoading){
  return <p>Loading...</p>
}

  return (
    <>
      <div className="container">
      <div className="search-bar">
        <h1>{ticker} Market Data</h1>
        <input 
          value={ticker}
          onChange={e=> {setTicker(e.target.value)}}
        />

        <input
          type="date"
          value={startDate}
          onChange={e => setStartDate(e.target.value)}
          />
        
        <input
          type="date"
          value={endDate}
          onChange={e => setEndDate(e.target.value)}
          />

        <button onClick={()=>{
          setSearchTicker(ticker)
          setSearchTrigger(prev => prev + 1)
        }}>
          Search
        </button>
      </div>
      <div className= "StockChart">
        <StockChart data={data} ticker={searchTicker} />
      </div>
      <div className= "data-table">
        <table>
          <thead className="header">
            <tr>
              <th>Date</th>
              <th>Ticker</th>
              <th>Open</th>
              <th>Close</th>
              <th>Intraday Difference</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row,i)=> (
              <tr key = {i}>
                <td>{row.Date}</td>
                <td>{row.Ticker}</td>
                <td>{parseFloat(row.Open).toFixed(2)}</td>
                <td>{parseFloat(row.Close).toFixed(2)}</td>
                <td style={{color: row.Intraday_Difference >= 0 ? 'green' : 'red'}}>{parseFloat(row.Intraday_Difference).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      </div>
    </>
  )
}

export default App
