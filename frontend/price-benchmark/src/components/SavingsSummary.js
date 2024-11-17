import React from 'react';

const SavingsSummary = ({ savingsData }) => {
  return (
    <div style={{ marginTop: '20px' }}>
      <h3>Potential Savings Summary</h3>
      <ul>
        <li><strong>Average Minimum Price Savings: </strong>${savingsData.min}</li>
        <li><strong>Average 10th Percentile Price Savings: </strong>${savingsData.percentile10}</li>
        <li><strong>Average Median Price Savings: </strong>${savingsData.median}</li>
        <li><strong>Average 90th Percentile Price Savings: </strong>${savingsData.percentile90}</li>
        <li><strong>Average Maximum Price Savings: </strong>${savingsData.max}</li>
      </ul>
    </div>
  );
};

export default SavingsSummary;
