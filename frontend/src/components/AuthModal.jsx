import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { X, Mail, Lock, User, Sparkles, ArrowRight, AlertCircle, Loader2 } from 'lucide-react';

export default function AuthModal() {
  const { 
    isAuthModalOpen, 
    setIsAuthModalOpen, 
    authMode, 
    setAuthMode, 
    login, 
    register, 
    authError, 
    setAuthError, 
    authLoading 
  } = useAuth();

  const [email, setEmail] = useState('alex.morgan@nutrivision.ai');
  const [password, setPassword] = useState('password123');
  const [fullName, setFullName] = useState('Alex Morgan');

  if (!isAuthModalOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (authMode === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName);
      }
    } catch (err) {
      // Error handled in AuthContext
    }
  };

  return (
    <div className="modal-overlay" onClick={() => setIsAuthModalOpen(false)}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={() => setIsAuthModalOpen(false)}>
          <X size={20} />
        </button>

        <div className="modal-header">
          <div className="brand-badge">
            <Sparkles size={16} /> NutriVision Security
          </div>
          <h2>{authMode === 'login' ? 'Welcome Back' : 'Create Your Health Account'}</h2>
          <p>Access personalized AI diet plans, scan logs, and smart macro tracking.</p>
        </div>

        {authError && (
          <div className="alert alert-danger" style={{ marginBottom: '16px' }}>
            <AlertCircle size={16} />
            <span>{authError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {authMode === 'register' && (
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <div className="input-with-icon">
                <User size={18} className="input-icon" />
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Alex Morgan"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Email Address</label>
            <div className="input-with-icon">
              <Mail size={18} className="input-icon" />
              <input
                type="email"
                className="form-input"
                placeholder="your.email@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <div className="input-with-icon">
              <Lock size={18} className="input-icon" />
              <input
                type="password"
                className="form-input"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn-primary full-width"
            disabled={authLoading}
            style={{ marginTop: '20px', padding: '12px' }}
          >
            {authLoading ? (
              <>
                <Loader2 size={18} className="spin" />
                {authMode === 'login' ? 'Authenticating...' : 'Creating Account...'}
              </>
            ) : (
              <>
                {authMode === 'login' ? 'Sign In to Account' : 'Register Account'}
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </form>

        <div className="modal-footer" style={{ marginTop: '20px', textAlign: 'center', fontSize: '13px' }}>
          {authMode === 'login' ? (
            <span>
              Don't have an account?{' '}
              <button
                className="text-link"
                onClick={() => { setAuthMode('register'); setAuthError(null); }}
              >
                Sign up free
              </button>
            </span>
          ) : (
            <span>
              Already have an account?{' '}
              <button
                className="text-link"
                onClick={() => { setAuthMode('login'); setAuthError(null); }}
              >
                Sign in
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
