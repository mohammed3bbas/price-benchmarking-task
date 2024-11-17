import './App.css';
import React, { useState } from 'react';
import CsvFileUpload from './components/CsvFileUpload';
import MarketVsUserRatesChart from './components/MarketVsUserRatesChart';

const App = () => {
  const [uploadResponse, setUploadResponse] = useState(null);

  const handleUploadSuccess = (data) => {
    setUploadResponse(data);
    // console.log("File uploaded successfully:", data);
  };

  return (
    <div className="App">
      <h1>CSV File Upload</h1>
      <CsvFileUpload onUploadSuccess={handleUploadSuccess} />
      
      {uploadResponse && (
        <div>
          <h3>Upload Status</h3>
          <pre>{uploadResponse.message}</pre>
          <div>
            <h1>Shipping Price Benchmarking Tool</h1>
            <MarketVsUserRatesChart />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
