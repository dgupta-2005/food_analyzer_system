import React from 'react';
import { 
  LayoutDashboard, 
  Utensils, 
  Barcode, 
  GitCompare, 
  Target, 
  BookOpen, 
  UserCheck,
  Sparkles,
  ChevronRight
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Sidebar({ activeTab, setActiveTab }) {
  const { user, setIsProfileModalOpen } = useAuth();

  const menuItems = [
    { id: 'dashboard', label: 'Nutrition Dashboard', icon: LayoutDashboard, badge: 'Live' },
    { id: 'estimator', label: 'AI Meal Estimator', icon: Utensils, badge: 'Vision AI' },
    { id: 'barcode', label: 'Barcode Food Scanner', icon: Barcode, badge: 'Smart' },
    { id: 'compare', label: 'Healthy Swap Engine', icon: GitCompare, badge: 'Compare' },
    { id: 'planner', label: 'AI Meal & Diet Planner', icon: Target, badge: 'Planner' },
    { id: 'history', label: 'Daily Food Journal', icon: BookOpen },
  ];

  return (
    <aside className="app-sidebar">
      <div className="sidebar-section-title">Navigation Services</div>
      
      <div className="nav-group">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <div className="nav-item-content">
                <Icon size={18} className="nav-icon" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className={`nav-badge ${isActive ? 'active-badge' : ''}`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* User Goal Card Banner at bottom */}
      <div className="sidebar-goal-card" onClick={() => setIsProfileModalOpen(true)}>
        <div className="goal-card-header">
          <div className="goal-icon-wrapper">
            <UserCheck size={16} />
          </div>
          <div>
            <div className="goal-card-title">Daily Goal Active</div>
            <div className="goal-card-subtitle">
              {user?.profile?.target_daily_calories || 2000} kcal • {user?.profile?.primary_goal === 'weight_loss' ? 'Fat Loss' : 'Muscle Gain'}
            </div>
          </div>
        </div>
        <div className="goal-card-footer">
          <span>Edit Preferences</span>
          <ChevronRight size={14} />
        </div>
      </div>
    </aside>
  );
}
