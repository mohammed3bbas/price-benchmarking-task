import React from 'react';

const PercentileFilter = ({ percentiles, onPercentileChange }) => {
  return (
    <div>
      <label>Select Percentiles: </label>
      {[10, 50, 90].map(percentile => (
        <label key={percentile}>
          <input
            type="checkbox"
            value={percentile}
            checked={percentiles.includes(percentile)}
            onChange={onPercentileChange}
          />
          P{percentile}
        </label>
      ))}
    </div>
  );
};

export default PercentileFilter;