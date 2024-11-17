import React from 'react';
import { Line } from 'react-chartjs-2';

const Chart = ({ chartData, filteredData }) => {
  return (
    <Line
      data={{ labels: chartData.labels, datasets: filteredData }}
      options={{
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'User Rates vs. Market Rates',
          },
          legend: {
            position: 'top',
          },
        },
        scales: {
          x: {
            type: 'category',
            title: {
              display: true,
              text: 'Date',
            },
          },
          y: {
            type: 'linear',
            title: {
              display: true,
              text: 'Price ($)',
            },
          },
        },
      }}
    />
  );
};

export default Chart;
