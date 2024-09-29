export const request = async (input) => {
    try {
      const url = input.url;
      const requestOptions = input.requestOptions || {}; 
  
      
      const response = await fetch(url, requestOptions);
  
      // check the status
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      // Parse
      const data = await response.json();
      return data;
  
    } catch (error) {

      // Handling error
      console.error('Error fetching data:', error);
      throw error; 

    }
  };
  