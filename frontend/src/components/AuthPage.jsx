import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Mail, Lock, User, Sparkles, ArrowRight,
  AlertCircle, Loader2, Eye, EyeOff, ChefHat,
  GitCompare, ScanLine, Utensils, CheckCircle2
} from 'lucide-react';

const FEATURES = [
  { icon: ChefHat,    title: 'AI Meal Estimator',    desc: 'Snap a photo and get instant calorie & macro breakdown powered by Gemini Vision.' },
  { icon: ScanLine,   title: 'Barcode Scanner',      desc: 'Scan any packaged food to retrieve nutrition facts from a global product database.' },
  { icon: GitCompare, title: 'Healthy Swap Engine',  desc: 'Compare food products side-by-side to discover lower-calorie & healthier alternatives.' },
  { icon: Utensils,   title: 'Meal History',         desc: 'Track every meal you have logged with a full nutritional timeline.' },
];

export default function AuthPage() {
  const { login, register, authError, setAuthError, authLoading } = useAuth();

  const [mode, setMode]                   = useState('login');   // 'login' | 'register'
  const [email, setEmail]                 = useState('');
  const [password, setPassword]           = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName]           = useState('');
  const [showPassword, setShowPassword]   = useState(false);
  const [showConfirm, setShowConfirm]     = useState(false);
  const [localError, setLocalError]       = useState(null);      // client-side validation
  const [registeredEmail, setRegisteredEmail] = useState(null);  // show success banner

  // ── Helpers ───────────────────────────────────────────────────────────────
  const clearForm = () => {
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setFullName('');
    setLocalError(null);
    setAuthError(null);
  };

  const switchMode = (next) => {
    clearForm();
    setMode(next);
    setRegisteredEmail(null);
  };

  // ── Submit handler ────────────────────────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError(null);

    if (mode === 'register') {
      // Confirm password validation
      if (password !== confirmPassword) {
        setLocalError('Passwords do not match. Please try again.');
        return;
      }
      if (password.length < 6) {
        setLocalError('Password must be at least 6 characters long.');
        return;
      }

      try {
        await register(email, password, fullName);
        // Success → store the email, switch to Sign In, prefill email
        setRegisteredEmail(email);
        clearForm();
        setEmail(email);      // prefill email on sign-in form
        setMode('login');
      } catch (_) {
        // Error displayed via authError from context
      }
    } else {
      try {
        await login(email, password);
      } catch (_) {
        // Error displayed via authError from context
      }
    }
  };

  // Combined error to show (local validation takes priority)
  const displayError = localError || authError;

  return (
    <div className="auth-page">
      {/* ── Left panel – branding & feature list ── */}
      <div className="auth-left">
        <div className="auth-brand">
          <div className="auth-brand-logo">
            <Sparkles size={26} />
          </div>
          <span className="auth-brand-name">NutriVision <strong>AI</strong></span>
        </div>

        <div className="auth-left-body">
          <h1 className="auth-hero-title">
            Your personal<br />AI nutrition<br />co-pilot.
          </h1>
          <p className="auth-hero-sub">
            Log meals with a photo, scan packaged food, plan your macros, and hit your
            health goals — all in one place.
          </p>

          <ul className="auth-features">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <li key={title} className="auth-feature-item">
                <div className="auth-feature-icon">
                  <Icon size={18} />
                </div>
                <div>
                  <div className="auth-feature-title">{title}</div>
                  <div className="auth-feature-desc">{desc}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <p className="auth-left-footer">
          © {new Date().getFullYear()} NutriVision AI · Smart Food Intelligence Platform
        </p>
      </div>

      {/* ── Right panel – form ── */}
      <div className="auth-right">
        <div className="auth-form-card">

          {/* Tab switcher */}
          <div className="auth-tabs">
            <button
              className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
              onClick={() => switchMode('login')}
            >
              Sign In
            </button>
            <button
              className={`auth-tab ${mode === 'register' ? 'active' : ''}`}
              onClick={() => switchMode('register')}
            >
              Create Account
            </button>
          </div>

          {/* ── Account created success banner (shown after signup) ── */}
          {registeredEmail && mode === 'login' && (
            <div className="alert alert-success" style={{ marginBottom: '20px' }}>
              <CheckCircle2 size={16} />
              <span>
                Account created! Sign in with <strong>{registeredEmail}</strong> to continue.
              </span>
            </div>
          )}

          <div className="auth-form-header">
            <h2 className="auth-form-title">
              {mode === 'login' ? 'Welcome back' : 'Get started for free'}
            </h2>
            <p className="auth-form-sub">
              {mode === 'login'
                ? 'Sign in to your NutriVision account.'
                : 'Create your account — then sign in to get started.'}
            </p>
          </div>

          {/* Error alert */}
          {displayError && (
            <div className="alert alert-danger" style={{ marginBottom: '20px' }}>
              <AlertCircle size={16} />
              <span>{displayError}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">

            {/* Full Name — register only */}
            {mode === 'register' && (
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <div className="input-with-icon">
                  <User size={17} className="input-icon" />
                  <input
                    id="auth-fullname"
                    type="text"
                    className="form-input"
                    placeholder="e.g. Alex Morgan"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                    autoFocus
                  />
                </div>
              </div>
            )}

            {/* Email */}
            <div className="form-group">
              <label className="form-label">Email Address</label>
              <div className="input-with-icon">
                <Mail size={17} className="input-icon" />
                <input
                  id="auth-email"
                  type="email"
                  className="form-input"
                  placeholder="your.email@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoFocus={mode === 'login'}
                />
              </div>
            </div>

            {/* Password */}
            <div className="form-group">
              <label className="form-label">Password</label>
              <div className="input-with-icon">
                <Lock size={17} className="input-icon" />
                <input
                  id="auth-password"
                  type={showPassword ? 'text' : 'password'}
                  className="form-input"
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  style={{ paddingRight: '44px' }}
                />
                <button
                  type="button"
                  className="auth-eye-btn"
                  onClick={() => setShowPassword((v) => !v)}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              {mode === 'register' && (
                <div className="auth-hint">Minimum 6 characters</div>
              )}
            </div>

            {/* Confirm Password — register only */}
            {mode === 'register' && (
              <div className="form-group">
                <label className="form-label">Confirm Password</label>
                <div className="input-with-icon">
                  <Lock size={17} className="input-icon" />
                  <input
                    id="auth-confirm-password"
                    type={showConfirm ? 'text' : 'password'}
                    className={`form-input ${
                      confirmPassword && password !== confirmPassword ? 'input-error' : ''
                    }`}
                    placeholder="••••••••••••"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    style={{ paddingRight: '44px' }}
                  />
                  <button
                    type="button"
                    className="auth-eye-btn"
                    onClick={() => setShowConfirm((v) => !v)}
                    tabIndex={-1}
                  >
                    {showConfirm ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
                {/* Inline mismatch hint */}
                {confirmPassword && password !== confirmPassword && (
                  <div className="auth-hint auth-hint-error">Passwords do not match</div>
                )}
              </div>
            )}

            <button
              id="auth-submit-btn"
              type="submit"
              className="btn-primary full-width"
              disabled={authLoading || (mode === 'register' && confirmPassword && password !== confirmPassword)}
              style={{ marginTop: '12px', padding: '13px', fontSize: '15px' }}
            >
              {authLoading ? (
                <>
                  <Loader2 size={18} className="spin" />
                  {mode === 'login' ? 'Signing in…' : 'Creating account…'}
                </>
              ) : (
                <>
                  {mode === 'login' ? 'Sign In' : 'Create Account'}
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

          <p className="auth-switch-text">
            {mode === 'login' ? (
              <>Don't have an account?{' '}
                <button className="text-link" onClick={() => switchMode('register')}>
                  Sign up free
                </button>
              </>
            ) : (
              <>Already have an account?{' '}
                <button className="text-link" onClick={() => switchMode('login')}>
                  Sign in
                </button>
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
