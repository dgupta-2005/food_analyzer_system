import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../services/apiClient';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  // null = unauthenticated; actual user object = authenticated
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('nutrivision_user');
      return (saved && saved !== 'undefined' && saved !== 'null') ? JSON.parse(saved) : null;
    } catch (e) {
      console.error('Error reading nutrivision_user from localStorage:', e);
      return null;
    }
  });

  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [authError, setAuthError] = useState(null);
  const [authLoading, setAuthLoading] = useState(false);

  // Keep localStorage in sync with authenticated user
  useEffect(() => {
    if (user) {
      localStorage.setItem('nutrivision_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('nutrivision_user');
    }
  }, [user]);

  const login = async (email, password) => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      const data = await apiClient.auth.login(email, password);
      setUser(data.user);
      return data;
    } catch (err) {
      setAuthError(err.response?.data?.detail || 'Invalid credentials. Please try again.');
      throw err;
    } finally {
      setAuthLoading(false);
    }
  };

  const register = async (email, password, fullName) => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      // Register only — do NOT setUser. User must sign in after registration.
      const newUser = await apiClient.auth.register(email, password, fullName);
      return newUser;
    } catch (err) {
      setAuthError(err.response?.data?.detail || 'Registration failed. Email may already be in use.');
      throw err;
    } finally {
      setAuthLoading(false);
    }
  };

  const updateProfile = async (profileData) => {
    if (!user || !user.id) return;
    try {
      const updatedProfile = await apiClient.auth.updateProfile(user.id, profileData);
      setUser(prev => ({
        ...prev,
        profile: updatedProfile
      }));
      setIsProfileModalOpen(false);
      return updatedProfile;
    } catch (err) {
      console.error('Failed to update user profile:', err);
      // Fallback local update if offline
      setUser(prev => ({
        ...prev,
        profile: { ...prev.profile, ...profileData }
      }));
      setIsProfileModalOpen(false);
    }
  };

  const logout = () => {
    setUser(null);
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        isAuthenticated,
        login,
        register,
        logout,
        updateProfile,
        isProfileModalOpen,
        setIsProfileModalOpen,
        authError,
        setAuthError,
        authLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
