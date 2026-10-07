import React, { useEffect, useState } from 'react';
import { 
  Server, 
  Utensils, 
  Barcode, 
  GitCompare, 
  Target, 
  History, 
  CheckCircle2, 
  ArrowRight,
  Database,
  Cpu,
  Globe
} from 'lucide-react';
import axios from 'axios';

export default function ServiceOverview({ setActiveTab }) {
  const [logCount, setLogCount] = useState(0);
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    // Fetch system health and history count
    axios.get('http://localhost:8000/api/v1/meals/history/1')
      .then(res => {
        setLogCount(res.data.length);
        setApiStatus('online');
      })
      .catch(() => {
        setApiStatus('offline');
      });
  }, []);

  const services = [
    {
      id: 'estimator',
      title: 'AI Meal Calorie Estimator',
      code: 'SVC-01',
      description: 'Upload meal photo or text description to get instant calorie count, portion breakdown, and macros using Gemini Vision AI.',
      status: 'Operational',
      icon: Utensils,
      badgeColor: 'badge-green'
    },
    {
      id: 'barcode',
      title: 'Packaged Food Scanner',
      code: 'SVC-02',
      description: 'Barcode scanning and database query via OpenFoodFacts integration. Retrieves Nutri-Score, ingredients, and nutrition facts.',
      status: 'Operational',
      icon: Barcode,
      badgeColor: 'badge-green'
    },
    {
      id: 'compare',
      title: 'Product Comparison Engine',
      code: 'SVC-03',
      description: 'Side-by-side statistical comparison of food products. Calculates calorie reduction %, sugar delta, and AI recommendation.',
      status: 'Operational',
      icon: GitCompare,
      badgeColor: 'badge-green'
    },
    {
      id: 'planner',
      title: 'AI Diet & Macro Planner',
      code: 'SVC-04',
      description: 'Generates customized meal slots, target calorie allocations, and dish recommendations based on user goals and preferences.',
      status: 'Operational',
      icon: Target,
      badgeColor: 'badge-green'
    },
    {
      id: 'history',
      title: 'Meal Logs & Database Manager',
      code: 'SVC-05',
      description: 'Persists user meal intake history to SQLite async database with complete itemized nutrient breakdown and image URLs.',
      status: 'Operational',
      icon: History,
      badgeColor: 'badge-green'
    },
    {
      id: 'apidocs',
      title: 'API Specifications & Testing',
      code: 'SVC-06',
      description: 'Swagger UI OpenAPI documentation & interactive testing portal for backend REST service endpoints on port 8000.',
      status: 'Active',
      icon: Server,
      badgeColor: 'badge-blue'
    }
  ];

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <Server size={24} color="#2563eb" />
          Enterprise IT Services Dashboard
        </h1>
        <p className="page-description">
          Overview of food analysis microservices, system health metrics, and active AI engine status.
        </p>
      </div>

      {/* Metrics Row */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Backend Service Status</div>
          <div className="metric-value" style={{ color: apiStatus === 'online' ? '#059669' : '#dc2626' }}>
            {apiStatus === 'online' ? '100% ONLINE' : 'OFFLINE'}
          </div>
          <div className="metric-subtext">FastAPI REST Server (Port 8000)</div>
        </div>

        <div className="metric-card emerald">
          <div className="metric-label">AI Engine Status</div>
          <div className="metric-value" style={{ color: '#059669' }}>READY</div>
          <div className="metric-subtext">Google Gemini 2.5 Vision API</div>
        </div>

        <div className="metric-card amber">
          <div className="metric-label">Persisted Meal Logs</div>
          <div className="metric-value">{logCount} Logs</div>
          <div className="metric-subtext">Active User DB Session #1</div>
        </div>

        <div className="metric-card purple">
          <div className="metric-label">OpenFoodFacts API</div>
          <div className="metric-value">CONNECTED</div>
          <div className="metric-subtext">Global Product Barcode Registry</div>
        </div>
      </div>

      {/* Services Catalogue Grid */}
      <div style={{ marginTop: '28px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 700, color: '#0f172a', marginBottom: '16px' }}>
          Available IT Services & Microservices Catalogue
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '20px' }}>
          {services.map((svc) => {
            const IconComponent = svc.icon;
            return (
              <div key={svc.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div className="card-header" style={{ marginBottom: '12px' }}>
                    <div className="card-title">
                      <IconComponent size={20} color="#2563eb" />
                      <span>{svc.title}</span>
                    </div>
                    <span className={`badge ${svc.badgeColor}`}>{svc.code}</span>
                  </div>
                  <p style={{ fontSize: '13px', color: '#475569', lineHeight: 1.6, marginBottom: '20px' }}>
                    {svc.description}
                  </p>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', borderTop: '1px solid #e2e8f0' }}>
                  <span className="badge badge-green">
                    <CheckCircle2 size={12} /> {svc.status}
                  </span>
                  <button 
                    className="btn-primary" 
                    style={{ fontSize: '13px', padding: '6px 12px' }}
                    onClick={() => setActiveTab(svc.id)}
                  >
                    Launch Service <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
