import React, { useState, useEffect } from 'react';
import { AuthProvider } from './context/AuthContext';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import MealEstimator from './components/MealEstimator';
import BarcodeScanner from './components/BarcodeScanner';
import ProductComparison from './components/ProductComparison';
import DietPlanner from './components/DietPlanner';
import MealHistory from './components/MealHistory';
import AuthModal from './components/AuthModal';
import ProfileModal from './components/ProfileModal';
import './App.css';
import apiClient from './services/apiClient';

function AppContent() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [todayCalories, setTodayCalories] = useState(1450);

  // Fetch recent meal history to compute live daily calorie totals
  const refreshCalories = async () => {
    try {
      const logs = await apiClient.meals.getHistory(1);
      const sum = logs.reduce((acc, curr) => acc + (curr.total_calories || 0), 0);
      setTodayCalories(sum);
    } catch (e) {
      // Fallback
    }
  };

  useEffect(() => {
    refreshCalories();
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard setActiveTab={setActiveTab} />;
      case 'estimator':
        return <MealEstimator onMealLogged={refreshCalories} />;
      case 'barcode':
        return <BarcodeScanner />;
      case 'compare':
        return <ProductComparison />;
      case 'planner':
        return <DietPlanner />;
      case 'history':
        return <MealHistory />;
      default:
        return <Dashboard setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="app-container">
      <Header todayCalories={todayCalories} />

      <div className="app-main">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="app-content">
          {renderContent()}
        </main>
      </div>

      <footer className="app-footer">
        <div>
          <strong>NutriVision AI Intelligence Platform</strong> © {new Date().getFullYear()} • Empowering Healthy Living Through Vision AI
        </div>
        <div>
          Nutritive Score Engine & Smart Macro Analytics
        </div>
      </footer>

      {/* Global User Auth & Profile Modals */}
      <AuthModal />
      <ProfileModal />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
