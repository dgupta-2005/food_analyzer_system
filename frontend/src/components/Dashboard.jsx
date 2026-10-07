import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Flame, 
  Utensils, 
  Barcode, 
  GitCompare, 
  Target, 
  Sparkles, 
  TrendingUp, 
  CheckCircle2, 
  ArrowRight,
  ShieldCheck,
  Plus,
  Zap
} from 'lucide-react';
import apiClient from '../services/apiClient';

export default function Dashboard({ setActiveTab, onMealSelect }) {
  const { user, setIsProfileModalOpen } = useAuth();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.meals.getHistory(user?.id || 1)
      .then(data => setLogs(data))
      .catch(() => setLogs([]))
      .finally(() => setLoading(false));
  }, [user]);

  // Compute today's total macros
  const totalCaloriesToday = logs.reduce((acc, curr) => acc + (curr.total_calories || 0), 0);
  const totalProteinToday = logs.reduce((acc, curr) => acc + (curr.total_protein_g || 0), 0);
  const totalCarbsToday = logs.reduce((acc, curr) => acc + (curr.total_carbs_g || 0), 0);
  const totalFatsToday = logs.reduce((acc, curr) => acc + (curr.total_fats_g || 0), 0);

  const targetCalories = user?.profile?.target_daily_calories || 2000;
  const targetProtein = Math.round((targetCalories * 0.3) / 4); // 30% protein target
  const targetCarbs = Math.round((targetCalories * 0.45) / 4);  // 45% carbs target
  const targetFats = Math.round((targetCalories * 0.25) / 9);   // 25% fats target

  const caloriePct = Math.min(Math.round((totalCaloriesToday / targetCalories) * 100), 100);

  return (
    <div className="dashboard-container">
      {/* Welcome Banner */}
      <div className="dashboard-hero">
        <div className="hero-content">
          <div className="hero-pill">
            <Sparkles size={14} /> AI Nutrition Command Center
          </div>
          <h1 className="hero-title">
            Welcome back, <span className="text-gradient">{user?.full_name || 'Nutrition Explorer'}</span>
          </h1>
          <p className="hero-subtitle">
            Track your calories, analyze food photos with AI, and achieve your daily {user?.profile?.primary_goal === 'weight_loss' ? 'weight loss' : 'fitness'} targets.
          </p>
        </div>

        <div className="hero-stats">
          <button className="btn-glass" onClick={() => setIsProfileModalOpen(true)}>
            <Target size={16} />
            <span>Target: {targetCalories} kcal</span>
          </button>
        </div>
      </div>

      {/* Main Metric Cards Grid */}
      <div className="metrics-grid">
        {/* Calorie Goal Card */}
        <div className="metric-card hero-metric">
          <div className="metric-card-header">
            <span className="metric-title">Daily Calorie Budget</span>
            <span className="badge badge-emerald">{caloriePct}% Completed</span>
          </div>
          <div className="metric-main-value">
            <span className="val">{totalCaloriesToday}</span>
            <span className="total">/ {targetCalories} kcal</span>
          </div>

          <div className="progress-bar-container">
            <div className="progress-bar-fill" style={{ width: `${caloriePct}%` }}></div>
          </div>

          <div className="metric-sub-info">
            <span>Remaining: <strong>{Math.max(0, targetCalories - totalCaloriesToday)} kcal</strong></span>
            <button className="text-link" onClick={() => setActiveTab('estimator')}>+ Add Meal</button>
          </div>
        </div>

        {/* Protein Macro Card */}
        <div className="metric-card">
          <div className="metric-card-header">
            <span className="metric-title">Protein Target</span>
            <span className="badge badge-blue">Muscle & Recovery</span>
          </div>
          <div className="metric-main-value">
            <span className="val">{Math.round(totalProteinToday)}g</span>
            <span className="total">/ {targetProtein}g</span>
          </div>
          <div className="progress-bar-container">
            <div 
              className="progress-bar-fill bg-blue" 
              style={{ width: `${Math.min(100, Math.round((totalProteinToday / targetProtein) * 100))}%` }}
            ></div>
          </div>
          <div className="metric-sub-info">
            <span>Progress: <strong>{Math.round((totalProteinToday / targetProtein) * 100)}%</strong></span>
          </div>
        </div>

        {/* Carbs Macro Card */}
        <div className="metric-card">
          <div className="metric-card-header">
            <span className="metric-title">Carbohydrates</span>
            <span className="badge badge-amber">Energy Source</span>
          </div>
          <div className="metric-main-value">
            <span className="val">{Math.round(totalCarbsToday)}g</span>
            <span className="total">/ {targetCarbs}g</span>
          </div>
          <div className="progress-bar-container">
            <div 
              className="progress-bar-fill bg-amber" 
              style={{ width: `${Math.min(100, Math.round((totalCarbsToday / targetCarbs) * 100))}%` }}
            ></div>
          </div>
          <div className="metric-sub-info">
            <span>Progress: <strong>{Math.round((totalCarbsToday / targetCarbs) * 100)}%</strong></span>
          </div>
        </div>

        {/* Fats Macro Card */}
        <div className="metric-card">
          <div className="metric-card-header">
            <span className="metric-title">Healthy Fats</span>
            <span className="badge badge-purple">Hormone Health</span>
          </div>
          <div className="metric-main-value">
            <span className="val">{Math.round(totalFatsToday)}g</span>
            <span className="total">/ {targetFats}g</span>
          </div>
          <div className="progress-bar-container">
            <div 
              className="progress-bar-fill bg-purple" 
              style={{ width: `${Math.min(100, Math.round((totalFatsToday / targetFats) * 100))}%` }}
            ></div>
          </div>
          <div className="metric-sub-info">
            <span>Progress: <strong>{Math.round((totalFatsToday / targetFats) * 100)}%</strong></span>
          </div>
        </div>
      </div>

      {/* Quick Launch Services Grid */}
      <div className="section-block">
        <div className="section-header">
          <h2>Smart AI Nutrition Services</h2>
          <p>Instant photo analysis, barcode lookup, healthy product swaps, and meal planning.</p>
        </div>

        <div className="services-action-grid">
          <div className="service-action-card" onClick={() => setActiveTab('estimator')}>
            <div className="action-icon-bg bg-emerald">
              <Utensils size={24} />
            </div>
            <div className="action-title">AI Meal Estimator</div>
            <div className="action-desc">Upload food photo or describe your plate for instant AI calorie & macro estimation.</div>
            <div className="action-footer">
              <span>Analyze Food</span> <ArrowRight size={14} />
            </div>
          </div>

          <div className="service-action-card" onClick={() => setActiveTab('barcode')}>
            <div className="action-icon-bg bg-blue">
              <Barcode size={24} />
            </div>
            <div className="action-title">Barcode & Food Scanner</div>
            <div className="action-desc">Scan product barcodes or search packaging to view Nutri-Score & allergen flags.</div>
            <div className="action-footer">
              <span>Scan Barcode</span> <ArrowRight size={14} />
            </div>
          </div>

          <div className="service-action-card" onClick={() => setActiveTab('compare')}>
            <div className="action-icon-bg bg-purple">
              <GitCompare size={24} />
            </div>
            <div className="action-title">Healthy Swap Engine</div>
            <div className="action-desc">Compare food products side-by-side to discover lower-calorie & lower-sugar alternatives.</div>
            <div className="action-footer">
              <span>Compare Items</span> <ArrowRight size={14} />
            </div>
          </div>

          <div className="service-action-card" onClick={() => setActiveTab('planner')}>
            <div className="action-icon-bg bg-amber">
              <Target size={24} />
            </div>
            <div className="action-title">AI Diet Planner</div>
            <div className="action-desc">Generate tailored meal plans aligned with your target daily calories and diet preferences.</div>
            <div className="action-footer">
              <span>Generate Plan</span> <ArrowRight size={14} />
            </div>
          </div>
        </div>
      </div>

      {/* Recent Meal Journal Stream */}
      <div className="section-block">
        <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>Today's Logged Meals</h2>
            <p>Your recent food journal logs and nutritional history.</p>
          </div>
          <button className="btn-secondary" onClick={() => setActiveTab('history')}>
            View Full Journal ({logs.length})
          </button>
        </div>

        {logs.length > 0 ? (
          <div className="recent-meals-list">
            {logs.slice(0, 4).map((log) => (
              <div key={log.id} className="meal-log-card">
                <div className="meal-log-info">
                  <div className="meal-log-icon">
                    <Utensils size={18} />
                  </div>
                  <div>
                    <div className="meal-log-title">{log.user_description || 'Logged Meal'}</div>
                    <div className="meal-log-time">
                      {new Date(log.logged_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>

                <div className="meal-log-stats">
                  <span className="badge badge-emerald">{log.total_calories} kcal</span>
                  <div className="macro-pills">
                    <span>P: <strong>{log.total_protein_g}g</strong></span>
                    <span>C: <strong>{log.total_carbs_g}g</strong></span>
                    <span>F: <strong>{log.total_fats_g}g</strong></span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state-card">
            <Utensils size={36} className="empty-icon" />
            <h3>No meals logged today yet</h3>
            <p>Snap a picture of your food or search for items to start tracking your daily progress.</p>
            <button className="btn-primary" onClick={() => setActiveTab('estimator')}>
              <Plus size={16} /> Log First Meal
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
