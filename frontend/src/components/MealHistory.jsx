import React, { useEffect, useState } from 'react';
import { BookOpen, RefreshCw, Search, Calendar, ChevronDown, ChevronUp, Image as ImageIcon, AlertCircle, Utensils, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';

export default function MealHistory() {
  const { user } = useAuth();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedRow, setExpandedRow] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.meals.getHistory(user?.id || 1);
      setLogs(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to load meal journal logs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [user]);

  const toggleRow = (id) => {
    setExpandedRow(expandedRow === id ? null : id);
  };

  const filteredLogs = logs.filter(log => 
    (log.user_description && log.user_description.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (log.id && log.id.toString().includes(searchTerm))
  );

  const totalCaloriesAll = logs.reduce((acc, curr) => acc + (curr.total_calories || 0), 0);
  const avgProtein = logs.length ? (logs.reduce((acc, curr) => acc + (curr.total_protein_g || 0), 0) / logs.length).toFixed(1) : 0;

  return (
    <div className="service-page">
      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="header-pill">
              <Sparkles size={14} /> Nutrition Journal
            </div>
            <h1 className="page-title">Daily Food Journal & Meal History</h1>
            <p className="page-description">
              Review your historical food logs, uploaded meal photos, and itemized component nutrition facts.
            </p>
          </div>

          <button className="btn-secondary" onClick={fetchHistory} disabled={loading}>
            <RefreshCw size={14} className={loading ? "spin" : ""} />
            Refresh Journal
          </button>
        </div>
      </div>

      {/* Summary Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-card-header">
            <span className="metric-title">Total Logged Meals</span>
            <span className="badge badge-emerald">Journal Records</span>
          </div>
          <div className="metric-main-value">
            <span className="val">{logs.length}</span>
            <span className="total">Meals</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-card-header">
            <span className="metric-title">Cumulative Calories</span>
            <span className="badge badge-emerald">Calorie Journal</span>
          </div>
          <div className="metric-main-value">
            <span className="val">{Math.round(totalCaloriesAll)}</span>
            <span className="total">kcal</span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-card-header">
            <span className="metric-title">Avg Protein Intake</span>
            <span className="badge badge-blue">Per Meal</span>
          </div>
          <div className="metric-main-value">
            <span className="val">{avgProtein}g</span>
            <span className="total">Protein / meal</span>
          </div>
        </div>
      </div>

      {/* Search Bar Card */}
      <div className="card" style={{ marginBottom: '20px', padding: '12px 16px' }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <Search size={18} className="text-muted" />
          <input
            type="text"
            className="form-input"
            placeholder="Search food journal by dish name or log entry..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ border: 'none', padding: '4px', background: 'transparent' }}
          />
        </div>
      </div>

      {error && (
        <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {/* Logs Table */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ width: '60px' }}>Entry</th>
              <th>Date & Time Logged</th>
              <th>Dish Name / Summary</th>
              <th>Calories</th>
              <th>Macros (P / C / F)</th>
              <th>Photo</th>
              <th style={{ width: '100px', textAlign: 'center' }}>Breakdown</th>
            </tr>
          </thead>
          <tbody>
            {filteredLogs.length > 0 ? (
              filteredLogs.map((log) => {
                const isExpanded = expandedRow === log.id;
                const formattedDate = new Date(log.logged_at).toLocaleString();
                const imageUrl = log.image_url ? (log.image_url.startsWith('http') ? log.image_url : `http://localhost:8000${log.image_url}`) : null;

                return (
                  <React.Fragment key={log.id}>
                    <tr>
                      <td style={{ fontWeight: 700 }}>#{log.id}</td>
                      <td style={{ fontSize: '13px', color: '#94a3b8' }}>{formattedDate}</td>
                      <td style={{ fontWeight: 600 }}>{log.user_description || 'Unspecified Meal'}</td>
                      <td>
                        <span className="badge badge-emerald">
                          {log.total_calories} kcal
                        </span>
                      </td>
                      <td style={{ fontSize: '13px' }}>
                        P: <strong>{log.total_protein_g}g</strong> | C: <strong>{log.total_carbs_g}g</strong> | F: <strong>{log.total_fats_g}g</strong>
                      </td>
                      <td>
                        {imageUrl ? (
                          <a href={imageUrl} target="_blank" rel="noreferrer" className="text-link" style={{ fontSize: '13px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                            <ImageIcon size={14} /> View Photo
                          </a>
                        ) : (
                          <span className="text-muted" style={{ fontSize: '12px' }}>None</span>
                        )}
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <button
                          className="btn-secondary"
                          style={{ padding: '4px 10px', fontSize: '12px' }}
                          onClick={() => toggleRow(log.id)}
                        >
                          {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                          {log.items?.length || 0} items
                        </button>
                      </td>
                    </tr>

                    {/* Sub-row for expanded items */}
                    {isExpanded && (
                      <tr style={{ background: 'rgba(30, 41, 59, 0.4)' }}>
                        <td colSpan="7" style={{ padding: '16px' }}>
                          <div style={{ fontSize: '13px', fontWeight: 700, color: '#e2e8f0', marginBottom: '8px' }}>
                            Itemized Component List for Entry #{log.id}:
                          </div>
                          <div className="grid-subitems">
                            {log.items && log.items.length > 0 ? (
                              log.items.map((item, iIdx) => (
                                <div key={iIdx} className="subitem-box">
                                  <div className="subitem-title">{item.item_name}</div>
                                  <div className="subitem-portion">{item.portion_description}</div>
                                  <div className="subitem-macros">
                                    {item.calories} kcal (P: {item.protein_g}g, C: {item.carbs_g}g, F: {item.fats_g}g)
                                  </div>
                                </div>
                              ))
                            ) : (
                              <div style={{ fontSize: '12px', color: '#94a3b8' }}>No itemized sub-components logged for this entry.</div>
                            )}
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })
            ) : (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '40px', color: '#94a3b8' }}>
                  {loading ? 'Loading daily food journal entries...' : 'No food journal entries found matching your query.'}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
