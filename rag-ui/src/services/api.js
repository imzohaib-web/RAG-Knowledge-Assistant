// API Service for RAG Knowledge Assistant
// Handles communication with FastAPI backend

const API_BASE_URL = 'http://localhost:8000';

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
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${this.baseURL}/upload`, {
        method: 'POST',
        body: formData,
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Error uploading PDF:', error);
      throw error;
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
      throw error;
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
      throw error;
    }
  }

  // Check if backend is available
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/`);
      return await this.handleResponse(response);
    } catch (error) {
      console.error('Backend health check failed:', error);
      throw error;
    }
  }

  async saveHistory(entry) {
    const response = await fetch(`${this.baseURL}/history`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entry),
    })
    return this.handleResponse(response)
  }

  async getHistory() {
    const response = await fetch(`${this.baseURL}/history/get`)
    return this.handleResponse(response)
  }

  async deleteHistory(conversationId) {
    const response = await fetch(`${this.baseURL}/history/delete/${conversationId}`, {
      method: 'DELETE',
    })
    return this.handleResponse(response)
  }

  async saveFeedback(entry) {
    const response = await fetch(`${this.baseURL}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entry),
    })
    return this.handleResponse(response)
  }

  async saveSettings(settings) {
    const response = await fetch(`${this.baseURL}/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    })
    return this.handleResponse(response)
  }

  async getPDFInfo() {
    const response = await fetch(`${this.baseURL}/pdf-info`)
    return this.handleResponse(response)
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
