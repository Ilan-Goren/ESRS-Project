import api from './api';

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

// Updated interface to match the actual response structure
export interface AuthResponse {
  message: string;
  role: string;
  user: User;
  // These might be returned via headers or cookies instead of the response body
  access?: string;
  refresh?: string;
}

// Helper function to test if localStorage is working properly
const testLocalStorage = (): boolean => {
  try {
    const testKey = `test_${Date.now()}`;
    localStorage.setItem(testKey, 'test_value');
    const retrieved = localStorage.getItem(testKey);
    localStorage.removeItem(testKey);
    return retrieved === 'test_value';
  } catch (error) {
    console.error('LocalStorage test failed:', error);
    return false;
  }
};

// TokenService with direct and memory-backed options
class TokenService {
  private memoryTokens: {
    access: string | null;
    refresh: string | null;
    user: User | null;
    role: string | null;
  } = {
    access: null,
    refresh: null,
    user: null,
    role: null
  };

  private isLocalStorageWorking: boolean;

  constructor() {
    this.isLocalStorageWorking = testLocalStorage();
    console.log('LocalStorage available and working:', this.isLocalStorageWorking);
    
    // Initial attempt to load from localStorage if available
    if (this.isLocalStorageWorking) {
      try {
        const storedAccess = localStorage.getItem('access_token');
        const storedRefresh = localStorage.getItem('refresh_token');
        const storedUser = localStorage.getItem('user');
        const storedRole = localStorage.getItem('role');
        
        console.log('Initial localStorage state:', {
          access: !!storedAccess,
          refresh: !!storedRefresh,
          user: !!storedUser,
          role: !!storedRole
        });
        
        if (storedAccess) this.memoryTokens.access = storedAccess;
        if (storedRefresh) this.memoryTokens.refresh = storedRefresh;
        if (storedRole) this.memoryTokens.role = storedRole;
        if (storedUser) {
          try {
            this.memoryTokens.user = JSON.parse(storedUser);
          } catch (e) {
            console.error('Failed to parse stored user:', e);
          }
        }
      } catch (error) {
        console.error('Error loading initial tokens from localStorage:', error);
      }
    }
  }

  // Getters
  getAccessToken(): string | null {
    if (this.isLocalStorageWorking) {
      try {
        const token = localStorage.getItem('access_token');
        return token;
      } catch (error) {
        console.warn('Failed to get access token from localStorage, using memory backup:', error);
      }
    }
    return this.memoryTokens.access;
  }

  getRefreshToken(): string | null {
    if (this.isLocalStorageWorking) {
      try {
        const token = localStorage.getItem('refresh_token');
        return token;
      } catch (error) {
        console.warn('Failed to get refresh token from localStorage, using memory backup:', error);
      }
    }
    return this.memoryTokens.refresh;
  }

  getRole(): string | null {
    if (this.isLocalStorageWorking) {
      try {
        return localStorage.getItem('role');
      } catch (error) {
        console.warn('Failed to get role from localStorage, using memory backup:', error);
      }
    }
    return this.memoryTokens.role;
  }

  getUser(): User | null {
    if (this.isLocalStorageWorking) {
      try {
        const userJson = localStorage.getItem('user');
        if (userJson) {
          return JSON.parse(userJson);
        }
      } catch (error) {
        console.warn('Failed to get user from localStorage, using memory backup:', error);
      }
    }
    return this.memoryTokens.user;
  }

  // Setters
  setAccessToken(token: string): void {
    this.memoryTokens.access = token;
    
    if (this.isLocalStorageWorking) {
      try {
        localStorage.setItem('access_token', token);
        // Verify storage worked
        const storedToken = localStorage.getItem('access_token');
        if (storedToken !== token) {
          console.error('Token verification failed! Stored:', storedToken, 'Expected:', token);
        } else {
          console.log('Access token successfully stored in localStorage');
        }
      } catch (error) {
        console.error('Failed to set access token in localStorage:', error);
      }
    }
  }

  setRefreshToken(token: string): void {
    this.memoryTokens.refresh = token;
    
    if (this.isLocalStorageWorking) {
      try {
        localStorage.setItem('refresh_token', token);
        // Verify storage worked
        const storedToken = localStorage.getItem('refresh_token');
        if (storedToken !== token) {
          console.error('Token verification failed! Stored:', storedToken, 'Expected:', token);
        } else {
          console.log('Refresh token successfully stored in localStorage');
        }
      } catch (error) {
        console.error('Failed to set refresh token in localStorage:', error);
      }
    }
  }

  setRole(role: string): void {
    this.memoryTokens.role = role;
    
    if (this.isLocalStorageWorking) {
      try {
        localStorage.setItem('role', role);
        // Verify storage worked
        const storedRole = localStorage.getItem('role');
        if (storedRole !== role) {
          console.error('Role verification failed! Stored:', storedRole, 'Expected:', role);
        } else {
          console.log('Role successfully stored in localStorage');
        }
      } catch (error) {
        console.error('Failed to set role in localStorage:', error);
      }
    }
  }

