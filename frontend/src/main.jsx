import React, { Component, StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("UI Error caught by ErrorBoundary:", error, errorInfo);
  }

  handleReset = () => {
    localStorage.removeItem('nutrivision_user');
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          background: '#0a0a0a',
          color: '#f5f5f5',
          fontFamily: 'sans-serif',
          textAlign: 'center'
        }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: '#ff6b6b' }}>
            Application Error Encountered
          </h2>
          <pre style={{
            background: 'rgba(255,255,255,0.05)',
            padding: '1rem',
            borderRadius: '8px',
            maxWidth: '600px',
            overflow: 'auto',
            marginBottom: '1.5rem',
            fontSize: '0.85rem',
            color: '#e0e0e0',
            textAlign: 'left'
          }}>
            {this.state.error?.message || String(this.state.error)}
          </pre>
          <button
            onClick={this.handleReset}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: '#ffffff',
              color: '#000000',
              fontWeight: '600',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            Clear Session &amp; Reload
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
