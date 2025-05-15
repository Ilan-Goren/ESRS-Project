import api from './api';

export interface LoginCredentials {
  email: string;
  password: string;
  role?: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'manager' | 'staff' | 'supplier';
}

export interface AuthResponse {
  message: string;
  role: string;
  user: User;
  token?: string;
  access?: string;
  refresh?: string;
}

const storeTokens = (access: string, refresh?: string): void => {
  try {
    localStorage.setItem('access_token', access);
    if (refresh) {
      localStorage.setItem('refresh_token', refresh);
    }
    console.log('Tokens stored successfully');
  } catch (error) {
    console.error('Failed to store tokens:', error);
  }
};

export const login = async (credentials: LoginCredentials): Promise<User> => {
  try {
    // Log the login attempt with selected role (if any)
    console.log('Login attempt:', { 
      email: credentials.email, 
      role: credentials.role || 'not specified' 
    });
    
    // Pass all credentials to the API, including the role if provided
    const response = await api.post<AuthResponse>('/auth/login/', {
      username: credentials.email,
      password: credentials.password,
      role: credentials.role
    });

    console.log('Login response:', response.status);

    // Handle different token response formats
    if (response.data.token) {
      storeTokens(response.data.token);
    } else if (response.data.access) {
      storeTokens(response.data.access, response.data.refresh);
    }

    if (response.data.user) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    if (response.data.role) {
      localStorage.setItem('role', response.data.role);
      console.log('Role stored:', response.data.role);
    }

    return response.data.user;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const logout = (): void => {
  console.log('Logout called, clearing tokens');
  try {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('role');
    console.log('Auth data cleared from localStorage');
  } catch (error) {
    console.error('Failed to clear auth data from localStorage:', error);
  }
};

export const getCurrentUser = (): User | null => {
  const userJson = localStorage.getItem('user');
  if (!userJson) {
    console.log('No current user found');
    return null;
  }
  
  try {
    return JSON.parse(userJson) as User;
  } catch (error) {
    console.error('Error parsing current user:', error);
    return null;
  }
};

export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('access_token');
  const user = getCurrentUser();
  return !!token && !!user;
};

export const getRole = (): string | null => {
  return localStorage.getItem('role');
};

export default {
  login,
  logout,
  getCurrentUser,
  isAuthenticated,
  getRole
};