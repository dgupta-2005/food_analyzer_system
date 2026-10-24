import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Sparkles, Flame, Settings, LogOut } from 'lucide-react';

export default function Header({ todayCalories = 0 }) {
  const { user, logout, setIsProfileModalOpen } = useAuth();

  const targetCalories = user?.profile?.target_daily_calories || 2000;
  const progressPct = Math.min(Math.round((todayCalories / targetCalories) * 100), 100);

  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-logo">
          <Sparkles size={22} />
        </div>
        <div>
          <div className="brand-title">
            NutriVision <span className="brand-accent">AI</span>
          </div>
          <div className="brand-subtitle">Smart Food Intelligence &amp; Personal AI Diet Advisor</div>
        </div>
      </div>

      <div className="header-actions">
        {/* Daily Calorie Progress Pill */}
        <div
          className="calorie-tracker-badge"
          onClick={() => setIsProfileModalOpen(true)}
          title="Click to adjust your daily calorie target"
        >
          <div className="tracker-icon">
            <Flame size={16} />
          </div>
          <div className="tracker-info">
            <div className="tracker-label">TODAY'S CALORIES</div>
            <div className="tracker-value">
              <span>{todayCalories}</span> / {targetCalories} <small>kcal</small>
            </div>
          </div>
          <div className="progress-ring-mini">
            <div className="progress-fill" style={{ width: `${progressPct}%` }}></div>
          </div>
        </div>

        {/* Authenticated user controls */}
        <div className="user-profile-menu">
          <button
            className="user-btn"
            onClick={() => setIsProfileModalOpen(true)}
          >
            <div className="avatar">
              {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
            </div>
            <div className="user-details">
              <span className="user-name">{user?.full_name || 'User'}</span>
              <span className="user-role">
                {user?.profile?.primary_goal === 'weight_loss' ? '🔥 Calorie Deficit' : '💪 Active Goal'}
              </span>
            </div>
          </button>

          <button
            className="icon-btn-ghost"
            title="Profile &amp; Daily Goal Settings"
            onClick={() => setIsProfileModalOpen(true)}
          >
            <Settings size={18} />
          </button>

          <button
            className="icon-btn-ghost"
            title="Sign Out"
            onClick={logout}
          >
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}
