import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts'

export default function StockChart({data, ticker}){

    return(
        <div>
            <h2>{ticker} Closing Price Over Time</h2>
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" />
                    <YAxis />
                    <Tooltip
                    labelFormatter={(label)=>`Date: ${label}`}
                    formatter={(value)=>[value.toFixed(2), 'Close']}
                    contentStyle={{ backgroundColor: '#1a1a2e', color: 'white' }}
                    labelStyle={{ color: 'white' }}
                    />
                    <Line type="monotone" dataKey="Close" stroke="#8884d8" dot={false} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}