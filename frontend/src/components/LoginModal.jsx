import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Lock,
  Mail,
  User,
  Briefcase,
  ArrowRight,
  ArrowLeft,
  X,
  AlertCircle,
  CheckCircle,
  KeyRound,
  RotateCw,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LoginModal({
  isOpen,
  onClose,
  defaultMode = 'login',
  onSuccess,
}) {
  const { login, sendSignupOtp, verifySignupOtp } = useAuth();
  const [isRegisterMode, setIsRegisterMode] = useState(defaultMode === 'register');
  const [signupStep, setSignupStep] = useState(1); // 1 = info, 2 = otp verification

  // Login & Shared
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Signup extra fields
  const [fullName, setFullName] = useState('');
  const [headline, setHeadline] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [devOtp, setDevOtp] = useState(null);
  const [resendCountdown, setResendCountdown] = useState(0);

  // Sync mode when defaultMode prop or isOpen changes
  useEffect(() => {
    if (isOpen) {
      setIsRegisterMode(defaultMode === 'register');
      setSignupStep(1);
      setError('');
      setDevOtp(null);
    }
  }, [defaultMode, isOpen]);

  // Resend cooldown timer effect
  useEffect(() => {
    let timer;
    if (signupStep === 2 && resendCountdown > 0) {
      timer = setInterval(() => {
        setResendCountdown((prev) => (prev > 0 ? prev - 1 : 0));
      }, 1000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [signupStep, resendCountdown]);

  if (!isOpen) return null;

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const authData = await login(email.trim(), password);
      onClose();
      if (onSuccess) onSuccess(authData);
    } catch (err) {
      setError(err.message || 'Authentication failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleStep1SendOtp = async (e) => {
    e.preventDefault();
    setError('');

    if (!fullName.trim()) {
      setError('Full Name is required.');
      return;
    }
    if (!email.trim() || !email.includes('@')) {
      setError('A valid email address is required.');
      return;
    }
    if (!password || password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setLoading(true);
    try {
      const resp = await sendSignupOtp(email.trim());
      if (resp.dev_otp) {
        setDevOtp(resp.dev_otp);
        setOtpCode(resp.dev_otp);
      }
      setSignupStep(2);
      setResendCountdown(60);
    } catch (err) {
      setError(err.message || 'Failed to send verification code.');
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    if (resendCountdown > 0 || loading) return;
    setError('');
    setLoading(true);
    try {
      const resp = await sendSignupOtp(email.trim());
      if (resp.dev_otp) {
        setDevOtp(resp.dev_otp);
        setOtpCode(resp.dev_otp);
      }
      setResendCountdown(60);
    } catch (err) {
      setError(err.message || 'Failed to resend verification code.');
    } finally {
      setLoading(false);
    }
  };

  const handleStep2VerifyOtp = async (e) => {
    e.preventDefault();
    setError('');

    if (!otpCode.trim() || otpCode.trim().length !== 6) {
      setError('Please enter the 6-digit verification code.');
      return;
    }

    setLoading(true);
    try {
      const authData = await verifySignupOtp({
        email: email.trim(),
        otpCode: otpCode.trim(),
        password,
        fullName: fullName.trim(),
        headline: headline.trim() || null,
      });
      onClose();
      if (onSuccess) onSuccess(authData);
    } catch (err) {
      setError(err.message || 'Verification failed. Please check your code.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-modal-backdrop" onClick={onClose}>
      <div
        className="admin-modal-window auth-modal-window"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '460px' }}
      >
        <div className="admin-modal-header auth-modal-header">
          <div className="auth-header-brand">
            <div className="brand-icon-box">
              <Sparkles className="icon-sparkles" />
            </div>
            <div>
              <h3 style={{ margin: 0 }}>
                {!isRegisterMode
                  ? 'Welcome to JobEazy'
                  : signupStep === 1
                  ? 'Create Candidate Account'
                  : 'Verify Your Email'}
              </h3>
              <p className="auth-subtitle">
                {!isRegisterMode
                  ? 'Sign in to access your Candidate OS'
                  : signupStep === 1
                  ? 'Step 1 of 2: Basic Professional Profile'
                  : `Enter 6-digit code sent to ${email}`}
              </p>
            </div>
          </div>
          <button className="close-modal-btn" onClick={onClose} type="button">
            <X size={18} />
          </button>
        </div>

        {/* Step indicator for signup */}
        {isRegisterMode && (
          <div className="auth-step-indicator">
            <div className={`auth-step-pill ${signupStep >= 1 ? 'active' : ''}`}>
              <span className="step-num">1</span>
              <span>Account Info</span>
            </div>
            <div className="auth-step-connector" />
            <div className={`auth-step-pill ${signupStep === 2 ? 'active' : ''}`}>
              <span className="step-num">2</span>
              <span>Email OTP</span>
            </div>
          </div>
        )}

        <div className="admin-modal-body auth-modal-body">
          {error && (
            <div className="auth-error-banner">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          {/* SIGN IN FORM */}
          {!isRegisterMode && (
            <form onSubmit={handleLoginSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
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
                  <span>Signing In...</span>
                ) : (
                  <>
                    <span>Sign In to Workspace</span>
                    <ArrowRight size={16} />
                  </>
                )}
              </button>

              <div className="auth-switch-mode">
                <span>
                  New to JobEazy?{' '}
                  <button
                    type="button"
                    className="auth-link-btn"
                    onClick={() => {
                      setIsRegisterMode(true);
                      setSignupStep(1);
                      setError('');
                    }}
                  >
                    Signup
                  </button>
                </span>
              </div>
            </form>
          )}

          {/* SIGNUP STEP 1: Basic Information */}
          {isRegisterMode && signupStep === 1 && (
            <form onSubmit={handleStep1SendOtp} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div className="admin-form-group">
                <label>
                  Full Name <span style={{ color: 'var(--emerald-500)' }}>*</span>
                </label>
                <div className="auth-input-wrapper">
                  <User className="auth-field-icon" size={16} />
                  <input
                    type="text"
                    required
                    placeholder="e.g. Alex Mercer"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="auth-input"
                  />
                </div>
              </div>

              <div className="admin-form-group">
                <label>
                  Professional Role / Headline{' '}
                  <span style={{ color: 'var(--text-muted)', fontSize: '11px' }}>(optional)</span>
                </label>
                <div className="auth-input-wrapper">
                  <Briefcase className="auth-field-icon" size={16} />
                  <input
                    type="text"
                    placeholder="e.g. AI Engineer, Full Stack Developer, Product Lead"
                    value={headline}
                    onChange={(e) => setHeadline(e.target.value)}
                    className="auth-input"
                  />
                </div>
              </div>

              <div className="admin-form-group">
                <label>
                  Email Address <span style={{ color: 'var(--emerald-500)' }}>*</span>
                </label>
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
                <label>
                  Password <span style={{ color: 'var(--emerald-500)' }}>*</span>
                </label>
                <div className="auth-input-wrapper">
                  <Lock className="auth-field-icon" size={16} />
                  <input
                    type="password"
                    required
                    minLength={6}
                    placeholder="•••••••••••• (min 6 characters)"
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
                  <span>Sending Verification Code...</span>
                ) : (
                  <>
                    <span>Continue to Verification</span>
                    <ArrowRight size={16} />
                  </>
                )}
              </button>

              <div className="auth-switch-mode">
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
              </div>
            </form>
          )}

          {/* SIGNUP STEP 2: Email OTP Verification */}
          {isRegisterMode && signupStep === 2 && (
            <form onSubmit={handleStep2VerifyOtp} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {devOtp && (
                <div className="auth-dev-otp-banner">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <KeyRound size={15} style={{ color: 'var(--emerald-400)' }} />
                    <span>
                      Dev OTP: <strong style={{ letterSpacing: '2px', color: 'var(--emerald-400)' }}>{devOtp}</strong>
                    </span>
                  </div>
                  <button
                    type="button"
                    className="dev-otp-autofill-btn"
                    onClick={() => setOtpCode(devOtp)}
                  >
                    Auto-fill
                  </button>
                </div>
              )}

              <div className="auth-otp-instructions">
                <p style={{ margin: 0, fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                  We sent a 6-digit verification code to{' '}
                  <strong style={{ color: 'var(--text-primary)' }}>{email}</strong>. Enter it below to activate your account.
                </p>
              </div>

              <div className="admin-form-group">
                <label style={{ textAlign: 'center', display: 'block' }}>6-Digit Verification Code</label>
                <div className="otp-digit-wrapper">
                  <input
                    type="text"
                    required
                    maxLength={6}
                    placeholder="000000"
                    value={otpCode}
                    onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                    className="auth-input otp-code-input"
                    autoFocus
                  />
                </div>
              </div>

              <div className="auth-otp-actions-strip">
                <button
                  type="button"
                  className="auth-back-link"
                  onClick={() => {
                    setSignupStep(1);
                    setError('');
                  }}
                >
                  <ArrowLeft size={13} />
                  <span>Change Email</span>
                </button>

                <div className="auth-resend-wrapper">
                  {resendCountdown > 0 ? (
                    <span className="resend-countdown-text">Resend in {resendCountdown}s</span>
                  ) : (
                    <button
                      type="button"
                      className="auth-resend-btn"
                      onClick={handleResendOtp}
                      disabled={loading}
                    >
                      <RotateCw size={12} className={loading ? 'spin' : ''} />
                      <span>Resend Code</span>
                    </button>
                  )}
                </div>
              </div>

              <button
                type="submit"
                disabled={loading || otpCode.length !== 6}
                className="action-btn-primary auth-submit-btn"
              >
                {loading ? (
                  <span>Verifying & Creating Account...</span>
                ) : (
                  <>
                    <CheckCircle size={16} />
                    <span>Verify & Launch Workspace</span>
                  </>
                )}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
