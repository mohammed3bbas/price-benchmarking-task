import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from './Chart';
import SavingsSummary from './SavingsSummary';
import PercentileFilter from './PercentileFilter';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';


// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);


const generateRandomColor = () => {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

const MarketVsUserRatesChart = () => {
  const [chartData, setChartData] = useState({ labels: [], datasets: [] });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [percentiles, setPercentiles] = useState([10, 50, 90]);
  const [filteredData, setFilteredData] = useState([]);
  const [savingsData, setSavingsData] = useState({
    min: 0,
    percentile10: 0,
    median: 0,
    percentile90: 0,
    max: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/market/aggregated_and_user_rates/');
        const results = response.data.results;

        if (!results || results.length === 0) {
          setError("No data available.");
          setLoading(false);
          return;
        }

        if (!Array.isArray(results)) {
          setError("Invalid data format.");
          setLoading(false);
          return;
        }

        const dates = [...new Set(results.map(result => result?.date))];
        const originsDestinations = [
          ...new Set(results.map(result => `${result?.origin}-${result?.destination}`))
        ];

        const filteredResults = originsDestinations.map(originDest => {
          const filteredDataForRoute = results.filter(result => `${result?.origin}-${result?.destination}` === originDest);

          const datasets = percentiles.map(percentile => {
            const priceKey = `percentile_${percentile}_price`;

            return {
              label: `${originDest} - Market Price (P${percentile})`,
              data: filteredDataForRoute.map(item => ({
                x: item?.date,
                y: parseFloat(item[priceKey]) || 0,
              })),
              fill: false,
              borderColor: generateRandomColor(),
              tension: 0.1,
            };
          });

          const userPriceLine = {
            label: `${originDest} - User Price`,
            data: filteredDataForRoute.map(item => ({
              x: item?.date,
              y: parseFloat(item?.user_price) || 0,
            })),
            fill: false,
            borderColor: generateRandomColor(),
            tension: 0.1,
          };

          return [userPriceLine, ...datasets];
        }).flat();

        setFilteredData(filteredResults);
        setChartData({
          labels: dates,
          datasets: filteredResults,
        });

        const avgSavings = results.reduce(
          (acc, route) => {
            acc.min += parseFloat(route?.potential_savings_min_price) || 0;
            acc.percentile10 += parseFloat(route?.potential_savings_percentile_10_price) || 0;
            acc.median += parseFloat(route?.potential_savings_median_price) || 0;
            acc.percentile90 += parseFloat(route?.potential_savings_percentile_90_price) || 0;
            acc.max += parseFloat(route?.potential_savings_max_price) || 0;
            acc.count += 1;
            return acc;
          },
          { min: 0, percentile10: 0, median: 0, percentile90: 0, max: 0, count: 0 }
        );

        setSavingsData({
          min: (avgSavings.min / avgSavings.count).toFixed(2),
          percentile10: (avgSavings.percentile10 / avgSavings.count).toFixed(2),
          median: (avgSavings.median / avgSavings.count).toFixed(2),
          percentile90: (avgSavings.percentile90 / avgSavings.count).toFixed(2),
          max: (avgSavings.max / avgSavings.count).toFixed(2),
        });

        setLoading(false);

      } catch (err) {
        setError("Error fetching data.");
        console.error(err);
        setLoading(false);
      }
    };

    fetchData();
  }, [percentiles]);

  const handlePercentileChange = (e) => {
    const value = parseInt(e.target.value);
    setPercentiles(prev =>
      prev.includes(value)
        ? prev.filter(p => p !== value)
        : [...prev, value]
    );
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>User Rates vs. Market Rates</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <PercentileFilter percentiles={percentiles} onPercentileChange={handlePercentileChange} />

      <div style={{ height: '400px', width: '100%' }}>
        {filteredData.length > 0 ? (
          <Chart chartData={chartData} filteredData={filteredData} />
        ) : (
          <p>No data to display</p>
        )}
      </div>

      <SavingsSummary savingsData={savingsData} />
    </div>
  );
};

export default MarketVsUserRatesChart;
