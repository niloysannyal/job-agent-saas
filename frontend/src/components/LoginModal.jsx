import React, { useState } from 'react';
import { Sparkles, Shield, Lock, Mail, ArrowRight, X, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LoginModal({ isOpen, onClose, defaultMode = 'login', onSuccess }) {
  const { login, register } = useAuth();
  const [isRegisterMode, setIsRegisterMode] = useState(defaultMode === 'register');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let authData;
      if (isRegisterMode) {
        authData = await register(email, password);
      } else {
        authData = await login(email, password);
      }
      onClose();
      if (onSuccess) onSuccess(authData);
    } catch (err) {
      setError(err.message || 'Authentication failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-modal-backdrop" onClick={onClose}>
      <div
        className="admin-modal-window auth-modal-window"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '440px' }}
      >
        <div className="admin-modal-header auth-modal-header">
          <div className="auth-header-brand">
            <div className="brand-icon-box">
              <Sparkles className="icon-sparkles" />
            </div>
            <div>
              <h3 style={{ margin: 0 }}>
                {isRegisterMode ? 'Create JobEazy Account' : 'Welcome to JobEazy'}
              </h3>
              <p className="auth-subtitle">
                {isRegisterMode
                  ? 'Start automating your personal job search'
                  : 'Sign in to access your Candidate OS'}
              </p>
            </div>
          </div>
          <button className="close-modal-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="admin-modal-body auth-modal-body">
          {error && (
            <div className="auth-error-banner">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          <div className="admin-form-group">
            <label>Email Address</label>
            <div className="auth-input-wrapper">
              <Mail className="auth-field-icon" size={16} />
              <input
                type="email"
                required
                placeholder="you@domain.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="auth-input"
              />
            </div>
          </div>

          <div className="admin-form-group">
            <label>Password</label>
            <div className="auth-input-wrapper">
              <Lock className="auth-field-icon" size={16} />
              <input
                type="password"
                required
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="auth-input"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="action-btn-primary auth-submit-btn"
          >
            {loading ? (
              <span>Authenticating...</span>
            ) : (
              <>
                <span>{isRegisterMode ? 'Create Free Account' : 'Sign In to Workspace'}</span>
                <ArrowRight size={16} />
              </>
            )}
          </button>

          <div className="auth-switch-mode">
            {isRegisterMode ? (
              <span>
                Already have an account?{' '}
                <button
                  type="button"
                  className="auth-link-btn"
                  onClick={() => {
                    setIsRegisterMode(false);
                    setError('');
                  }}
                >
                  Sign In
                </button>
              </span>
            ) : (
              <span>
                New to JobEazy?{' '}
                <button
                  type="button"
                  className="auth-link-btn"
                  onClick={() => {
                    setIsRegisterMode(true);
                    setError('');
                  }}
                >
                  Create Free Account
                </button>
              </span>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}

