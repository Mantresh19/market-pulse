import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [zThreshold, setZThreshold] = useState(2.0);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchMarketData = async () => {
    setLoading(true);
    try {
      const url = `http://localhost:8000/api/analyze/${ticker}?z_threshold=${zThreshold}`;
      const response = await fetch(url);
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Failed to connect to Python API:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchMarketData();
  }, []);

  return {
    <div className="dashboard">
      {}
      <header className = "header">
      <h1>📊 MarketPulse AI</h1>
      <div className="controls">
      <input type="text"
      value={ticker}
      onChange={(e)} />
      </div>
    </div>
  }
}