  setUser(user: User): void {
    this.memoryTokens.user = user;
    
    if (this.isLocalStorageWorking) {
      try {
        const userJson = JSON.stringify(user);
        localStorage.setItem('user', userJson);
        // Verify storage worked
        const storedUserJson = localStorage.getItem('user');
        if (storedUserJson !== userJson) {
          console.error('User verification failed!');
        } else {
          console.log('User successfully stored in localStorage');
        }
      } catch (error) {
        console.error('Failed to set user in localStorage:', error);
      }
    }
  }

  isAuthenticated(): boolean {
    // Check for either tokens or role
    return (!!this.getAccessToken() || (!!this.getUser() && !!this.getRole()));
  }

  clear(): void {
    this.memoryTokens = {
      access: null,
      refresh: null,
      user: null,
      role: null
    };
    
    if (this.isLocalStorageWorking) {
      try {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('role');
        console.log('Auth data cleared from localStorage');
      } catch (error) {
        console.error('Failed to clear auth data from localStorage:', error);
      }
    }
  }
  
  // Force setting of mock tokens since they're not returned from the API
  setMockTokens(userId: number): void {
    // Generate dummy tokens if they're not provided by the API
    // but still needed for your frontend authentication flow
    const mockAccess = `mock-access-token-${userId}-${Date.now()}`;
    const mockRefresh = `mock-refresh-token-${userId}-${Date.now()}`;
    
    this.setAccessToken(mockAccess);
    this.setRefreshToken(mockRefresh);
    
    console.log('Mock tokens generated and stored');
  }
}

// Create singleton instance
const TokenStorage = new TokenService();

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  console.log('Login attempt with credentials:', { email: credentials.email });
  
  try {
    // Check if localStorage is operating normally before login
    console.log('Current localStorage state:', {
      access: localStorage.getItem('access_token'),
      refresh: localStorage.getItem('refresh_token'),
      role: localStorage.getItem('role'),
      allKeys: Object.keys(localStorage)
    });
    
    const response = await api.post('/auth/login/', {
      username: credentials.email,
      password: credentials.password,
    });
    
    console.log('Login response received:', {
      status: response.status,
      data: response.data
    });
    
    // Validate that we have the expected data structure
    if (!response.data.message || !response.data.role || !response.data.user) {
      console.error('API response missing required fields:', response.data);
      throw new Error('Login response missing required fields');
    }
    
    // Test localStorage directly with a unique key
    const testKey = `login_test_${Date.now()}`;
    try {
      localStorage.setItem(testKey, 'working');
      const testValue = localStorage.getItem(testKey);
      localStorage.removeItem(testKey);
      console.log('Direct localStorage test during login:', testValue === 'working');
    } catch (storageError) {
      console.error('Direct localStorage test failed during login:', storageError);
    }
    
    // Store user and role
    TokenStorage.setUser(response.data.user);
    TokenStorage.setRole(response.data.role);
    
    // Check for actual tokens in the response
    if (response.data.access && response.data.refresh) {
      TokenStorage.setAccessToken(response.data.access);
      TokenStorage.setRefreshToken(response.data.refresh);
    } 
    // If no tokens in response, generate mock tokens
    else {
      // Use user ID or some other unique identifier
      const userId = response.data.user.id || 1;
      TokenStorage.setMockTokens(userId);
    }
    
    // Try to extract tokens from response headers if they're not in the body
    const accessTokenHeader = response.headers['x-access-token'] || 
                              response.headers['access-token'] || 
                              response.headers['authorization'];
    
    const refreshTokenHeader = response.headers['x-refresh-token'] || 
                               response.headers['refresh-token'];
    
    if (accessTokenHeader) {
      // Remove 'Bearer ' prefix if present
      const token = accessTokenHeader.replace(/^Bearer\s+/i, '');
      TokenStorage.setAccessToken(token);
    }
    
    if (refreshTokenHeader) {
      TokenStorage.setRefreshToken(refreshTokenHeader);
    }
    
    // Verify storage immediately after setting
    console.log('Verification after login:', {
      userStored: !!localStorage.getItem('user'),
      roleStored: localStorage.getItem('role') === response.data.role,
      accessToken: !!TokenStorage.getAccessToken(),
      refreshToken: !!TokenStorage.getRefreshToken(),
      memoryUser: !!TokenStorage.getUser(),
      memoryRole: TokenStorage.getRole() === response.data.role
    });
    
    return response.data;
  } catch (error: any) {
    console.error('LOGIN ERROR', error.response?.data || error.message, error);
    throw error;
  }
};

export const logout = (): void => {
  console.log('Logout called, clearing tokens');
  TokenStorage.clear();
};

export const getCurrentUser = (): User | null => {
  const user = TokenStorage.getUser();
  if (!user) {
    console.log('No current user found');
    return null;
  }
  
  try {
    return user as User;
  } catch (error) {
    console.error('Error parsing current user:', error);
    return null;
  }
};

export const isAuthenticated = (): boolean => {
  return TokenStorage.isAuthenticated();
};

export const getRole = (): string | null => {
  return TokenStorage.getRole();
};

export const getAccessToken = (): string | null => {
  return TokenStorage.getAccessToken();
};

export default {
  login,
  logout,
  getCurrentUser,
  isAuthenticated,
  getRole,
  getAccessToken
};