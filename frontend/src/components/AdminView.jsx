import React, { useState, useEffect } from 'react';
import {
  Users,
  Server,
  Layers,
  FileCode,
  ShieldCheck,
  ShieldAlert,
  Play,
  RefreshCw,
  Plus,
  Key,
  CheckCircle,
  XCircle,
  AlertTriangle,
  ArrowRight,
  Sliders,
  TrendingUp,
  Cpu,
  Trash2,
  ExternalLink,
} from 'lucide-react';

const API_BASE = '/api/v1';

export default function AdminView({
  currentSuperadminId,
  onImpersonateTenant,
  showToast,
}) {
  const [activeTab, setActiveTab] = useState('tenants'); // tenants | providers | sources | templates | flagged
  const [metrics, setMetrics] = useState(null);
  const [loadingMetrics, setLoadingMetrics] = useState(true);

  // Tenants State
  const [tenants, setTenants] = useState([]);
  const [loadingTenants, setLoadingTenants] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [newTenantEmail, setNewTenantEmail] = useState('');
  const [newTenantTier, setNewTenantTier] = useState('free');
  const [newTenantRole, setNewTenantRole] = useState('tenant');

  // Providers State
  const [providers, setProviders] = useState([]);
  const [loadingProviders, setLoadingProviders] = useState(false);
  const [testingProviderId, setTestingProviderId] = useState(null);
  const [showAddProviderModal, setShowAddProviderModal] = useState(false);
  const [newProviderForm, setNewProviderForm] = useState({
    provider: 'openai',
    model_name: 'gpt-4o-mini',
    api_key: '',
    priority: 1,
  });

  // Sources State
  const [sources, setSources] = useState([]);
  const [loadingSources, setLoadingSources] = useState(false);
  const [isTriggeringIngest, setIsTriggeringIngest] = useState(false);
  const [ingestQuery, setIngestQuery] = useState('AI Engineer');
  const [ingestCountry, setIngestCountry] = useState('gb');

  // Templates State
  const [templates, setTemplates] = useState([]);
  const [loadingTemplates, setLoadingTemplates] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(null);

  // Flagged Jobs
  const [flaggedJobs, setFlaggedJobs] = useState([]);
  const [loadingFlagged, setLoadingFlagged] = useState(false);

  useEffect(() => {
    fetchMetrics();
    if (activeTab === 'tenants') fetchTenants();
    if (activeTab === 'providers') fetchProviders();
    if (activeTab === 'sources') fetchSources();
    if (activeTab === 'templates') fetchTemplates();
    if (activeTab === 'flagged') fetchFlaggedJobs();
  }, [activeTab]);

  const fetchMetrics = async () => {
    try {
      setLoadingMetrics(true);
      const res = await fetch(`${API_BASE}/admin/metrics`);
      if (res.ok) {
        setMetrics(await res.json());
      }
    } catch (err) {
      console.error('Failed to fetch metrics:', err);
    } finally {
      setLoadingMetrics(false);
    }
  };

  const fetchTenants = async () => {
    try {
      setLoadingTenants(true);
      const res = await fetch(`${API_BASE}/admin/tenants`);
      if (res.ok) {
        setTenants(await res.json());
      }
    } catch (err) {
      console.error('Failed to fetch tenants:', err);
    } finally {
      setLoadingTenants(false);
    }
  };

  const fetchProviders = async () => {
    try {
      setLoadingProviders(true);
      const res = await fetch(`${API_BASE}/admin/llm-providers`);
      if (res.ok) {
        setProviders(await res.json());
      }
    } catch (err) {
      console.error('Failed to fetch providers:', err);
    } finally {
      setLoadingProviders(false);
    }
  };

  const fetchSources = async () => {
    try {
      setLoadingSources(true);
      const res = await fetch(`${API_BASE}/admin/jobs/sources`);
      if (res.ok) {
        setSources(await res.json());
      }
    } catch (err) {
      console.error('Failed to fetch sources:', err);
    } finally {
      setLoadingSources(false);
    }
  };

  const fetchTemplates = async () => {
    try {
      setLoadingTemplates(true);
      const res = await fetch(`${API_BASE}/admin/templates`);
      if (res.ok) {
        const data = await res.json();
        setTemplates(data);
        if (data.length > 0 && !selectedTemplate) {
          setSelectedTemplate(data[0]);
        }
      }
    } catch (err) {
      console.error('Failed to fetch templates:', err);
    } finally {
      setLoadingTemplates(false);
    }
  };

  const fetchFlaggedJobs = async () => {
    try {
      setLoadingFlagged(true);
      const res = await fetch(`${API_BASE}/admin/jobs/flagged?limit=50`);
      if (res.ok) {
        setFlaggedJobs(await res.json());
      }
    } catch (err) {
      console.error('Failed to fetch flagged jobs:', err);
    } finally {
      setLoadingFlagged(false);
    }
  };

  // --- Actions ---

  const handleCreateTenant = async (e) => {
    e.preventDefault();
    if (!newTenantEmail) return;
    try {
      const res = await fetch(`${API_BASE}/admin/tenants`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: newTenantEmail,
          plan_tier: newTenantTier,
          role: newTenantRole,
          status: 'active',
        }),
      });
      if (res.ok) {
        showToast?.(`Tenant ${newTenantEmail} created successfully!`);
        setShowInviteModal(false);
        setNewTenantEmail('');
        fetchTenants();
        fetchMetrics();
      } else {
        const err = await res.json();
        showToast?.(err.detail || 'Failed to create tenant');
      }
    } catch (err) {
      showToast?.('Error creating tenant');
    }
  };

  const handleToggleTenantStatus = async (tenant) => {
    const nextStatus = tenant.status === 'active' ? 'suspended' : 'active';
    try {
      const res = await fetch(`${API_BASE}/admin/tenants/${tenant.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus }),
      });
      if (res.ok) {
        showToast?.(`Tenant status updated to ${nextStatus}`);
        fetchTenants();
        fetchMetrics();
      }
    } catch (err) {
      showToast?.('Failed to update tenant status');
    }
  };

  const handleTestProvider = async (providerId) => {
    try {
      setTestingProviderId(providerId);
      const res = await fetch(`${API_BASE}/admin/llm-providers/${providerId}/test`, {
        method: 'POST',
      });
      if (res.ok) {
        const result = await res.json();
        if (result.status === 'connected') {
          showToast?.(`Connected to ${result.provider} (${result.model}): "${result.response}"`);
        } else {
          showToast?.(`Connection issue: ${result.error || 'Failed'}`);
        }
      }
    } catch (err) {
      showToast?.('Provider connection test failed');
    } finally {
      setTestingProviderId(null);
    }
  };

  const handleTriggerIngest = async () => {
    try {
      setIsTriggeringIngest(true);
      const res = await fetch(`${API_BASE}/admin/jobs/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: ingestQuery,
          country: ingestCountry,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        showToast?.(`Ingestion complete! Fetched ${data.total_fetched}, Saved ${data.saved_count} jobs.`);
        fetchMetrics();
        fetchSources();
      } else {
        showToast?.('Job ingestion failed');
      }
    } catch (err) {
      showToast?.('Error triggering ingestion');
    } finally {
      setIsTriggeringIngest(false);
    }
  };

  return (
    <div className="admin-container animate-fadeIn">
      {/* Top Header */}
      <div className="admin-header">
        <div>
          <div className="admin-badge-wrap">
            <span className="admin-pill">
              <ShieldCheck size={14} className="icon-emerald" /> SUPERADMIN COMMAND CENTER
            </span>
            <span className="admin-mode-pill">Multi-Tenant Mode: Active</span>
          </div>
          <h2 className="admin-title">SaaS Control & Orchestration Plane</h2>
          <p className="admin-subtitle">
            Manage tenant workspaces, configure dynamic LLM failover, supervise job ingestion sources, and audit safety gates.
          </p>
        </div>

        <div className="admin-header-actions">
          <button
            className="btn-refresh"
            onClick={() => {
              fetchMetrics();
              if (activeTab === 'tenants') fetchTenants();
              if (activeTab === 'providers') fetchProviders();
              if (activeTab === 'sources') fetchSources();
            }}
            title="Refresh metrics"
          >
            <RefreshCw size={15} />
          </button>
          <button
            className="btn-primary"
            onClick={() => setShowInviteModal(true)}
          >
            <Plus size={16} /> Invite / Add Tenant
          </button>
        </div>
      </div>

      {/* Metric Bento Grid */}
      <div className="admin-bento-grid">
        <div className="admin-metric-card">
          <div className="metric-header">
            <span className="metric-label">Tenants & Workspaces</span>
            <Users size={18} className="metric-icon" />
          </div>
          <div className="metric-val">{metrics?.total_tenants ?? '—'}</div>
          <div className="metric-sub">
            <span className="text-emerald">{metrics?.active_tenants ?? 0} active</span> • 0 suspended
          </div>
        </div>

        <div className="admin-metric-card">
          <div className="metric-header">
            <span className="metric-label">Clean Ingested Jobs</span>
            <Layers size={18} className="metric-icon" />
          </div>
          <div className="metric-val">{metrics?.clean_jobs ?? '—'}</div>
          <div className="metric-sub">
            out of <span className="text-white">{metrics?.total_jobs ?? 0} total</span> in database
          </div>
        </div>

        <div className="admin-metric-card">
          <div className="metric-header">
            <span className="metric-label">Posting Guard Flags</span>
            <ShieldAlert size={18} className="metric-icon text-amber" />
          </div>
          <div className="metric-val text-amber">{metrics?.flagged_jobs ?? '—'}</div>
          <div className="metric-sub">
            prompt injections & invisible text trapped
          </div>
        </div>

        <div className="admin-metric-card">
          <div className="metric-header">
            <span className="metric-label">Primary LLM Engine</span>
            <Cpu size={18} className="metric-icon text-indigo" />
          </div>
          <div className="metric-val text-capitalize">{metrics?.active_provider ?? 'OpenAI'}</div>
          <div className="metric-sub text-mono">
            {metrics?.active_model ?? 'gpt-4o-mini'} (Priority 1)
          </div>
        </div>
      </div>

      {/* Admin Module Tabs */}
      <div className="admin-nav-tabs">
        <button
          className={`admin-tab-btn ${activeTab === 'tenants' ? 'active' : ''}`}
          onClick={() => setActiveTab('tenants')}
        >
          <Users size={16} /> Tenants & Workspaces
        </button>
        <button
          className={`admin-tab-btn ${activeTab === 'providers' ? 'active' : ''}`}
          onClick={() => setActiveTab('providers')}
        >
          <Server size={16} /> Dynamic LLM Providers
        </button>
        <button
          className={`admin-tab-btn ${activeTab === 'sources' ? 'active' : ''}`}
          onClick={() => setActiveTab('sources')}
        >
          <Layers size={16} /> Job Sources & Sourcing
        </button>
        <button
          className={`admin-tab-btn ${activeTab === 'templates' ? 'active' : ''}`}
          onClick={() => setActiveTab('templates')}
        >
          <FileCode size={16} /> Global LaTeX Templates
        </button>
        <button
          className={`admin-tab-btn ${activeTab === 'flagged' ? 'active' : ''}`}
          onClick={() => setActiveTab('flagged')}
        >
          <AlertTriangle size={16} /> Flagged Postings ({metrics?.flagged_jobs ?? 0})
        </button>
      </div>

      {/* TAB CONTENT 1: Tenants */}
      {activeTab === 'tenants' && (
        <div className="admin-card-panel animate-fadeIn">
          <div className="panel-title-bar">
            <div>
              <h3 className="panel-heading">Registered SaaS Tenants</h3>
              <p className="panel-desc">
                Every tenant has a strictly isolated data partition (`account_id`). Click "Test As Tenant" to impersonate Niloy or any user.
              </p>
            </div>
            <button className="btn-secondary" onClick={fetchTenants}>
              <RefreshCw size={14} className={loadingTenants ? 'spin' : ''} /> Refresh
            </button>
          </div>

          <div className="table-responsive">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Tenant Email</th>
                  <th>Role</th>
                  <th>Plan Tier</th>
                  <th>Status</th>
                  <th>Jobs Partition</th>
                  <th>Applications</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tenants.map((t) => (
                  <tr key={t.id} className={t.email === 'niloy@example.com' ? 'row-highlight' : ''}>
                    <td>
                      <div className="tenant-email-cell">
                        <strong>{t.email}</strong>
                        {t.email === 'niloy@example.com' && (
                          <span className="badge-qa">Niloy (QA Dogfood)</span>
                        )}
                      </div>
                      <span className="tenant-uuid-muted">{t.id}</span>
                    </td>
                    <td>
                      <span className={`badge-role ${t.role}`}>
                        {t.role}
                      </span>
                    </td>
                    <td>
                      <span className="badge-tier">{t.plan_tier}</span>
                    </td>
                    <td>
                      <span className={`status-dot-pill ${t.status}`}>
                        {t.status}
                      </span>
                    </td>
                    <td>
                      <strong>{t.jobs_count}</strong> jobs
                    </td>
                    <td>
                      <strong>{t.applications_count}</strong> drafted
                    </td>
                    <td className="text-muted text-sm">
                      {new Date(t.created_at).toLocaleDateString()}
                    </td>
                    <td>
                      <div className="action-buttons-wrap">
                        <button
                          className="btn-action-test"
                          onClick={() => onImpersonateTenant(t)}
                          title="Switch to this tenant workspace to test real job applying"
                        >
                          🧪 Test As Tenant
                        </button>
                        <button
                          className="btn-action-status"
                          onClick={() => handleToggleTenantStatus(t)}
                          title={t.status === 'active' ? 'Suspend tenant' : 'Activate tenant'}
                        >
                          {t.status === 'active' ? 'Suspend' : 'Activate'}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB CONTENT 2: LLM Providers */}
      {activeTab === 'providers' && (
        <div className="admin-card-panel animate-fadeIn">
          <div className="panel-title-bar">
            <div>
              <h3 className="panel-heading">Dynamic LLM Provider Failover Engine</h3>
              <p className="panel-desc">
                Configured providers in order of priority. If Provider #1 (OpenAI) rate limits or errors, traffic falls over to Provider #2 automatically.
              </p>
            </div>
            <button className="btn-primary" onClick={() => setShowAddProviderModal(true)}>
              <Plus size={14} /> Add Provider
            </button>
          </div>

          <div className="providers-grid">
            {providers.map((p) => (
              <div key={p.id} className={`provider-card ${p.is_active ? 'active-provider' : ''}`}>
                <div className="provider-card-top">
                  <div className="provider-brand">
                    <Server size={20} className="icon-emerald" />
                    <div>
                      <h4 className="provider-name text-capitalize">{p.provider}</h4>
                      <span className="provider-model text-mono">{p.model_name}</span>
                    </div>
                  </div>
                  <div className="provider-priority-pill">
                    Priority #{p.priority}
                  </div>
                </div>

                <div className="provider-details">
                  <div className="detail-row">
                    <span>Active Status:</span>
                    <strong className={p.is_active ? 'text-emerald' : 'text-muted'}>
                      {p.is_active ? 'Enabled' : 'Disabled'}
                    </strong>
                  </div>
                  <div className="detail-row">
                    <span>API Key Encrypted:</span>
                    <strong>{p.has_api_key ? '✓ Present at rest' : '⚠️ Missing'}</strong>
                  </div>
                  <div className="detail-row">
                    <span>Scope:</span>
                    <strong>{p.account_id ? 'Tenant Override' : 'Global Platform Default'}</strong>
                  </div>
                </div>

                <div className="provider-actions">
                  <button
                    className="btn-secondary"
                    onClick={() => handleTestProvider(p.id)}
                    disabled={testingProviderId === p.id}
                  >
                    <Play size={13} /> {testingProviderId === p.id ? 'Pinging...' : 'Test Ping'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB CONTENT 3: Sources & Sourcing Trigger */}
      {activeTab === 'sources' && (
        <div className="admin-card-panel animate-fadeIn">
          <div className="panel-title-bar">
            <div>
              <h3 className="panel-heading">Job Ingestion Sources & Manual Dispatch</h3>
              <p className="panel-desc">
                All 6 legal sourcing adapters implementing `JobSource.fetch()`. Run an immediate multi-source fetch below.
              </p>
            </div>
          </div>

          {/* Trigger Ingestion Box */}
          <div className="admin-trigger-box">
            <h4 className="trigger-box-title">⚡ Trigger On-Demand Multi-Source Job Search</h4>
            <div className="trigger-controls">
              <input
                type="text"
                className="input-admin"
                value={ingestQuery}
                onChange={(e) => setIngestQuery(e.target.value)}
                placeholder="Search Query (e.g. AI Engineer, LLM Engineer)"
              />
              <select
                className="select-admin"
                value={ingestCountry}
                onChange={(e) => setIngestCountry(e.target.value)}
              >
                <option value="gb">United Kingdom (gb)</option>
                <option value="us">United States (us)</option>
                <option value="de">Germany (de)</option>
                <option value="nl">Netherlands (nl)</option>
              </select>
              <button
                className="btn-primary"
                onClick={handleTriggerIngest}
                disabled={isTriggeringIngest}
              >
                {isTriggeringIngest ? 'Sourcing Jobs...' : 'Trigger Ingestion'}
              </button>
            </div>
          </div>

          <div className="sources-table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Job Source</th>
                  <th>Legal Layer</th>
                  <th>Access Scope</th>
                  <th>Total Ingested</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {sources.map((s) => (
                  <tr key={s.name}>
                    <td>
                      <strong>{s.display_name}</strong>
                    </td>
                    <td>
                      <span className="badge-legal">{s.legal_layer}</span>
                    </td>
                    <td>
                      {s.is_restricted ? (
                        <span className="badge-restricted">Niloy QA Only</span>
                      ) : (
                        <span className="badge-general">All Tenants</span>
                      )}
                    </td>
                    <td>
                      <strong>{s.jobs_count}</strong> jobs
                    </td>
                    <td className="text-muted text-sm">{s.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB CONTENT 4: Global Templates */}
      {activeTab === 'templates' && (
        <div className="admin-card-panel animate-fadeIn">
          <div className="panel-title-bar">
            <div>
              <h3 className="panel-heading">Global Curated LaTeX CV Templates</h3>
              <p className="panel-desc">
                Templates curated by admin (`account_id = None`) available to all tenants for CV tailoring.
              </p>
            </div>
          </div>

          <div className="templates-split-layout">
            <div className="templates-list-pane">
              {templates.map((tmpl) => (
                <div
                  key={tmpl.id}
                  className={`template-list-card ${selectedTemplate?.id === tmpl.id ? 'active' : ''}`}
                  onClick={() => setSelectedTemplate(tmpl)}
                >
                  <div className="template-card-header">
                    <strong>{tmpl.name}</strong>
                    {tmpl.is_admin_default && <span className="badge-default">System Default</span>}
                  </div>
                  <p className="text-muted text-sm">{tmpl.description || 'Curated LaTeX template'}</p>
                </div>
              ))}
            </div>

            <div className="template-preview-pane">
              {selectedTemplate ? (
                <div>
                  <div className="preview-top-bar">
                    <h4>Editing: {selectedTemplate.name}</h4>
                    <span className="badge-tag">LaTeX Source Code</span>
                  </div>
                  <pre className="latex-editor-pre">{selectedTemplate.latex_source}</pre>
                </div>
              ) : (
                <p className="text-muted">Select a template on the left to preview.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT 5: Flagged Postings */}
      {activeTab === 'flagged' && (
        <div className="admin-card-panel animate-fadeIn">
          <div className="panel-title-bar">
            <div>
              <h3 className="panel-heading">Posting Integrity Guard Audit Log</h3>
              <p className="panel-desc">
                Job postings flagged for potential prompt injection, invisible instructions, or suspect text layers before LLM evaluation.
              </p>
            </div>
          </div>

          <div className="table-responsive">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Job Title & Company</th>
                  <th>Source</th>
                  <th>Integrity Status</th>
                  <th>Found At</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {flaggedJobs.map((j) => (
                  <tr key={j.id}>
                    <td>
                      <strong>{j.role}</strong>
                      <div className="text-muted text-sm">{j.company} • {j.country || 'Remote'}</div>
                    </td>
                    <td>
                      <span className="badge-tier">{j.source}</span>
                    </td>
                    <td>
                      <span className="badge-flagged">⚠️ {j.integrity_status}</span>
                    </td>
                    <td className="text-muted text-sm">
                      {new Date(j.found_at).toLocaleDateString()}
                    </td>
                    <td>
                      <a
                        href={j.apply_link}
                        target="_blank"
                        rel="noreferrer"
                        className="btn-link-view"
                      >
                        <ExternalLink size={13} /> View External
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Invite Modal */}
      {showInviteModal && (
        <div className="modal-backdrop">
          <div className="modal-content animate-scaleIn">
            <h3 className="modal-title">Invite New SaaS Tenant</h3>
            <p className="modal-desc">
              Create an isolated tenant partition with free or custom entitlements.
            </p>
            <form onSubmit={handleCreateTenant}>
              <div className="form-group">
                <label>Tenant Email Address</label>
                <input
                  type="email"
                  required
                  className="input-admin"
                  placeholder="e.g. colleague@example.com"
                  value={newTenantEmail}
                  onChange={(e) => setNewTenantEmail(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label>Plan Tier</label>
                <select
                  className="select-admin"
                  value={newTenantTier}
                  onChange={(e) => setNewTenantTier(e.target.value)}
                >
                  <option value="free">Free Tier (Personal Validation)</option>
                  <option value="pro">Pro Tier ($19/mo)</option>
                  <option value="unlimited">Unlimited / Internal QA</option>
                </select>
              </div>

              <div className="form-group">
                <label>Role</label>
                <select
                  className="select-admin"
                  value={newTenantRole}
                  onChange={(e) => setNewTenantRole(e.target.value)}
                >
                  <option value="tenant">Regular Tenant User</option>
                  <option value="superadmin">Superadmin</option>
                </select>
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowInviteModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Create Tenant
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
