import api from './api';
import TokenStorage from './TokenStorage';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'manager' | 'staff' | 'supplier';
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await api.post('/auth/login/', {
      username: credentials.email,
      password: credentials.password,
    });
    TokenStorage.setUser(response.data.user);
    TokenStorage.setAccessToken(response.data.access);
    TokenStorage.setRefreshToken(response.data.refresh);
    return response.data;
  } catch (error: any) {
    console.error('LOGIN ERROR', error.response?.data || error.message);
    throw error;
  }
};

export const logout = (): void => {
  TokenStorage.clear();
};

export const getCurrentUser = (): User | null => {
  const user = TokenStorage.getUser();
  if (!user) return null;
  try {
    return user as User;
  } catch (error) {
    return null;
  }
};