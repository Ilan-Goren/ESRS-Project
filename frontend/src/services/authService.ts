import api from './api';

export interface LoginCredentials {
  email: string;
  password: string;
  role?: string;  // Added optional role parameter
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'manager' | 'staff' | 'supplier';
}

// Updated interface to match the actual response structure
export interface AuthResponse {
  message: string;
  role: string;
  user: User;
  token?: string;
  access?: string;
  refresh?: string;
}

const storeToken = (token: string): void => {
  try {
    localStorage.setItem('access_token', token);
    console.log('Token stored successfully');
  } catch (error) {
    console.error('Failed to store token:', error);
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
      role: credentials.role  // This will be passed to the backend
    });

    console.log('Login response:', response.status);

    if (response.data.token) {
      storeToken(response.data.token);
    } else if (response.data.access) {
      storeToken(response.data.access);
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
  const user = getCurrentUser();
  const role = localStorage.getItem('role');
  return !!user && !!role;
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