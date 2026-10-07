import React, { useState } from 'react';
import { Barcode, Search, AlertCircle, CheckCircle2, ShieldCheck, Loader2, Sparkles, Upload, Image as ImageIcon } from 'lucide-react';
import apiClient from '../services/apiClient';

export default function BarcodeScanner() {
  const [barcode, setBarcode] = useState('5449000000996');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleScan = async (e) => {
    if (e) e.preventDefault();
    if (!barcode.trim()) {
      setError("Please enter a valid product barcode number.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await apiClient.food.lookupBarcode(barcode.trim());
      setResult({ product: data });
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Product not found in global barcode catalog.");
    } finally {
      setLoading(false);
    }
  };

  const handleBarcodeImageUpload = async (file) => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await apiClient.food.scanBarcodeImage(file);
      if (data.success && data.product) {
        setResult(data);
      } else {
        setError(data.message || "No barcode found in image. Try typing the barcode number below.");
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to scan barcode from image.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      handleBarcodeImageUpload(file);
    }
  };

  const loadPresetBarcode = (code) => {
    setBarcode(code);
  };

  const getNutriScoreColor = (score) => {
    if (!score) return 'badge-blue';
    const s = score.toUpperCase();
    if (s === 'A' || s === 'B') return 'badge-emerald';
    if (s === 'C' || s === 'D') return 'badge-amber';
    return 'badge-danger';
  };

  return (
    <div className="service-page">
      <div className="page-header">
        <div className="header-pill">
          <Sparkles size={14} /> Smart Catalog Lookup
        </div>
        <h1 className="page-title">Barcode & Packaged Food Scanner</h1>
        <p className="page-description">
          Scan product barcodes or search packaging to inspect Nutri-Score, sugar levels, additives, and nutritional quality.
        </p>
      </div>

      <div className="grid-2col">
        {/* Input Card */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Search size={18} className="text-primary" />
              <span>Product Barcode & Photo Lookup</span>
            </div>
            <span className="badge badge-emerald">Smart Index</span>
          </div>

          <form onSubmit={handleScan}>
            <div className="form-group">
              <label className="form-label">Upload Barcode Photo</label>
              <div 
                className="dropzone"
                onClick={() => document.getElementById('barcodeFileInput').click()}
              >
                <input 
                  type="file" 
                  id="barcodeFileInput" 
                  accept="image/*" 
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                />
                {previewUrl ? (
                  <div className="preview-container">
                    <img src={previewUrl} alt="Barcode Preview" className="preview-image" />
                    <p className="preview-filename">
                      Selected: {selectedFile?.name} (Click to change)
                    </p>
                  </div>
                ) : (
                  <div className="dropzone-placeholder">
                    <Barcode size={40} className="drop-icon" />
                    <p className="drop-title">Snap or upload barcode image</p>
                    <p className="drop-sub">Decodes barcode stripes automatically</p>
                  </div>
                )}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Enter EAN / UPC Barcode Number</label>
              <div className="input-with-icon">
                <Barcode size={18} className="input-icon" />
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. 5449000000996"
                  value={barcode}
                  onChange={(e) => setBarcode(e.target.value)}
                />
              </div>
            </div>

            <div className="preset-container">
              <div className="preset-label">Sample Test Barcodes:</div>
              <div className="preset-chips">
                <button
                  type="button"
                  className="chip-btn"
                  onClick={() => loadPresetBarcode('5449000000996')}
                >
                  🥤 Coca Cola (5449000000996)
                </button>
                <button
                  type="button"
                  className="chip-btn"
                  onClick={() => loadPresetBarcode('3017620422003')}
                >
                  🍫 Nutella (3017620422003)
                </button>
                <button
                  type="button"
                  className="chip-btn"
                  onClick={() => loadPresetBarcode('737628064502')}
                >
                  🍜 Rice Ramen (737628064502)
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
                  Fetching Product Data...
                </>
              ) : (
                <>
                  <Search size={18} /> Lookup Product Data
                </>
              )}
            </button>
          </form>
        </div>

        {/* Result View */}
        <div>
          {result && result.product ? (
            <div className="card">
              <div className="card-header">
                <div className="card-title">
                  <CheckCircle2 size={18} className="text-emerald" />
                  <span>Product Nutritional Card</span>
                </div>
                <span className={`badge ${getNutriScoreColor(result.product.nutri_score)}`}>
                  Nutri-Score: {result.product.nutri_score || 'N/A'}
                </span>
              </div>

              <div className="product-hero-block">
                {result.product.image_url && (
                  <img
                    src={result.product.image_url}
                    alt={result.product.product_name}
                    className="product-img"
                  />
                )}
                <div>
                  <h2 className="product-title">{result.product.product_name}</h2>
                  <div className="product-meta">
                    Brand: <strong>{result.product.brand || 'Generic'}</strong> • Category: {result.product.category || 'Food'}
                  </div>
                  <div className="product-serving">
                    Standard Serving: {result.product.serving_size_g || 100}g
                  </div>
                </div>
              </div>

              {/* Health Quality Indicators */}
              <div className="health-badges-row">
                <div className="health-flag">
                  <ShieldCheck size={16} className="text-emerald" />
                  <span>Nutritive Grade: <strong>{result.product.nutri_score || 'B'}</strong></span>
                </div>
                {result.product.sugar_100g > 15 && (
                  <div className="health-flag warning">
                    <AlertCircle size={16} className="text-danger" />
                    <span>High Refined Sugar Content ({result.product.sugar_100g}g/100g)</span>
                  </div>
                )}
              </div>

              {/* Nutrition Values Grid */}
              <div className="table-title" style={{ marginTop: '16px' }}>Nutritional Facts (per 100g):</div>

              <div className="macro-cards-grid">
                <div className="macro-box calorie">
                  <div className="macro-lbl">CALORIES</div>
                  <div className="macro-val">{result.product.calories_100g}</div>
                  <div className="macro-unit">kcal / 100g</div>
                </div>

                <div className="macro-box protein">
                  <div className="macro-lbl">PROTEIN</div>
                  <div className="macro-val">{result.product.protein_100g}g</div>
                  <div className="macro-unit">grams</div>
                </div>

                <div className="macro-box carbs">
                  <div className="macro-lbl">CARBS</div>
                  <div className="macro-val">{result.product.carbs_100g}g</div>
                  <div className="macro-unit">grams</div>
                </div>

                <div className="macro-box fats">
                  <div className="macro-lbl">SUGAR</div>
                  <div className="macro-val">{result.product.sugar_100g}g</div>
                  <div className="macro-unit">grams</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card empty-card">
              <Barcode size={48} className="empty-icon-lg" />
              <h3>No Barcode Loaded</h3>
              <p>Enter a product barcode on the left or click a sample preset to view nutritional facts.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
