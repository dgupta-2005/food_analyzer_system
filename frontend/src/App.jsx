import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import MealEstimator from './components/MealEstimator';
import BarcodeScanner from './components/BarcodeScanner';
import ProductComparison from './components/ProductComparison';
import MealHistory from './components/MealHistory';
import ProfileModal from './components/ProfileModal';
import AuthPage from './components/AuthPage';
import './App.css';
import apiClient from './services/apiClient';

// ── Authenticated app shell ────────────────────────────────────────────────
function AppContent() {
  const { user, isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [todayCalories, setTodayCalories] = useState(0);
  const [refreshKey, setRefreshKey] = useState(0);

  const refreshCalories = async () => {
    try {
      const targetId = user?.id || 1;
      const logs = await apiClient.meals.getHistory(targetId);
      const sum = logs.reduce((acc, curr) => acc + (curr.total_calories || 0), 0);
      setTodayCalories(sum);
      setRefreshKey(k => k + 1);
    } catch (_) {
      // silent
    }
  };

  useEffect(() => {
    if (isAuthenticated) refreshCalories();
  }, [isAuthenticated, user?.id]);

  // ── Guard: show login/signup page for unauthenticated visitors ──────────
  if (!isAuthenticated) {
    return <AuthPage />;
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard': return <Dashboard key={refreshKey} setActiveTab={setActiveTab} />;
      case 'estimator': return <MealEstimator onMealLogged={refreshCalories} />;
      case 'barcode':   return <BarcodeScanner />;
      case 'compare':   return <ProductComparison />;
      case 'history':   return <MealHistory key={refreshKey} />;
      default:          return <Dashboard key={refreshKey} setActiveTab={setActiveTab} />;
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
          <strong>NutriVision AI Intelligence Platform</strong> © {new Date().getFullYear()} · Empowering Healthy Living Through Vision AI
        </div>
        <div>Nutritive Score Engine &amp; Smart Macro Analytics</div>
      </footer>

      {/* Profile settings modal (only for authenticated users) */}
      <ProfileModal />
    </div>
  );
}

// ── Root: wraps everything in the auth provider ───────────────────────────
export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
