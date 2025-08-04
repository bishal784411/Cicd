// services/apiService.ts
class ApiService {
  private baseURL: string;
  private getAuthHeaders: () => Record<string, string> | null;

  constructor(baseURL: string, getAuthHeaders: () => Record<string, string> | null) {
    this.baseURL = baseURL;
    this.getAuthHeaders = getAuthHeaders;
  }

  private async request(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<any> {
    const url = `${this.baseURL}${endpoint}`;
    const authHeaders = this.getAuthHeaders();
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (response.status === 401) {
        // Token expired or invalid, trigger logout
        localStorage.removeItem('devops-jwt-token');
        localStorage.removeItem('devops-user');
        window.location.href = '/loginpage';
        throw new Error('Authentication failed');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // GET request
  async get(endpoint: string): Promise<any> {
    return this.request(endpoint, { method: 'GET' });
  }

  // POST request
  async post(endpoint: string, data: any): Promise<any> {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // PUT request
  async put(endpoint: string, data: any): Promise<any> {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // DELETE request
  async delete(endpoint: string): Promise<any> {
    return this.request(endpoint, { method: 'DELETE' });
  }

  // Specific auth endpoints
  async login(credentials: { email: string; password: string }) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

}

// Create a singleton instance
let apiServiceInstance: ApiService | null = null;

export const createApiService = (getAuthHeaders: () => Record<string, string> | null) => {
  if (!apiServiceInstance) {
    apiServiceInstance = new ApiService('http://localhost:5000/api', getAuthHeaders);
  }
  return apiServiceInstance;
};

export default ApiService;