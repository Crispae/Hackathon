import React, { useState } from 'react';
import { request } from './utils/request';

function Main() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]); // Array to hold multiple results

  const url = "http://127.0.0.1:8000/retrevial";
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: query  // Using the dynamic query entered by the user
    })
  };

  const inputReq = {
    url: url,
    requestOptions: requestOptions
  };

  // Function to handle the search request
  const handleSearch = async () => {
    try {
      const data = await request(inputReq);  // Wait for the request to complete
      setResults(data.response);  // Set the results array in the state to display
    } catch (error) {
      console.error('Error fetching data:', error);
      setResults([]);  // Clear results on error
    }
  };

  return (
    <div style={{
      margin: '20px',
      display: 'flex',
      flexDirection: 'column',  // Stacks the query and result vertically
      alignItems: 'center',
      gap: '10px'
    }}>
      <div style={{ display: 'flex', gap: '10px' }}>
        <label 
          htmlFor="query-input" 
          style={{
            fontSize: '18px', 
            fontWeight: 'bold'
          }}>
          Query
        </label>
        <input 
          type="text" 
          id="query-input" 
          placeholder="Enter your query"
          value={query}  // Bind the input to the query state
          onChange={(e) => setQuery(e.target.value)}  // Update query on input change
          style={{
            padding: '8px',
            fontSize: '16px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            width: '300px'
          }}
        />
        <button 
          style={{
            padding: '8px 16px',
            fontSize: '16px',
            borderRadius: '4px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            cursor: 'pointer'
          }}
          onClick={handleSearch}  // Trigger search when the button is clicked
        >
          Search
        </button>
      </div>
      
      {/* Display the results in a table */}
      {results.length > 0 && (
        <table style={{
          marginTop: '20px',
          borderCollapse: 'collapse',  // Collapse borders for a cleaner look
          width: '100%',  // Make table width full
          maxWidth: '600px',  // Set a max width for the table
        }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ccc', padding: '8px' }}>Image</th>
              <th style={{ border: '1px solid #ccc', padding: '8px' }}>Score</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => (
              <tr key={index}>
                <td style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'center' }}>
                  <img 
                    src={result.encoding} 
                    alt={`Result ${index + 1}`} 
                    style={{ 
                      width: '100px',  // Set a fixed width
                      height: '100px', // Set a fixed height
                      objectFit: 'cover', // Maintain aspect ratio and fill the dimensions
                      borderRadius: '4px'
                    }} 
                  />
                </td>
                <td style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'center' }}>
                  {result.score.toFixed(2)} {/* Show score rounded to 2 decimal places */}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Main;
