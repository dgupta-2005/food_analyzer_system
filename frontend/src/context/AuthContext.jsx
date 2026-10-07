import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../services/apiClient';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  // Default guest user profile for seamless out-of-the-box experience
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('nutrivision_user');
    return saved ? JSON.parse(saved) : {
      id: 1,
      email: 'alex.morgan@nutrivision.ai',
      full_name: 'Alex Morgan',
      profile: {
        primary_goal: 'weight_loss',
        target_daily_calories: 2000,
        age: 28,
        weight_kg: 72,
        height_cm: 175,
        activity_level: 'moderate',
        allergies: ['Peanuts', 'Gluten Free Option'],
        dietary_preferences: ['Balanced', 'High Protein']
      }
    };
  });

  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' | 'register'
  const [authError, setAuthError] = useState(null);
  const [authLoading, setAuthLoading] = useState(false);

  useEffect(() => {
    localStorage.setItem('nutrivision_user', JSON.stringify(user));
  }, [user]);

  const login = async (email, password) => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      const data = await apiClient.auth.login(email, password);
      setUser(data.user);
      setIsAuthModalOpen(false);
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
      const newUser = await apiClient.auth.register(email, password, fullName);
      setUser(newUser);
      setIsAuthModalOpen(false);
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
    localStorage.removeItem('nutrivision_user');
    setUser({
      id: 1,
      email: 'guest@nutrivision.ai',
      full_name: 'Guest User',
      profile: {
        primary_goal: 'maintenance',
        target_daily_calories: 2000,
        allergies: [],
        dietary_preferences: ['Balanced']
      }
    });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        login,
        register,
        logout,
        updateProfile,
        isAuthModalOpen,
        setIsAuthModalOpen,
        isProfileModalOpen,
        setIsProfileModalOpen,
        authMode,
        setAuthMode,
        authError,
        setAuthError,
        authLoading
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
