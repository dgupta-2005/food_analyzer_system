import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { X, Target, User, Flame, Activity, ShieldAlert, Check, Save } from 'lucide-react';

export default function ProfileModal() {
  const { isProfileModalOpen, setIsProfileModalOpen, user, updateProfile } = useAuth();

  const profile = user?.profile || {};

  const [primaryGoal, setPrimaryGoal] = useState(profile.primary_goal || 'weight_loss');
  const [targetCalories, setTargetCalories] = useState(profile.target_daily_calories || 2000);
  const [age, setAge] = useState(profile.age || 28);
  const [weightKg, setWeightKg] = useState(profile.weight_kg || 72);
  const [heightCm, setHeightCm] = useState(profile.height_cm || 175);
  const [allergies, setAllergies] = useState(profile.allergies ? profile.allergies.join(', ') : 'Peanuts, Gluten Free Option');
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (user?.profile) {
      setPrimaryGoal(user.profile.primary_goal || 'weight_loss');
      setTargetCalories(user.profile.target_daily_calories || 2000);
      setAge(user.profile.age || 28);
      setWeightKg(user.profile.weight_kg || 72);
      setHeightCm(user.profile.height_cm || 175);
      if (Array.isArray(user.profile.allergies)) {
        setAllergies(user.profile.allergies.join(', '));
      }
    }
  }, [user]);

  if (!isProfileModalOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const allergyList = allergies ? allergies.split(',').map(s => s.trim()).filter(Boolean) : [];
    await updateProfile({
      primary_goal: primaryGoal,
      target_daily_calories: parseInt(targetCalories),
      age: parseInt(age),
      weight_kg: parseFloat(weightKg),
      height_cm: parseFloat(heightCm),
      allergies: allergyList
    });
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  return (
    <div className="modal-overlay" onClick={() => setIsProfileModalOpen(false)}>
      <div className="modal-card modal-large" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={() => setIsProfileModalOpen(false)}>
          <X size={20} />
        </button>

        <div className="modal-header">
          <div className="brand-badge">
            <Target size={16} /> Personal Nutrition Targets
          </div>
          <h2>Personal Health & Goal Profile</h2>
          <p>Customize your daily calorie deficit, target macros, and dietary restrictions.</p>
        </div>

        {savedSuccess && (
          <div className="alert alert-success" style={{ marginBottom: '16px' }}>
            <Check size={16} />
            <span>Profile goals updated successfully!</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Primary Fitness & Body Goal</label>
              <select
                className="form-select"
                value={primaryGoal}
                onChange={(e) => setPrimaryGoal(e.target.value)}
              >
                <option value="weight_loss">🔥 Weight Loss & Fat Burn (Caloric Deficit)</option>
                <option value="muscle_gain">💪 Lean Muscle Building (High Protein Surplus)</option>
                <option value="maintenance">⚖️ Overall Health & Weight Maintenance</option>
                <option value="keto">🥑 Ketogenic Low-Carb Fat Focus</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Target Daily Calorie Intake (kcal)</label>
              <div className="input-with-icon">
                <Flame size={18} className="input-icon" />
                <input
                  type="number"
                  step="50"
                  className="form-input"
                  value={targetCalories}
                  onChange={(e) => setTargetCalories(e.target.value)}
                  required
                />
              </div>
            </div>
          </div>

          <div className="form-row three-cols">
            <div className="form-group">
              <label className="form-label">Age (Years)</label>
              <input
                type="number"
                className="form-input"
                value={age}
                onChange={(e) => setAge(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Weight (kg)</label>
              <input
                type="number"
                step="0.1"
                className="form-input"
                value={weightKg}
                onChange={(e) => setWeightKg(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Height (cm)</label>
              <input
                type="number"
                className="form-input"
                value={heightCm}
                onChange={(e) => setHeightCm(e.target.value)}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Food Allergies & Intolerances (Comma Separated)</label>
            <div className="input-with-icon">
              <ShieldAlert size={18} className="input-icon" />
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Peanuts, Gluten, Dairy, Shellfish"
                value={allergies}
                onChange={(e) => setAllergies(e.target.value)}
              />
            </div>
          </div>

          <div className="modal-actions" style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '24px' }}>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => setIsProfileModalOpen(false)}
            >
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              <Save size={16} /> Save Profile Goals
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
