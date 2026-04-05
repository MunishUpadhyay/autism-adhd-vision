import axios from 'axios';

// Absolute URL mapping directly to your native FastAPI uvicorn runtime structure
const API_URL = 'http://127.0.0.1:8000';

export const analyzeVideo = async (file) => {
  // Translate the video structure securely into a binary Form format preventing client-side blocking
  const formData = new FormData();
  formData.append('video', file);

  try {
    const response = await axios.post(`${API_URL}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to securely negotiate ML API stream natively');
  }
};
