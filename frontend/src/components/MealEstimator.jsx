import React, { useState } from 'react';
import { Utensils, Upload, Image as ImageIcon, CheckCircle2, AlertCircle, Save, Loader2, Sparkles, Check } from 'lucide-react';
import apiClient from '../services/apiClient';

export default function MealEstimator({ onMealLogged }) {
  const [description, setDescription] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError(null);
    }
  };

  const handleEstimate = async (e) => {
    if (e) e.preventDefault();
    if (!description && !selectedFile) {
      setError("Please select a meal photo or type a food description.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setSaveSuccess(false);

    try {
      const data = await apiClient.meals.estimate(description, selectedFile);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to analyze meal. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveToJournal = async () => {
    if (!result) return;
    setSaving(true);
    try {
      const payload = {
        user_id: 1,
        image_url: result.image_url,
        user_description: description || result.summary_item_name,
        total_calories: result.total_calories,
        total_protein_g: result.total_protein_g,
        total_carbs_g: result.total_carbs_g,
        total_fats_g: result.total_fats_g,
        items: result.items
      };

      await apiClient.meals.logMeal(payload);
      setSaveSuccess(true);
      if (onMealLogged) onMealLogged();
    } catch (err) {
      alert("Failed to log meal to journal: " + (err.response?.data?.detail || err.message));
    } finally {
      setSaving(false);
    }
  };

  const loadPreset = (desc) => {
    setDescription(desc);
    setSelectedFile(null);
    setPreviewUrl(null);
  };

  return (
    <div className="service-page">
      <div className="page-header">
        <div className="header-pill">
          <Sparkles size={14} /> AI Vision Analysis
        </div>
        <h1 className="page-title">AI Meal Calorie & Macro Estimator</h1>
        <p className="page-description">
          Upload a food photo or describe your plate for instant portion breakdown, calories, and macro identification.
        </p>
      </div>

      <div className="grid-2col">
        {/* Input Card */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Upload size={18} className="text-primary" />
              <span>Meal Photo & Description</span>
            </div>
            <span className="badge badge-emerald">Gemini Vision AI</span>
          </div>

          <form onSubmit={handleEstimate}>
            <div className="form-group">
              <label className="form-label">Upload Food Photo (Optional)</label>
              <div 
                className="dropzone"
                onClick={() => document.getElementById('fileInput').click()}
              >
                <input 
                  type="file" 
                  id="fileInput" 
                  accept="image/*" 
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                />
                {previewUrl ? (
                  <div className="preview-container">
                    <img src={previewUrl} alt="Meal Preview" className="preview-image" />
                    <p className="preview-filename">
                      Selected: {selectedFile?.name} (Click to change)
                    </p>
                  </div>
                ) : (
                  <div className="dropzone-placeholder">
                    <ImageIcon size={40} className="drop-icon" />
                    <p className="drop-title">Drop your meal photo here or click to browse</p>
                    <p className="drop-sub">Supports JPG, PNG, WEBP food photos</p>
                  </div>
                )}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Meal Description & Portion Notes</label>
              <textarea
                className="form-textarea"
                rows="3"
                placeholder="e.g. 1 bowl of oatmeal with sliced strawberries, chia seeds, and honey"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              ></textarea>
            </div>

            <div className="preset-container">
              <div className="preset-label">Sample Meal Ideas:</div>
              <div className="preset-chips">
                <button 
                  type="button" 
                  className="chip-btn"
                  onClick={() => loadPreset("Overnight oats with chia seeds, blueberries and honey")}
                >
                  🥣 Oats & Berries
                </button>
                <button 
                  type="button" 
                  className="chip-btn"
                  onClick={() => loadPreset("Grilled chicken breast with brown rice and steamed broccoli")}
                >
                  🍗 Chicken & Rice Bowl
                </button>
                <button 
                  type="button" 
                  className="chip-btn"
                  onClick={() => loadPreset("Avocado toast on whole grain bread with poached egg")}
                >
                  🥑 Avocado Toast & Egg
                </button>
              </div>
            </div>

            {error && (
              <div className="alert alert-danger">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}

            <button 
              type="submit" 
              className="btn-primary full-width"
              disabled={loading}
              style={{ marginTop: '16px', padding: '12px' }}
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="spin" />
                  Analyzing Meal with AI...
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  Analyze Calorie & Macro Breakdown
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results Card */}
        <div>
          {result ? (
            <div className="card">
              <div className="card-header">
                <div className="card-title">
                  <CheckCircle2 size={18} className="text-emerald" />
                  <span>AI Estimation Summary</span>
                </div>
                <span className="badge badge-emerald">
                  Confidence: {Math.round(result.confidence_score * 100)}%
                </span>
              </div>

              <div className="dish-banner">
                <h2 className="dish-name">{result.summary_item_name}</h2>
                <div className="dish-subtext">Identified Food Items & Portion Breakdown</div>
              </div>

              {/* Macro Cards Grid */}
              <div className="macro-cards-grid">
                <div className="macro-box calorie">
                  <div className="macro-lbl">CALORIES</div>
                  <div className="macro-val">{result.total_calories}</div>
                  <div className="macro-unit">kcal</div>
                </div>

                <div className="macro-box protein">
                  <div className="macro-lbl">PROTEIN</div>
                  <div className="macro-val">{result.total_protein_g}g</div>
                  <div className="macro-unit">grams</div>
                </div>

                <div className="macro-box carbs">
                  <div className="macro-lbl">CARBS</div>
                  <div className="macro-val">{result.total_carbs_g}g</div>
                  <div className="macro-unit">grams</div>
                </div>

                <div className="macro-box fats">
                  <div className="macro-lbl">FATS</div>
                  <div className="macro-val">{result.total_fats_g}g</div>
                  <div className="macro-unit">grams</div>
                </div>
              </div>

              {/* Itemized Table */}
              <div className="table-block">
                <div className="table-title">Plate Component Breakdown:</div>
                <div className="table-container">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Item</th>
                        <th>Portion</th>
                        <th>Calories</th>
                        <th>Macros (P / C / F)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.items.map((item, idx) => (
                        <tr key={idx}>
                          <td style={{ fontWeight: 600 }}>{item.item_name}</td>
                          <td>{item.portion_description}</td>
                          <td><span className="text-emerald">{item.calories} kcal</span></td>
                          <td>{item.protein_g}g / {item.carbs_g}g / {item.fats_g}g</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Save to Log Button */}
              {saveSuccess ? (
                <div className="alert alert-success full-width" style={{ justifyContent: 'center' }}>
                  <Check size={18} />
                  <span>Meal Logged to Daily Food Journal!</span>
                </div>
              ) : (
                <button
                  type="button"
                  className="btn-success full-width"
                  style={{ marginTop: '16px', padding: '12px' }}
                  onClick={handleSaveToJournal}
                  disabled={saving}
                >
                  {saving ? (
                    <>
                      <Loader2 size={16} className="spin" />
                      Logging Meal...
                    </>
                  ) : (
                    <>
                      <Save size={16} /> Save Meal to Daily Food Journal
                    </>
                  )}
                </button>
              )}
            </div>
          ) : (
            <div className="card empty-card">
              <Utensils size={48} className="empty-icon-lg" />
              <h3>No Meal Analyzed Yet</h3>
              <p>Upload a food photo or select a sample meal on the left to view calories & macros.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
