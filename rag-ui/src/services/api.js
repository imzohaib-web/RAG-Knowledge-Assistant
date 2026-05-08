// API Service for RAG Knowledge Assistant
// Handles communication with FastAPI backend

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('API Base URL:', API_BASE_URL);

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Helper method to handle API responses
  async handleResponse(response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  // Upload PDF file to backend
  async uploadPDF(file) {
    console.log('Starting PDF upload for file:', file.name);
    console.log('Upload URL:', `${this.baseURL}/upload`);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log('Sending upload request...');
      const response = await fetch(`${this.baseURL}/upload`, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header for FormData - browser sets it with boundary
      });

      console.log('Upload response status:', response.status);
      console.log('Upload response headers:', response.headers);

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Error uploading PDF:', error);
      console.error('Network error details:', {
        message: error.message,
        stack: error.stack,
        baseURL: this.baseURL
      });
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Network error: Unable to connect to backend. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  // Send chat message to backend
  async sendMessage(payload) {
    try {
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  // Clear all stored documents
  async clearData() {
    try {
      const response = await fetch(`${this.baseURL}/clear`, {
        method: 'DELETE',
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Error clearing data:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  // Check if backend is available
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/`);
      return await this.handleResponse(response);
    } catch (error) {
      console.error('Backend health check failed:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  async saveHistory(entry) {
    try {
      const response = await fetch(`${this.baseURL}/history`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry),
      })
      return this.handleResponse(response)
    } catch (error) {
      console.error('Error saving history:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  async getHistory() {
    try {
      const response = await fetch(`${this.baseURL}/history/get`)
      return this.handleResponse(response)
    } catch (error) {
      console.error('Error getting history:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  async deleteHistory(conversationId) {
    try {
      const response = await fetch(`${this.baseURL}/history/delete/${conversationId}`, {
        method: 'DELETE',
      })
      return this.handleResponse(response)
    } catch (error) {
      console.error('Error deleting history:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  async saveFeedback(entry) {
    try {
      const response = await fetch(`${this.baseURL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry),
      })
      return this.handleResponse(response)
    } catch (error) {
      console.error('Error saving feedback:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  async saveSettings(settings) {
    try {
      const response = await fetch(`${this.baseURL}/settings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings),
      })
      return this.handleResponse(response)
    } catch (error) {
      console.error('Error saving settings:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }

  async getPDFInfo() {
    try {
      const response = await fetch(`${this.baseURL}/pdf-info`)
      return this.handleResponse(response)
    } catch (error) {
      console.error('Error getting PDF info:', error);
      
      // Provide more specific error messages
      if (error.message.includes('Failed to fetch')) {
        throw new Error('Backend server is not running or unreachable. Please check if the server is running and accessible.');
      } else if (error.message.includes('CORS')) {
        throw new Error('CORS error: Backend server is not configured to allow requests from this origin.');
      } else {
        throw error;
      }
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
