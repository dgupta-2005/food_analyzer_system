import React, { useState, useRef, useEffect } from 'react';
import {
  GitCompare, Search, CheckCircle2, TrendingDown, TrendingUp,
  AlertCircle, Loader2, Sparkles, X, ArrowRightLeft, Zap, ChevronDown, ChevronRight
} from 'lucide-react';
import apiClient from '../services/apiClient';

/* ── Nutri-Score color helper ─────────────────────────────── */
const nutriColor = (s) => {
  if (!s) return { bg: 'rgba(255,255,255,0.08)', text: '#aaa' };
  const map = {
    A: { bg: 'rgba(34,197,94,0.15)', text: '#4ade80' },
    B: { bg: 'rgba(132,204,22,0.12)', text: '#a3e635' },
    C: { bg: 'rgba(250,204,21,0.12)', text: '#facc15' },
    D: { bg: 'rgba(251,146,60,0.12)', text: '#fb923c' },
    E: { bg: 'rgba(239,68,68,0.12)', text: '#f87171' },
  };
  return map[s.toUpperCase()] || map.C;
};

/* ── Product Search Input component ───────────────────────── */
function ProductSearchInput({ label, placeholder, onProductSelected, accentColor = '#a0a0a0' }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [searching, setSearching] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const debounceRef = useRef(null);
  const containerRef = useRef(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const handleSearch = (val) => {
    setQuery(val);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (val.length < 2) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }
    debounceRef.current = setTimeout(async () => {
      setSearching(true);
      try {
        const results = await apiClient.food.searchProducts(val);
        setSuggestions(results.slice(0, 8));
        setShowDropdown(true);
      } catch {
        setSuggestions([]);
      } finally {
        setSearching(false);
      }
    }, 400);
  };

  const pickProduct = (product) => {
    setQuery(product.product_name);
    setShowDropdown(false);
    onProductSelected(product);
  };

  return (
    <div className="pc-search-wrap" ref={containerRef}>
      <label className="form-label">{label}</label>
      <div className="pc-search-input-row">
        <Search size={16} className="pc-search-icon" />
        <input
          type="text"
          className="form-input"
          placeholder={placeholder}
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          onFocus={() => suggestions.length > 0 && setShowDropdown(true)}
          style={{ paddingLeft: '40px' }}
        />
        {searching && <Loader2 size={16} className="pc-search-spinner spin" />}
        {query && !searching && (
          <button
            className="pc-search-clear"
            onClick={() => { setQuery(''); setSuggestions([]); setShowDropdown(false); }}
          >
            <X size={14} />
          </button>
        )}
      </div>
      {showDropdown && suggestions.length > 0 && (
        <div className="pc-dropdown">
          {suggestions.map((p, i) => {
            const sc = nutriColor(p.nutri_score);
            return (
              <button key={i} className="pc-dropdown-item" onClick={() => pickProduct(p)}>
                <div className="pc-dropdown-info">
                  <span className="pc-dropdown-name">{p.product_name}</span>
                  <span className="pc-dropdown-brand">{p.brand || 'Unknown brand'} • {p.calories_100g} kcal</span>
                </div>
                {p.nutri_score && (
                  <span className="pc-nutri-badge-sm" style={{ background: sc.bg, color: sc.text }}>
                    {p.nutri_score.toUpperCase()}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}

/* ── Visual bar helper ────────────────────────────────────── */
function ComparisonBar({ label, origVal, altVal, unit, lowerIsBetter = true }) {
  const maxVal = Math.max(origVal, altVal, 1);
  const origPct = (origVal / maxVal) * 100;
  const altPct = (altVal / maxVal) * 100;
  const diff = origVal - altVal;
  const improved = lowerIsBetter ? diff > 0 : diff < 0;
  const pctChange = origVal > 0 ? Math.abs(((diff) / origVal) * 100).toFixed(0) : '–';

  return (
    <div className="pc-bar-row">
      <div className="pc-bar-label">{label}</div>
      <div className="pc-bar-tracks">
        <div className="pc-bar-track">
          <div className="pc-bar-fill pc-bar-orig" style={{ width: `${origPct}%` }} />
          <span className="pc-bar-val">{origVal}{unit}</span>
        </div>
        <div className="pc-bar-track">
          <div className="pc-bar-fill pc-bar-alt" style={{ width: `${altPct}%` }} />
          <span className="pc-bar-val">{altVal}{unit}</span>
        </div>
      </div>
      <div className={`pc-bar-delta ${improved ? 'good' : diff === 0 ? '' : 'bad'}`}>
        {improved ? (lowerIsBetter ? '↓' : '↑') : diff === 0 ? '=' : (lowerIsBetter ? '↑' : '↓')}
        {pctChange}%
      </div>
    </div>
  );
}

/* ── Nutri Score badge ────────────────────────────────────── */
function NutriScoreBadge({ score }) {
  const grades = ['A', 'B', 'C', 'D', 'E'];
  const active = (score || 'C').toUpperCase();
  return (
    <div className="pc-nutriscore-row">
      {grades.map((g) => {
        const c = nutriColor(g);
        const isActive = g === active;
        return (
          <span
            key={g}
            className={`pc-nutri-letter ${isActive ? 'active' : ''}`}
            style={{
              background: isActive ? c.bg : 'rgba(255,255,255,0.03)',
              color: isActive ? c.text : '#444',
              borderColor: isActive ? c.text : 'transparent',
              transform: isActive ? 'scale(1.2)' : 'scale(1)',
            }}
          >
            {g}
          </span>
        );
      })}
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════
   MAIN COMPONENT
   ══════════════════════════════════════════════════════════════ */
export default function ProductComparison() {
  const [origProduct, setOrigProduct] = useState(null);
  const [altProduct, setAltProduct] = useState(null);

  // Auto-find alternatives
  const [autoQuery, setAutoQuery] = useState('');
  const [autoLoading, setAutoLoading] = useState(false);
  const [autoResults, setAutoResults] = useState([]);

  const [manualMode, setManualMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [comparisonResult, setComparisonResult] = useState(null);

  // ── Load a preset pair ──────────────────────────────────
  const presets = [
    {
      label: '🍟 Chips vs Baked Oats',
      orig: { product_name: 'Deep Fried Potato Chips', calories_100g: 536, sugar_100g: 5.0, protein_100g: 6.5, carbs_100g: 52, fat_100g: 35, nutri_score: 'E', brand: 'Generic', category: 'Snacks' },
      alt: { product_name: 'Baked Quinoa & Oats Chips', calories_100g: 380, sugar_100g: 1.2, protein_100g: 12.0, carbs_100g: 60, fat_100g: 8, nutri_score: 'A', brand: 'Health Store', category: 'Snacks' },
    },
    {
      label: '🥤 Soda vs Sparkling Water',
      orig: { product_name: 'Regular Sugary Cola Soda', calories_100g: 160, sugar_100g: 39.0, protein_100g: 0.0, carbs_100g: 40, fat_100g: 0, nutri_score: 'E', brand: 'Cola Co', category: 'Beverages' },
      alt: { product_name: 'Zero Sugar Sparkling Water', calories_100g: 0, sugar_100g: 0.0, protein_100g: 0.0, carbs_100g: 0, fat_100g: 0, nutri_score: 'A', brand: 'Fresh', category: 'Beverages' },
    },
    {
      label: '🍫 Chocolate vs Dark Cocoa',
      orig: { product_name: 'Milk Chocolate Candy Bar', calories_100g: 540, sugar_100g: 56.0, protein_100g: 7.0, carbs_100g: 60, fat_100g: 30, nutri_score: 'D', brand: 'Choco', category: 'Confectionery' },
      alt: { product_name: '85% Dark Cocoa Chocolate', calories_100g: 450, sugar_100g: 14.0, protein_100g: 11.0, carbs_100g: 30, fat_100g: 40, nutri_score: 'B', brand: 'Lindt', category: 'Confectionery' },
    },
  ];

  const loadPreset = (idx) => {
    const p = presets[idx];
    setOrigProduct(p.orig);
    setAltProduct(p.alt);
    setComparisonResult(null);
    setAutoResults([]);
    setError(null);
    buildLocalComparison(p.orig, p.alt);
  };

  // ── Build local comparison result ───────────────────────
  const buildLocalComparison = (orig, alt) => {
    const origCal = Math.max(1, orig.calories_100g);
    const origSugar = Math.max(0.1, orig.sugar_100g);
    const origProtein = Math.max(0.1, orig.protein_100g);

    setComparisonResult({
      original_product: orig,
      alternative_product: alt,
      calorie_reduction_pct: Math.round(((origCal - alt.calories_100g) / origCal) * 100),
      sugar_reduction_pct: Math.round(((origSugar - alt.sugar_100g) / origSugar) * 100),
      protein_increase_pct: Math.round(((alt.protein_100g - origProtein) / origProtein) * 100),
      health_score_delta: 0,
      summary_verdict: `${alt.product_name} is a healthier swap for ${orig.product_name}.`,
    });
  };

  // ── Auto find healthier alternatives ────────────────────
  const triggerAutoFind = async (targetQuery) => {
    if (!targetQuery || targetQuery.length < 2) return;
    setAutoLoading(true);
    setError(null);
    setAutoResults([]);
    setComparisonResult(null);

    try {
      const results = await apiClient.food.findHealthyAlternatives(targetQuery);
      if (results.length === 0) {
        setError('No healthier alternatives found for this product. Try another product.');
      } else {
        setAutoResults(results);
        setAltProduct(results[0].alternative_product);
        setOrigProduct(results[0].original_product);
        setComparisonResult(results[0]);
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to find alternatives.');
    } finally {
      setAutoLoading(false);
    }
  };

  const handleAutoFind = () => {
    const query = origProduct?.product_name || autoQuery;
    if (!query || query.length < 2) {
      setError('Please search and select a product first, or type a product name.');
      return;
    }
    triggerAutoFind(query);
  };

  // ── Select an alternative from auto-results ─────────────
  const selectAlternative = (result) => {
    setAltProduct(result.alternative_product);
    setComparisonResult(result);
  };

  // ── Manual compare ──────────────────────────────────────
  const handleManualCompare = () => {
    if (!origProduct || !altProduct) {
      setError('Please select both products to compare.');
      return;
    }
    setError(null);
    buildLocalComparison(origProduct, altProduct);
  };

  return (
    <div className="service-page">
      <div className="page-header">
        <div className="header-pill">
          <Sparkles size={14} /> Smart Food Swap
        </div>
        <h1 className="page-title">Healthy Product Swap & Comparison</h1>
        <p className="page-description">
          Search any product to instantly discover healthier alternatives with calorie, sugar, and protein comparisons.
        </p>
      </div>

      {/* ── Quick Presets ────────────────────────────────── */}
      <div className="preset-container" style={{ marginBottom: '20px' }}>
        <div className="preset-label">Quick Comparisons:</div>
        <div className="preset-chips">
          {presets.map((p, i) => (
            <button key={i} type="button" className="chip-btn" onClick={() => loadPreset(i)}>
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* ── Main Input Card ──────────────────────────────── */}
      <div className="card pc-main-card">
        <div className="card-header">
          <div className="card-title">
            <Search size={18} className="text-primary" />
            <span>Find Product & Healthier Swaps</span>
          </div>
          <button
            type="button"
            className="pc-mode-toggle"
            onClick={() => setManualMode(!manualMode)}
          >
            {manualMode ? 'Auto Mode' : 'Manual Mode'}
            <ChevronRight size={14} />
          </button>
        </div>

        {/* ── Auto Mode (default) ───────────────────────── */}
        {!manualMode ? (
          <div className="pc-auto-section">
            <ProductSearchInput
              label="Search for a product to swap"
              placeholder="e.g. Coca Cola, Doritos, Nutella..."
              onProductSelected={(p) => {
                setOrigProduct(p);
                setAutoQuery(p.product_name);
                setComparisonResult(null);
                setAutoResults([]);
                triggerAutoFind(p.product_name);
              }}
            />

            {origProduct && (
              <div className="pc-selected-card">
                <div className="pc-selected-info">
                  <span className="pc-selected-name">{origProduct.product_name}</span>
                  <span className="pc-selected-meta">
                    {origProduct.brand || 'Unknown'} • {origProduct.calories_100g} kcal • Sugar: {origProduct.sugar_100g}g
                  </span>
                </div>
                <NutriScoreBadge score={origProduct.nutri_score} />
              </div>
            )}

            <button
              type="button"
              className="btn-primary full-width pc-find-btn"
              onClick={handleAutoFind}
              disabled={autoLoading}
            >
              {autoLoading ? (
                <>
                  <Loader2 size={18} className="spin" />
                  Searching healthier alternatives...
                </>
              ) : (
                <>
                  <Zap size={18} />
                  Find Healthier Swaps
                </>
              )}
            </button>
          </div>
        ) : (
          /* ── Manual Mode ───────────────────────────────── */
          <div className="pc-manual-section">
            <div className="pc-manual-grid">
              <div className="pc-manual-col">
                <div className="pc-manual-label danger">
                  <span className="pc-dot red" /> Original Product
                </div>
                <ProductSearchInput
                  label="Search original product"
                  placeholder="Search by name..."
                  onProductSelected={(p) => { setOrigProduct(p); setComparisonResult(null); }}
                />
                {origProduct && (
                  <div className="pc-mini-card">
                    <strong>{origProduct.product_name}</strong>
                    <span>{origProduct.calories_100g} kcal • Sugar: {origProduct.sugar_100g}g • Protein: {origProduct.protein_100g}g</span>
                  </div>
                )}
              </div>

              <div className="pc-manual-divider">
                <ArrowRightLeft size={20} />
              </div>

              <div className="pc-manual-col">
                <div className="pc-manual-label good">
                  <span className="pc-dot green" /> Healthier Alternative
                </div>
                <ProductSearchInput
                  label="Search alternative product"
                  placeholder="Search by name..."
                  onProductSelected={(p) => { setAltProduct(p); setComparisonResult(null); }}
                />
                {altProduct && (
                  <div className="pc-mini-card">
                    <strong>{altProduct.product_name}</strong>
                    <span>{altProduct.calories_100g} kcal • Sugar: {altProduct.sugar_100g}g • Protein: {altProduct.protein_100g}g</span>
                  </div>
                )}
              </div>
            </div>

            <button
              type="button"
              className="btn-primary full-width pc-find-btn"
              onClick={handleManualCompare}
              disabled={loading}
            >
              <GitCompare size={18} />
              Compare Products
            </button>
          </div>
        )}

        {error && (
          <div className="alert alert-danger" style={{ marginTop: '16px' }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* ── Auto-discovered alternatives list ────────────── */}
      {autoResults.length > 1 && (
        <div className="card pc-alts-card">
          <div className="card-header">
            <div className="card-title">
              <Sparkles size={18} className="text-primary" />
              <span>Healthier Alternatives Found ({autoResults.length})</span>
            </div>
          </div>
          <div className="pc-alts-list">
            {autoResults.map((r, i) => {
              const isActive = comparisonResult?.alternative_product?.product_name === r.alternative_product.product_name;
              const sc = nutriColor(r.alternative_product.nutri_score);
              return (
                <button
                  key={i}
                  className={`pc-alt-item ${isActive ? 'active' : ''}`}
                  onClick={() => selectAlternative(r)}
                >
                  <div className="pc-alt-left">
                    <span className="pc-alt-name">{r.alternative_product.product_name}</span>
                    <span className="pc-alt-brand">{r.alternative_product.brand || 'Unknown'}</span>
                  </div>
                  <div className="pc-alt-right">
                    {r.calorie_reduction_pct > 0 && (
                      <span className="pc-alt-tag green">
                        <TrendingDown size={12} /> {r.calorie_reduction_pct}% fewer cal
                      </span>
                    )}
                    {r.alternative_product.nutri_score && (
                      <span className="pc-nutri-badge-sm" style={{ background: sc.bg, color: sc.text }}>
                        {r.alternative_product.nutri_score.toUpperCase()}
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* ── Visual Comparison Results ────────────────────── */}
      {comparisonResult && (
        <div className="card pc-result-card">
          <div className="card-header">
            <div className="card-title">
              <CheckCircle2 size={18} className="text-emerald" />
              <span>Comparison Results</span>
            </div>
            <span className="badge badge-emerald">Analysis Complete</span>
          </div>

          {/* Product name headers */}
          <div className="pc-result-header">
            <div className="pc-result-product orig">
              <span className="pc-dot red" />
              <div>
                <div className="pc-result-pname">{comparisonResult.original_product.product_name}</div>
                <div className="pc-result-pbrand">{comparisonResult.original_product.brand || ''}</div>
              </div>
              <NutriScoreBadge score={comparisonResult.original_product.nutri_score} />
            </div>
            <div className="pc-vs">VS</div>
            <div className="pc-result-product alt">
              <span className="pc-dot green" />
              <div>
                <div className="pc-result-pname">{comparisonResult.alternative_product.product_name}</div>
                <div className="pc-result-pbrand">{comparisonResult.alternative_product.brand || ''}</div>
              </div>
              <NutriScoreBadge score={comparisonResult.alternative_product.nutri_score} />
            </div>
          </div>

          {/* Metric delta cards */}
          <div className="pc-deltas-grid">
            <div className={`pc-delta-card ${comparisonResult.calorie_reduction_pct > 0 ? 'positive' : 'negative'}`}>
              <TrendingDown size={18} />
              <div className="pc-delta-val">
                {comparisonResult.calorie_reduction_pct > 0 ? '-' : '+'}{Math.abs(comparisonResult.calorie_reduction_pct)}%
              </div>
              <div className="pc-delta-label">Calories</div>
            </div>
            <div className={`pc-delta-card ${comparisonResult.sugar_reduction_pct > 0 ? 'positive' : 'negative'}`}>
              <TrendingDown size={18} />
              <div className="pc-delta-val">
                {comparisonResult.sugar_reduction_pct > 0 ? '-' : '+'}{Math.abs(comparisonResult.sugar_reduction_pct)}%
              </div>
              <div className="pc-delta-label">Sugar</div>
            </div>
            <div className={`pc-delta-card ${comparisonResult.protein_increase_pct > 0 ? 'positive' : 'negative'}`}>
              <TrendingUp size={18} />
              <div className="pc-delta-val">
                {comparisonResult.protein_increase_pct > 0 ? '+' : ''}{comparisonResult.protein_increase_pct}%
              </div>
              <div className="pc-delta-label">Protein</div>
            </div>
          </div>

          {/* Visual comparison bars */}
          <div className="pc-bars-section">
            <div className="pc-bars-legend">
              <span><span className="pc-dot red" /> Original</span>
              <span><span className="pc-dot green" /> Alternative</span>
            </div>
            <ComparisonBar
              label="Calories"
              origVal={comparisonResult.original_product.calories_100g}
              altVal={comparisonResult.alternative_product.calories_100g}
              unit=" kcal"
              lowerIsBetter={true}
            />
            <ComparisonBar
              label="Sugar"
              origVal={comparisonResult.original_product.sugar_100g}
              altVal={comparisonResult.alternative_product.sugar_100g}
              unit="g"
              lowerIsBetter={true}
            />
            <ComparisonBar
              label="Protein"
              origVal={comparisonResult.original_product.protein_100g}
              altVal={comparisonResult.alternative_product.protein_100g}
              unit="g"
              lowerIsBetter={false}
            />
            {comparisonResult.original_product.fat_100g !== undefined && (
              <ComparisonBar
                label="Fat"
                origVal={comparisonResult.original_product.fat_100g || 0}
                altVal={comparisonResult.alternative_product.fat_100g || 0}
                unit="g"
                lowerIsBetter={true}
              />
            )}
          </div>

          {/* AI Verdict */}
          <div className="verdict-banner">
            <div className="verdict-tag">AI Nutritionist Verdict</div>
            <div className="verdict-text">{comparisonResult.summary_verdict}</div>
          </div>
        </div>
      )}
    </div>
  );
}
