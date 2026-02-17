import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { jwtDecode } from "jwt-decode";
import { api } from '@/services/api';

interface User {
  id: number;
  email: string;
  full_name: string;
  is_verified: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string) => void;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [isLoading, setIsLoading] = useState(true);

  // We can't use useNavigate here directly if AuthProvider is outside Router
  // But usually it's inside. Let's assume it is inside or we handle redirect in components.

  useEffect(() => {
    if (token) {
      try {
        jwtDecode(token);
        // We might want to fetch full user details from backend here
        // For now, let's just use what we have or fetch /users/me
        fetchUser(token);
      } catch (e) {
        // Invalid token, logout synchronously
        logoutSync();
      }
    } else {
      setIsLoading(false);
    }
  }, [token]);

  const fetchUser = async (authToken: string) => {
    try {
      const userData = await api.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      // Error fetching user, logout synchronously
      logoutSync();
    } finally {
      setIsLoading(false);
    }
  };

  const login = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    // fetchUser will be called by useEffect
  };

  // Synchronous logout for internal use
  const logoutSync = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setIsLoading(false);
  };

  // Async logout for external use (from UI)
  const logout = async () => {
    try {
      // Call backend logout endpoint
      await api.logout();
    } catch (error) {
      console.error('Backend logout error:', error);
    } finally {
      // Always clear local state and storage
      logoutSync();
    }
  };

  const value = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!user,
    isLoading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
