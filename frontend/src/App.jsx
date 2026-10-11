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
    }
  }
}