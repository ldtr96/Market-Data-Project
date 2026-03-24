import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts'

export default function StockChart({data, ticker}){

    return(
        <div>
            <h2>{ticker} Closing Price Over Time</h2>
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="close" stoke="8884d8" dot={false} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}