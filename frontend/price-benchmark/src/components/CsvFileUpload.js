import React, { useState } from 'react';
import axios from 'axios';

const CsvFileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    console.log(selectedFile)
    if (selectedFile && selectedFile.type === "text/csv") {
      setFile(selectedFile);
      setError(""); // Reset error message
    } else {
      setError("Please upload a valid CSV file.");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload/csv", formData);
      onUploadSuccess(response.data);
    } catch (err) {
      setError("Error uploading file.");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Upload CSV File</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default CsvFileUpload;
