import React, { useState } from 'react';
import { Target, Sparkles, Clock, AlertCircle, Loader2, Utensils, Check } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';

export default function DietPlanner() {
  const { user } = useAuth();
  const [goal, setGoal] = useState(user?.profile?.primary_goal || 'weight_loss');
  const [targetCalories, setTargetCalories] = useState(user?.profile?.target_daily_calories || 1800);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [plan, setPlan] = useState(null);

  const handleGeneratePlan = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    setPlan(null);

    const profileData = {
      id: user?.id || 1,
      user_id: user?.id || 1,
      primary_goal: goal,
      target_daily_calories: parseInt(targetCalories)
    };

    try {
      const data = await apiClient.planner.generatePlan(profileData, []);
      setPlan(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to generate diet plan. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="service-page">
      <div className="page-header">
        <div className="header-pill">
          <Sparkles size={14} /> AI Meal Planning
        </div>
        <h1 className="page-title">AI Personal Diet & Macro Planner</h1>
        <p className="page-description">
          Generate structured meal slots, target calorie allocations, and customized dish recipes aligned with your fitness goals.
        </p>
      </div>

      <div className="grid-planner">
        {/* Form Card */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Target size={18} className="text-primary" />
              <span>Goal & Calorie Preferences</span>
            </div>
            <span className="badge badge-emerald">AI Tailored</span>
          </div>

          <form onSubmit={handleGeneratePlan}>
            <div className="form-group">
              <label className="form-label">Primary Fitness & Body Goal</label>
              <select className="form-select" value={goal} onChange={(e) => setGoal(e.target.value)}>
                <option value="weight_loss">🔥 Weight Loss & Fat Burn (Caloric Deficit)</option>
                <option value="muscle_gain">💪 Muscle Building & Lean Bulk (High Protein)</option>
                <option value="maintenance">⚖️ Health Maintenance & Balanced Wellness</option>
                <option value="keto">🥑 Ketogenic Low-Carb High-Fat</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Target Daily Caloric Intake (kcal)</label>
              <input
                type="number"
                step="50"
                className="form-input"
                value={targetCalories}
                onChange={(e) => setTargetCalories(e.target.value)}
              />
            </div>

            <div className="preset-container">
              <div className="preset-label">Goal Shortcuts:</div>
              <div className="preset-chips">
                <button
                  type="button"
                  className="chip-btn"
                  onClick={() => { setGoal('weight_loss'); setTargetCalories(1600); }}
                >
                  🔥 1600 kcal Deficit
                </button>
                <button
                  type="button"
                  className="chip-btn"
                  onClick={() => { setGoal('muscle_gain'); setTargetCalories(2400); }}
                >
                  💪 2400 kcal Muscle Bulk
                </button>
                <button
                  type="button"
                  className="chip-btn"
                  onClick={() => { setGoal('maintenance'); setTargetCalories(2000); }}
                >
                  ⚖️ 2000 kcal Balance
                </button>
              </div>
            </div>

            {error && (
              <div className="alert alert-danger" style={{ marginTop: '16px' }}>
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}

            <button type="submit" className="btn-primary full-width" style={{ marginTop: '20px', padding: '12px' }} disabled={loading}>
              {loading ? (
                <>
                  <Loader2 size={18} className="spin" />
                  Generating Custom Meal Plan...
                </>
              ) : (
                <>
                  <Sparkles size={18} /> Generate Personal Diet Plan
                </>
              )}
            </button>
          </form>
        </div>

        {/* Plan Display Panel */}
        <div>
          {plan ? (
            <div className="plan-results-wrapper">
              <div className="card card-border-blue" style={{ marginBottom: '20px' }}>
                <div className="card-header">
                  <div>
                    <h2 className="plan-title">{plan.plan_title}</h2>
                    <div className="plan-subtitle">
                      Target: <strong>{plan.target_daily_calories} kcal/day</strong> • Mode: <span className="badge badge-emerald">{plan.user_goal}</span>
                    </div>
                  </div>
                  <span className="badge badge-emerald">Fresh AI Plan</span>
                </div>

                <div className="advice-box">
                  <strong>AI Nutritionist Strategy:</strong> {plan.overall_advice}
                </div>
              </div>

              {/* Daily Meal Slots */}
              <div className="meal-slots-list">
                {plan.daily_slots.map((slot, idx) => (
                  <div key={idx} className="card">
                    <div className="card-header">
                      <div className="card-title">
                        <Clock size={18} className="text-primary" />
                        <span>{slot.slot_name} Meal Slot</span>
                      </div>
                      <span className="badge badge-emerald">Target: {slot.target_calories} kcal</span>
                    </div>

                    <div className="dishes-list">
                      {slot.recommended_dishes.map((dish, dIdx) => (
                        <div key={dIdx} className="dish-card">
                          <div className="dish-card-header">
                            <span className="dish-card-title">{dish.dish_name}</span>
                            <span className="dish-card-cal">{dish.target_calories} kcal ({dish.portion_size})</span>
                          </div>
                          <div className="dish-card-macros">
                            Macros: P: <strong>{dish.protein_g}g</strong> | C: <strong>{dish.carbs_g}g</strong> | F: <strong>{dish.fats_g}g</strong>
                          </div>
                          <div className="dish-card-reason">
                            Rationale: {dish.reason}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="card empty-card">
              <Target size={48} className="empty-icon-lg" />
              <h3>No Meal Plan Generated Yet</h3>
              <p>Select your fitness goal and calorie budget on the left to generate your custom AI meal plan.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
