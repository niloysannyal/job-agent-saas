import React, { useState, useEffect, useCallback } from 'react';
import {
  Mail,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  ShieldCheck,
  Key,
  Trash2,
  Sparkles,
  Eye,
  EyeOff,
  Server,
  Zap,
} from 'lucide-react';

export default function ProfileIntegrationsTab({
  authHeaders = {},
  showToast,
  accountId,
}) {
  const [emailStatus, setEmailStatus] = useState({
    connected: false,
    provider: null,
    email: null,
    token_expires_at: null,
    platform_oauth_configured: false,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isConnectingOAuth, setIsConnectingOAuth] = useState(false);
  const [isDisconnecting, setIsDisconnecting] = useState(false);

  // SMTP Form State
  const [activeSubMode, setActiveSubMode] = useState('oauth'); // 'oauth' | 'smtp'
  const [smtpEmail, setSmtpEmail] = useState('');
  const [smtpPassword, setSmtpPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isConnectingSmtp, setIsConnectingSmtp] = useState(false);
  const [smtpError, setSmtpError] = useState(null);

  const fetchEmailStatus = useCallback(async () => {
    try {
      setIsLoading(true);
      const res = await fetch('/api/v1/integrations/email/status', {
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const data = await res.json();
        setEmailStatus(data);
        if (data.email && !smtpEmail) {
          setSmtpEmail(data.email);
        }
      }
    } catch (err) {
      console.error('Error checking email status:', err);
    } finally {
      setIsLoading(false);
    }
  }, [authHeaders, smtpEmail]);

  useEffect(() => {
    fetchEmailStatus();
  }, [fetchEmailStatus]);

  // Listen for popup OAuth messages
  useEffect(() => {
    function handleOAuthMessage(event) {
      if (event.data?.type === 'GOOGLE_OAUTH_CODE') {
        fetchEmailStatus();
        showToast?.('✨ Google Gmail account connected successfully!');
      }
    }
    window.addEventListener('message', handleOAuthMessage);
    return () => window.removeEventListener('message', handleOAuthMessage);
  }, [fetchEmailStatus, showToast]);

  // Connect via Google OAuth 2.0
  const handleConnectGoogle = async () => {
    try {
      setIsConnectingOAuth(true);
      const res = await fetch('/api/v1/integrations/google/auth-url', {
        headers: { ...authHeaders },
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to initiate Google OAuth.');
      }

      const { auth_url } = await res.json();

      // Attempt to open in a popup window
      const width = 520;
      const height = 640;
      const left = window.screen.width / 2 - width / 2;
      const top = window.screen.height / 2 - height / 2;

      const popup = window.open(
        auth_url,
        'JobEazyGoogleAuth',
        `width=${width},height=${height},top=${top},left=${left},status=no,menubar=no,toolbar=no`
      );

      if (!popup || popup.closed || typeof popup.closed === 'undefined') {
        // Popup blocked by browser: fallback to full redirect
        window.location.href = auth_url;
      } else {
        // Poll popup closure as fallback to postMessage
        const pollTimer = setInterval(() => {
          if (popup.closed) {
            clearInterval(pollTimer);
            fetchEmailStatus();
          }
        }, 1200);
      }
    } catch (err) {
      showToast?.(err.message || 'Error connecting to Google.');
      // If platform OAuth isn't configured, switch to SMTP tab automatically
      if (err.message?.toLowerCase().includes('not configured')) {
        setActiveSubMode('smtp');
      }
    } finally {
      setIsConnectingOAuth(false);
    }
  };

  // Disconnect active email
  const handleDisconnect = async () => {
    const provider = emailStatus.provider || 'google';
    if (!confirm(`Are you sure you want to disconnect ${emailStatus.email || 'your email'}?`)) {
      return;
    }

    try {
      setIsDisconnecting(true);
      const endpoint =
        provider === 'smtp'
          ? '/api/v1/integrations/smtp/disconnect'
          : '/api/v1/integrations/google/disconnect';

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { ...authHeaders },
      });

      if (res.ok) {
        showToast?.('Email account disconnected.');
        await fetchEmailStatus();
      } else {
        throw new Error('Failed to disconnect email account.');
      }
    } catch (err) {
      showToast?.(err.message || 'Error disconnecting account.');
    } finally {
      setIsDisconnecting(false);
    }
  };

  // Connect via Direct SMTP / App Password
  const handleConnectSmtp = async (e) => {
    e.preventDefault();
    setSmtpError(null);

    if (!smtpEmail.trim() || !smtpPassword.trim()) {
      setSmtpError('Please enter both your email and App Password.');
      return;
    }

    try {
      setIsConnectingSmtp(true);
      const res = await fetch('/api/v1/integrations/smtp/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify({
          email: smtpEmail.trim(),
          app_password: smtpPassword.trim(),
          host: 'smtp.gmail.com',
          port: 587,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to authenticate via SMTP.');
      }

      showToast?.(`✨ Connected email dispatch via Gmail (${data.email})!`);
      setSmtpPassword('');
      await fetchEmailStatus();
    } catch (err) {
      setSmtpError(err.message || 'Failed to verify SMTP credentials.');
    } finally {
      setIsConnectingSmtp(false);
    }
  };

  if (isLoading) {
    return (
      <div className="tab-pane-content animate-fadeIn">
        <div className="section-card text-center p-8">
          <div className="spinner-border mb-3" />
          <p className="text-secondary">Checking email integration status...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tab-pane-content animate-fadeIn">
      {/* HEADER SECTION */}
      <div className="section-header-row mb-6">
        <div>
          <h2 className="section-title flex-align-center gap-2">
            <Mail className="text-emerald" size={20} />
            <span>Email & Outbound Dispatch Connection</span>
          </h2>
          <p className="section-description">
            Connect your personal email to enable 1-click verified outbound job applications, direct recruiter outreach, and automated Gmail draft composition.
          </p>
        </div>
      </div>

      {/* ACTIVE CONNECTION CARD (IF CONNECTED) */}
      {emailStatus.connected ? (
        <div className="section-card border-emerald mb-6">
          <div className="connected-account-banner flex-between items-center p-4">
            <div className="flex items-center gap-4">
              <div className="connected-avatar-circle">
                <Mail size={24} className="text-emerald" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="badge-connected-dot" />
                  <strong className="text-lg text-emerald">
                    {emailStatus.provider === 'google'
                      ? 'Connected via Google OAuth 2.0'
                      : 'Connected via Gmail App Password (SMTP)'}
                  </strong>
                </div>
                <div className="text-secondary text-sm mt-1">
                  Active Dispatch Account: <strong>{emailStatus.email}</strong>
                </div>
                <div className="text-muted text-xs mt-1">
                  {emailStatus.provider === 'google'
                    ? 'Official Google Gmail API (Offline access enabled, automatic refresh)'
                    : 'Direct SMTP Transmission (STARTTLS smtp.gmail.com:587)'}
                </div>
              </div>
            </div>

            <button
              type="button"
              className="btn-danger-outline flex items-center gap-2 px-4 py-2"
              onClick={handleDisconnect}
              disabled={isDisconnecting}
            >
              <Trash2 size={15} />
              <span>{isDisconnecting ? 'Disconnecting...' : 'Disconnect Account'}</span>
            </button>
          </div>
        </div>
      ) : (
        /* DISCONNECTED STATE: DUAL OPTION CARDS */
        <div className="email-connection-options-grid">
          {/* OPTION SELECTOR TABS */}
          <div className="sub-tab-group mb-5">
            <button
              type="button"
              className={`sub-tab-btn ${activeSubMode === 'oauth' ? 'active' : ''}`}
              onClick={() => setActiveSubMode('oauth')}
            >
              <Sparkles size={15} />
              <span>Option 1: Google OAuth 2.0 (1-Click)</span>
              {emailStatus.platform_oauth_configured && (
                <span className="badge-chip-green">Ready</span>
              )}
            </button>
            <button
              type="button"
              className={`sub-tab-btn ${activeSubMode === 'smtp' ? 'active' : ''}`}
              onClick={() => setActiveSubMode('smtp')}
            >
              <Key size={15} />
              <span>Option 2: Gmail App Password (Instant SMTP)</span>
              <span className="badge-chip-blue">Zero Setup</span>
            </button>
          </div>

          {/* SUB-PANE 1: GOOGLE OAUTH 2.0 */}
          {activeSubMode === 'oauth' && (
            <div className="section-card p-6">
              <div className="flex items-start gap-4">
                <div className="provider-logo-wrap google">
                  <svg width="24" height="24" viewBox="0 0 24 24">
                    <path
                      fill="#4285F4"
                      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                    />
                    <path
                      fill="#34A853"
                      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                    />
                    <path
                      fill="#FBBC05"
                      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                    />
                    <path
                      fill="#EA4335"
                      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                    />
                  </svg>
                </div>

                <div className="flex-1">
                  <h3 className="text-base font-bold text-primary mb-1">
                    Google OAuth 2.0 Official Integration
                  </h3>
                  <p className="text-secondary text-sm mb-4">
                    Connect securely using Google’s OAuth consent screen. Allows JobEazy to generate Gmail drafts and execute verified human-approved dispatches with zero password storage.
                  </p>

                  {emailStatus.platform_oauth_configured ? (
                    <div className="oauth-action-area">
                      <button
                        type="button"
                        className="btn-primary flex items-center gap-2 px-5 py-2.5"
                        onClick={handleConnectGoogle}
                        disabled={isConnectingOAuth}
                      >
                        <Sparkles size={16} />
                        <span>{isConnectingOAuth ? 'Connecting to Google...' : 'Connect Gmail Account'}</span>
                      </button>
                      <span className="text-muted text-xs block mt-2">
                        Opens official Google consent window. Requires <code>gmail.compose</code> and <code>gmail.send</code> offline permissions.
                      </span>
                    </div>
                  ) : (
                    <div className="advisory-banner amber p-4 rounded-md">
                      <div className="flex items-start gap-2">
                        <AlertCircle size={18} className="text-amber flex-shrink-0 mt-0.5" />
                        <div>
                          <strong className="text-sm text-amber">Platform Google OAuth App Not Configured Yet</strong>
                          <p className="text-xs text-secondary mt-1">
                            The platform SuperAdmin has not yet entered Google Cloud Client ID & Secret in the Admin Ops Center.
                          </p>
                          <div className="mt-3 flex items-center gap-3">
                            <button
                              type="button"
                              className="btn-secondary-xs"
                              onClick={() => setActiveSubMode('smtp')}
                            >
                              Connect via Gmail App Password Instead →
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* SUB-PANE 2: GMAIL APP PASSWORD (SMTP) */}
          {activeSubMode === 'smtp' && (
            <div className="section-card p-6">
              <div className="flex items-start gap-4">
                <div className="provider-logo-wrap smtp">
                  <Key size={24} className="text-primary" />
                </div>

                <div className="flex-1">
                  <h3 className="text-base font-bold text-primary mb-1">
                    Connect via Gmail App Password (SMTP)
                  </h3>
                  <p className="text-secondary text-sm mb-4">
                    No Google Cloud Console setup required! Generate a secure 16-character App Password directly in your Google Account to enable immediate email dispatch.
                  </p>

                  {smtpError && (
                    <div className="alert-error-bar mb-4 p-3 rounded text-sm flex items-start gap-2">
                      <AlertCircle size={16} className="text-red flex-shrink-0 mt-0.5" />
                      <span>{smtpError}</span>
                    </div>
                  )}

                  <form onSubmit={handleConnectSmtp} className="smtp-connect-form">
                    <div className="form-group mb-3">
                      <label className="form-label text-xs">Your Gmail Address</label>
                      <input
                        type="email"
                        className="form-control"
                        placeholder="you@gmail.com"
                        value={smtpEmail}
                        onChange={(e) => setSmtpEmail(e.target.value)}
                        required
                      />
                    </div>

                    <div className="form-group mb-4">
                      <div className="flex-between items-center mb-1">
                        <label className="form-label text-xs">16-Character Google App Password</label>
                        <a
                          href="https://myaccount.google.com/apppasswords"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-emerald flex items-center gap-1"
                        >
                          <span>Generate in Google Account</span>
                          <ExternalLink size={12} />
                        </a>
                      </div>
                      <div className="input-with-icon-right">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          className="form-control"
                          placeholder="abcd efgh ijkl mnop"
                          value={smtpPassword}
                          onChange={(e) => setSmtpPassword(e.target.value)}
                          required
                        />
                        <button
                          type="button"
                          className="btn-icon-inside"
                          onClick={() => setShowPassword(!showPassword)}
                          title={showPassword ? 'Hide password' : 'Show password'}
                        >
                          {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                        </button>
                      </div>
                      <span className="text-muted text-xs mt-1 block">
                        Requires 2-Step Verification to be ON. Go to: Google Account → Security → 2-Step Verification → App passwords.
                      </span>
                    </div>

                    <button
                      type="submit"
                      className="btn-primary flex items-center gap-2 px-5 py-2"
                      disabled={isConnectingSmtp}
                    >
                      <ShieldCheck size={16} />
                      <span>{isConnectingSmtp ? 'Verifying SMTP Connection...' : 'Verify & Connect Email'}</span>
                    </button>
                  </form>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* DISPATCH SECURITY & PRIVACY FOOTER CARD */}
      <div className="section-card bg-surface-subtle mt-6 p-4">
        <div className="flex items-start gap-3">
          <ShieldCheck size={18} className="text-emerald flex-shrink-0 mt-0.5" />
          <div className="text-xs text-secondary">
            <strong className="text-primary">Human-in-the-Loop Send Guarantee:</strong> JobEazy never auto-sends emails without your explicit, interactive confirmation. All outbound dispatches require prior fact-checking, ATS pass validation, and an explicit review step in Application Studio or Pipeline Monitor.
          </div>
        </div>
      </div>
    </div>
  );
}

