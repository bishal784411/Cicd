// import { useState, useEffect, createContext, useContext } from 'react';

// interface User {
//   email: string;
//   name: string;
//   role: string;
// }

// interface AuthContextType {
//   user: User | null;
//   isAuthenticated: boolean;
//   login: (user: User) => void;
//   logout: () => void;
//   isLoading: boolean;
// }

// const AuthContext = createContext<AuthContextType | undefined>(undefined);

// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (context === undefined) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };

// export const useAuthProvider = () => {
//   const [user, setUser] = useState<User | null>(null);
//   const [isLoading, setIsLoading] = useState(true);

//   useEffect(() => {
//     // Check for stored authentication on app load
//     const storedUser = localStorage.getItem('devops-user');
//     if (storedUser) {
//       try {
//         setUser(JSON.parse(storedUser));
//       } catch (error) {
//         console.error('Error parsing stored user:', error);
//         localStorage.removeItem('devops-user');
//       }
//     }
//     setIsLoading(false);
//   }, []);

//   const login = (userData: User) => {
//     setUser(userData);
//     localStorage.setItem('devops-user', JSON.stringify(userData));
//   };

//   const logout = () => {
//     setUser(null);
//     localStorage.removeItem('devops-user');
//   };

//   return {
//     user,
//     isAuthenticated: !!user,
//     login,
//     logout,
//     isLoading
//   };
// };

// export { AuthContext };


import { createContext, useContext, useState, useEffect } from 'react';

// Types
export interface User {
  email: string;
  name: string;
  role: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

// Create context
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// API configuration
// const API_BASE_URL = 'http://localhost:5000/api'; // Adjust this to match your backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

console.log("here", API_BASE_URL)
// Auth API functions
const authAPI = {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for HTTP-only cookie handling
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Login failed');
    }

    return response.json();
  },

  async verifyToken(token: string): Promise<boolean> {
    try {
      // You might want to create a verify endpoint in your FastAPI backend
      // For now, we'll use a simple approach by trying to decode the token
      const response = await fetch(`${API_BASE_URL}/auth/verify`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        credentials: 'include',
      });

      return response.ok;
    } catch {
      return false;
    }
  }
};

// Token management utilities
const TOKEN_KEY = 'access_token';

const tokenManager = {
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  },

  setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  },

  removeToken(): void {
    localStorage.removeItem(TOKEN_KEY);
  },

  // Parse JWT token to extract user info (basic parsing, consider using a JWT library)
  parseToken(token: string): any {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch {
      return null;
    }
  },

  isTokenExpired(token: string): boolean {
    const payload = this.parseToken(token);
    if (!payload || !payload.exp) return true;
    
    const currentTime = Date.now() / 1000;
    return payload.exp < currentTime;
  }
};

// Main auth provider hook
export const useAuthProvider = (): AuthContextType => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user;

  // Convert email to user object (you might want to fetch this from your backend)
  const createUserFromEmail = (email: string): User => {
    // This is a basic implementation - ideally you'd fetch user details from your backend
    const name = email.split('@')[0].replace(/[._]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    return {
      email,
      name,
      role: 'Administrator' // You might want to fetch this from your backend
    };
  };

  const login = async (credentials: LoginCredentials): Promise<void> => {
    setIsLoading(true);
    try {
      const response = await authAPI.login(credentials);
      
      // Store the token
      tokenManager.setToken(response.access_token);
      
      // Create user object from email (in the token payload)
      const payload = tokenManager.parseToken(response.access_token);
      if (payload && payload.sub) {
        const userData = createUserFromEmail(payload.sub);
        setUser(userData);
      }
    } catch (error) {
      tokenManager.removeToken();
      setUser(null);
      throw error; // Re-throw so the login component can handle the error
    } finally {
      setIsLoading(false);
    }
  };

  const logout = (): void => {
    tokenManager.removeToken();
    setUser(null);
    
    // Optional: Call logout endpoint to invalidate token on server
    fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    }).catch(() => {
      // Ignore errors, we're logging out anyway
    });
  };

  const checkAuth = async (): Promise<void> => {
    setIsLoading(true);
    try {
      const token = tokenManager.getToken();
      
      if (!token) {
        setUser(null);
        return;
      }

      // Check if token is expired
      if (tokenManager.isTokenExpired(token)) {
        tokenManager.removeToken();
        setUser(null);
        return;
      }

      // For better UX, we can trust the token if it's not expired
      // and skip the server verification for faster loading
      const payload = tokenManager.parseToken(token);
      if (payload && payload.sub) {
        const userData = createUserFromEmail(payload.sub);
        setUser(userData);
      }

      // Optional: Verify token with backend in the background
      // This is good for security but adds latency
      /*
      const isValid = await authAPI.verifyToken(token);
      if (!isValid) {
        tokenManager.removeToken();
        setUser(null);
      }
      */
    } catch (error) {
      console.error('Auth check failed:', error);
      tokenManager.removeToken();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Check authentication status on mount and when the page becomes visible
  useEffect(() => {
    checkAuth();

    // Optional: Re-check auth when the user returns to the tab
    const handleVisibilityChange = () => {
      if (!document.hidden && user) {
        checkAuth();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  // Set up axios interceptor or fetch interceptor to automatically include the token
  useEffect(() => {
    const token = tokenManager.getToken();
    if (token) {
      // You can set up global axios defaults here if you're using axios
      // axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, [user]);

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    checkAuth,
  };
};

// Hook for consuming auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// HTTP client utility with automatic token inclusion
export const createAuthenticatedFetch = () => {
  return async (url: string, options: RequestInit = {}): Promise<Response> => {
    const token = tokenManager.getToken();
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      credentials: 'include',
    };

    const response = await fetch(url, config);

    // If we get a 401, the token might be expired
    if (response.status === 401) {
      tokenManager.removeToken();
      // You might want to redirect to login or trigger a logout here
      window.location.href = '/loginpage';
    }

    return response;
  };
};

// Export the authenticated fetch instance
export const authFetch = createAuthenticatedFetch();