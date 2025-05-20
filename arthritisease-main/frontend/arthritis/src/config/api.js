// API Base URL
const baseURL = 'https://api.arthritisease.org';

// API Endpoints
export const API_ENDPOINTS = {
  SARA_CHAT: `${baseURL}/chatgptGeneralResponse/`,
  FILTER_COMMENTS: `${baseURL}/filterInappropriateComments/`,
  DAILY_TOPIC: `${baseURL}/topicGenerateDaily/`,
  WEATHER_DATA: `${baseURL}/getWeatherData/`,
  ARTHRITIS_DATA: `${baseURL}/getArthritisDataFromRDS/`,
  
  // Community related endpoints
  COMMENTS: `${baseURL}/arthritease-comments`,
  TOPICS: `${baseURL}/arthritease-topics`,
  SESSIONS: `${baseURL}/sessions`,
  CATEGORIES: `${baseURL}/arthritease-categories`
};

// Generic request function
export async function fetchAPI(endpoint, options = {}) {
  const {
    method = 'POST',
    data = null,
    headers = {},
    retries = 3
  } = options;

  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  
  for (let i = 0; i < retries; i++) {
    try {
      console.log(`Request ${endpoint}, attempt ${i + 1}`);
      
      const requestOptions = {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...headers
        },
        mode: 'cors'
      };

      // Add body only if data exists
      if (data) {
        requestOptions.body = JSON.stringify(data);
      }

      // Add request debug info
      console.log('Request config:', {
        url: endpoint,
        method: requestOptions.method,
        headers: requestOptions.headers,
        body: data ? JSON.stringify(data) : undefined
      });

      const response = await fetch(endpoint, requestOptions);

      // Log response info for debugging
      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries(response.headers.entries()));

      // Handle preflight response
      if (response.status === 204) {
        return null;
      }

      // Handle error response
      if (!response.ok) {
        let errorMessage;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorData.error || `HTTP Error! Status: ${response.status}`;
        } catch {
          errorMessage = `HTTP Error! Status: ${response.status}`;
        }
        throw new Error(errorMessage);
      }

      const text = await response.text();
      if (!text) {
        return null;
      }

      try {
        return JSON.parse(text);
      } catch (parseError) {
        console.error('Response parsing error:', {
          text,
          error: parseError.message
        });
        throw new Error('Invalid data format returned from server');
      }
    } catch (error) {
      const isLastAttempt = i === retries - 1;
      const isCORSError = error.message.includes('has been blocked by CORS policy');
      
      console.error('Request error:', {
        message: error.message,
        endpoint,
        attempt: i + 1,
        timestamp: new Date().toISOString(),
        isCORSError
      });

      if (isLastAttempt) {
        if (isCORSError) {
          throw new Error('CORS request denied. Please check API configuration or contact administrator');
        } else {
          throw new Error(
            error.message.includes('Failed to fetch')
              ? 'Network connection failed. Please check your network settings or try again later'
              : error.message
          );
        }
      }

      const waitTime = 1000 * Math.pow(2, i);
      console.log(`Waiting ${waitTime}ms before retry...`);
      await delay(waitTime);
    }
  }
}

// Topic-related API functions
export async function createTopic(topicData) {
  return fetchAPI(API_ENDPOINTS.TOPICS, {
    method: 'POST',
    data: topicData
  });
}

export async function getTopics(category = null) {
  const endpoint = category 
    ? `${API_ENDPOINTS.TOPICS}?category=${encodeURIComponent(category)}`
    : API_ENDPOINTS.TOPICS;
  
  return fetchAPI(endpoint, {
    method: 'GET'
  });
}

export async function updateTopic(topicId, updateData) {
  return fetchAPI(`${API_ENDPOINTS.TOPICS}/${topicId}`, {
    method: 'PUT',
    data: updateData
  });
}

export async function deleteTopic(topicId, sessionId) {
  return fetchAPI(`${API_ENDPOINTS.TOPICS}/${topicId}`, {
    method: 'DELETE',
    data: { sessionId }
  });
}

// Comment-related API functions
export async function addComment(commentData) {
  return fetchAPI(API_ENDPOINTS.COMMENTS, {
    method: 'POST',
    data: commentData
  });
}

export async function getComments(topicId) {
  return fetchAPI(`${API_ENDPOINTS.COMMENTS}?topicId=${topicId}`, {
    method: 'GET'
  });
}

export async function updateComment(commentId, updateData) {
  return fetchAPI(`${API_ENDPOINTS.COMMENTS}/${commentId}`, {
    method: 'PUT',
    data: updateData
  });
}

export async function deleteComment(commentId, sessionId) {
  return fetchAPI(`${API_ENDPOINTS.COMMENTS}/${commentId}?sessionId=${sessionId}`, {
    method: 'DELETE'
  });
} 