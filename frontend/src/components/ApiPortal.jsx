import React, { useState } from 'react';
import { Terminal, ExternalLink, Play, Server, Code, CheckCircle2 } from 'lucide-react';
import axios from 'axios';

export default function ApiPortal() {
  const [selectedEndpoint, setSelectedEndpoint] = useState('GET /');
  const [responseOutput, setResponseOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  const endpoints = [
    {
      method: 'GET',
      path: '/',
      description: 'Health check endpoint returns backend status and API service version info.',
      exampleUrl: 'http://localhost:8000/'
    },
    {
      method: 'GET',
      path: '/api/v1/meals/history/1',
      description: 'Fetches historical logged meals for user ID 1.',
      exampleUrl: 'http://localhost:8000/api/v1/meals/history/1'
    },
    {
      method: 'GET',
      path: '/api/v1/packaged-food/scan/5449000000996',
      description: 'Queries OpenFoodFacts database for Coca Cola barcode.',
      exampleUrl: 'http://localhost:8000/api/v1/packaged-food/scan/5449000000996'
    }
  ];

  const handleTestApi = async (ep) => {
    setSelectedEndpoint(`${ep.method} ${ep.path}`);
    setLoading(true);
    setResponseOutput(null);

    try {
      const res = await axios.get(ep.exampleUrl);
      setResponseOutput(JSON.stringify(res.data, null, 2));
    } catch (err) {
      setResponseOutput(JSON.stringify(err.response?.data || { error: err.message }, null, 2));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <Terminal size={24} color="#2563eb" />
          API Services Portal & Endpoint Specifications
        </h1>
        <p className="page-description">
          Technical service contracts, OpenAPI documentation endpoints, and live response inspector.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Left Column: API Endpoints Table */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <Server size={18} color="#2563eb" />
              <span>Available Microservice Endpoints</span>
            </div>
            <a 
              href="http://localhost:8000/docs" 
              target="_blank" 
              rel="noreferrer"
              className="btn-secondary" 
              style={{ padding: '4px 8px', fontSize: '11px' }}
            >
              Open Swagger <ExternalLink size={12} />
            </a>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {endpoints.map((ep, idx) => (
              <div key={idx} style={{ backgroundColor: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '6px', padding: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <div>
                    <span className="badge badge-blue" style={{ marginRight: '8px' }}>{ep.method}</span>
                    <span style={{ fontWeight: 600, fontFamily: 'monospace', fontSize: '13px', color: '#0f172a' }}>{ep.path}</span>
                  </div>
                  <button 
                    className="btn-primary" 
                    style={{ padding: '4px 8px', fontSize: '11px' }}
                    onClick={() => handleTestApi(ep)}
                  >
                    <Play size={10} /> Test GET
                  </button>
                </div>
                <p style={{ fontSize: '12px', color: '#64748b' }}>{ep.description}</p>
              </div>
            ))}

            {/* In addition, list POST endpoints */}
            <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '12px', fontWeight: 600, color: '#475569', marginBottom: '8px' }}>
                POST Data Mutation Services:
              </div>
              <div style={{ fontSize: '12px', color: '#334155', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div><span className="badge badge-green">POST</span> <code>/api/v1/meals/estimate</code> (Multipart Form)</div>
                <div><span className="badge badge-green">POST</span> <code>/api/v1/meals/log</code> (JSON Payload)</div>
                <div><span className="badge badge-green">POST</span> <code>/api/v1/packaged-food/compare</code> (JSON Comparison)</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Live JSON Inspector */}
        <div className="card" style={{ backgroundColor: '#0f172a', color: '#f8fafc', border: '1px solid #1e293b' }}>
          <div className="card-header" style={{ borderColor: '#334155' }}>
            <div className="card-title" style={{ color: '#38bdf8' }}>
              <Code size={18} />
              <span>Live Response Inspector</span>
            </div>
            <span className="badge badge-blue">{selectedEndpoint}</span>
          </div>

          <div style={{ minHeight: '300px' }}>
            {loading ? (
              <div style={{ color: '#94a3b8', padding: '24px', textAlign: 'center' }}>Executing HTTP request...</div>
            ) : responseOutput ? (
              <pre style={{ fontFamily: 'monospace', fontSize: '12px', color: '#4ade80', overflowX: 'auto', padding: '12px', backgroundColor: '#020617', borderRadius: '6px', border: '1px solid #1e293b' }}>
                {responseOutput}
              </pre>
            ) : (
              <div style={{ color: '#64748b', padding: '48px 24px', textAlign: 'center', fontSize: '13px' }}>
                Click "Test GET" on any endpoint to execute a real-time HTTP request and view the JSON response payload.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
