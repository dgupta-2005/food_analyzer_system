import React, { useState } from 'react';
import { GitCompare, ArrowRight, CheckCircle2, TrendingDown, TrendingUp, AlertCircle, Loader2, Sparkles, ShieldCheck } from 'lucide-react';
import apiClient from '../services/apiClient';

export default function ProductComparison() {
  const [origName, setOrigName] = useState('Deep Fried Potato Chips');
  const [origCal, setOrigCal] = useState(536);
  const [origSugar, setOrigSugar] = useState(5.0);
  const [origProtein, setOrigProtein] = useState(6.5);
  const [origScore, setOrigScore] = useState('E');

  const [altName, setAltName] = useState('Baked Quinoa & Oats Chips');
  const [altCal, setAltCal] = useState(380);
  const [altSugar, setAltSugar] = useState(1.2);
  const [altProtein, setAltProtein] = useState(12.0);
  const [altScore, setAltScore] = useState('A');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleCompare = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const origProd = {
      product_name: origName,
      calories_100g: parseFloat(origCal),
      sugar_100g: parseFloat(origSugar),
      protein_100g: parseFloat(origProtein),
      nutri_score: origScore
    };

    const altProd = {
      product_name: altName,
      calories_100g: parseFloat(altCal),
      sugar_100g: parseFloat(altSugar),
      protein_100g: parseFloat(altProtein),
      nutri_score: altScore
    };

    try {
      const data = await apiClient.food.compareProducts(origProd, altProd);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Product comparison failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const loadPresetPair = (preset) => {
    if (preset === 1) {
      setOrigName('Deep Fried Potato Chips');
      setOrigCal(536);
      setOrigSugar(5.0);
      setOrigProtein(6.5);
      setOrigScore('E');

      setAltName('Baked Quinoa & Oats Chips');
      setAltCal(380);
      setAltSugar(1.2);
      setAltProtein(12.0);
      setAltScore('A');
    } else if (preset === 2) {
      setOrigName('Regular Sugary Cola Soda');
      setOrigCal(160);
      setOrigSugar(39.0);
      setOrigProtein(0.0);
      setOrigScore('E');

      setAltName('Zero Sugar Sparkling Water');
      setAltCal(0);
      setAltSugar(0.0);
      setAltProtein(0.0);
      setAltScore('A');
    } else if (preset === 3) {
      setOrigName('Milk Chocolate Candy Bar');
      setOrigCal(540);
      setOrigSugar(56.0);
      setOrigProtein(7.0);
      setOrigScore('D');

      setAltName('85% Dark Cocoa Chocolate');
      setAltCal(450);
      setAltSugar(14.0);
      setAltProtein(11.0);
      setAltScore('B');
    }
  };

  return (
    <div className="service-page">
      <div className="page-header">
        <div className="header-pill">
          <Sparkles size={14} /> Smart Food Swap
        </div>
        <h1 className="page-title">Healthy Product Swap & Comparison</h1>
        <p className="page-description">
          Compare food products side-by-side to analyze calorie reduction %, sugar savings, protein gains, and AI health verdicts.
        </p>
      </div>

      <div className="preset-container" style={{ marginBottom: '20px' }}>
        <div className="preset-label">Test Food Comparisons:</div>
        <div className="preset-chips">
          <button type="button" className="chip-btn" onClick={() => loadPresetPair(1)}>
            🍟 Chips vs Baked Oats
          </button>
          <button type="button" className="chip-btn" onClick={() => loadPresetPair(2)}>
            🥤 Soda vs Zero Sparkling Water
          </button>
          <button type="button" className="chip-btn" onClick={() => loadPresetPair(3)}>
            🍫 Milk Chocolate vs 85% Dark Cocoa
          </button>
        </div>
      </div>

      <form onSubmit={handleCompare}>
        <div className="grid-2col">
          {/* Original Item */}
          <div className="card card-border-danger">
            <div className="card-header">
              <div className="card-title text-danger">
                <span>Original Food (Benchmark)</span>
              </div>
              <span className="badge badge-danger">Unhealthy Target</span>
            </div>

            <div className="form-group">
              <label className="form-label">Product Name</label>
              <input type="text" className="form-input" value={origName} onChange={(e) => setOrigName(e.target.value)} />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Calories / 100g</label>
                <input type="number" className="form-input" value={origCal} onChange={(e) => setOrigCal(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Sugar (g) / 100g</label>
                <input type="number" step="0.1" className="form-input" value={origSugar} onChange={(e) => setOrigSugar(e.target.value)} />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Protein (g) / 100g</label>
                <input type="number" step="0.1" className="form-input" value={origProtein} onChange={(e) => setOrigProtein(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Nutri-Score</label>
                <select className="form-select" value={origScore} onChange={(e) => setOrigScore(e.target.value)}>
                  <option value="A">A (Best)</option>
                  <option value="B">B</option>
                  <option value="C">C</option>
                  <option value="D">D</option>
                  <option value="E">E (Worst)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Healthier Alternative */}
          <div className="card card-border-emerald">
            <div className="card-header">
              <div className="card-title text-emerald">
                <span>Healthier Alternative Product</span>
              </div>
              <span className="badge badge-emerald">Recommended Swap</span>
            </div>

            <div className="form-group">
              <label className="form-label">Product Name</label>
              <input type="text" className="form-input" value={altName} onChange={(e) => setAltName(e.target.value)} />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Calories / 100g</label>
                <input type="number" className="form-input" value={altCal} onChange={(e) => setAltCal(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Sugar (g) / 100g</label>
                <input type="number" step="0.1" className="form-input" value={altSugar} onChange={(e) => setAltSugar(e.target.value)} />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Protein (g) / 100g</label>
                <input type="number" step="0.1" className="form-input" value={altProtein} onChange={(e) => setAltProtein(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Nutri-Score</label>
                <select className="form-select" value={altScore} onChange={(e) => setAltScore(e.target.value)}>
                  <option value="A">A (Best)</option>
                  <option value="B">B</option>
                  <option value="C">C</option>
                  <option value="D">D</option>
                  <option value="E">E (Worst)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {error && (
          <div className="alert alert-danger" style={{ marginTop: '16px' }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <button 
          type="submit" 
          className="btn-primary full-width" 
          style={{ marginTop: '20px', padding: '12px', fontSize: '15px' }} 
          disabled={loading}
        >
          {loading ? (
            <>
              <Loader2 size={18} className="spin" />
              Computing Health Deltas & Verdict...
            </>
          ) : (
            <>
              <GitCompare size={18} />
              Calculate Food Swap Comparison
            </>
          )}
        </button>
      </form>

      {/* Comparison Results Card */}
      {result && (
        <div className="card" style={{ marginTop: '24px' }}>
          <div className="card-header">
            <div className="card-title">
              <CheckCircle2 size={18} className="text-emerald" />
              <span>Smart Comparison Analytics & Verdict</span>
            </div>
            <span className="badge badge-emerald">Analytics Complete</span>
          </div>

          {/* Metric Delta Badges Grid */}
          <div className="metrics-grid three-cols" style={{ marginBottom: '20px' }}>
            <div className="metric-box green">
              <div className="metric-lbl">
                <TrendingDown size={14} /> CALORIE REDUCTION
              </div>
              <div className="metric-val">-{result.calorie_reduction_pct}%</div>
              <div className="metric-sub">Fewer calories per portion</div>
            </div>

            <div className="metric-box green">
              <div className="metric-lbl">
                <TrendingDown size={14} /> SUGAR REDUCTION
              </div>
              <div className="metric-val">-{result.sugar_reduction_pct}%</div>
              <div className="metric-sub">Drop in refined sugar</div>
            </div>

            <div className="metric-box blue">
              <div className="metric-lbl">
                <TrendingUp size={14} /> PROTEIN INCREASE
              </div>
              <div className="metric-val">+{result.protein_increase_pct}%</div>
              <div className="metric-sub">Higher dietary protein</div>
            </div>
          </div>

          {/* Verdict Banner */}
          <div className="verdict-banner">
            <div className="verdict-tag">AI Nutritionist Verdict</div>
            <div className="verdict-text">{result.summary_verdict}</div>
          </div>

          {/* Comparison Table */}
          <div className="table-container" style={{ marginTop: '20px' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Nutrient Metric</th>
                  <th className="text-danger">Original ({result.original_product.product_name})</th>
                  <th className="text-emerald">Swap Alternative ({result.alternative_product.product_name})</th>
                  <th>Nutritional Benefit</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ fontWeight: 600 }}>Calories (per 100g)</td>
                  <td>{result.original_product.calories_100g} kcal</td>
                  <td>{result.alternative_product.calories_100g} kcal</td>
                  <td className="text-emerald font-semibold">-{result.original_product.calories_100g - result.alternative_product.calories_100g} kcal savings</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600 }}>Sugar (per 100g)</td>
                  <td>{result.original_product.sugar_100g} g</td>
                  <td>{result.alternative_product.sugar_100g} g</td>
                  <td className="text-emerald font-semibold">-{(result.original_product.sugar_100g - result.alternative_product.sugar_100g).toFixed(1)} g less sugar</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600 }}>Protein (per 100g)</td>
                  <td>{result.original_product.protein_100g} g</td>
                  <td>{result.alternative_product.protein_100g} g</td>
                  <td className="text-blue font-semibold">+{(result.alternative_product.protein_100g - result.original_product.protein_100g).toFixed(1)} g more protein</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600 }}>Nutri-Score Rating</td>
                  <td><span className="badge badge-danger">{result.original_product.nutri_score}</span></td>
                  <td><span className="badge badge-emerald">{result.alternative_product.nutri_score}</span></td>
                  <td className="text-emerald font-semibold">Upgraded Grade</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
