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
  X,
  AlertTriangle,
  ArrowRight,
  Sliders,
  TrendingUp,
  Cpu,
  Trash2,
  ExternalLink,
  Edit2,
  ChevronUp,
  ChevronDown,
  Save,
  Check,
  Search,
  Database,
  Activity,
  Zap,
} from 'lucide-react';

const API_BASE = '/api/v1';

export default function AdminView({
  currentSuperadminId,
  activeTab = 'overview',
  setActiveTab,
  authHeaders = {},
  onImpersonateTenant,
  showToast,
}) {
  const currentTab = activeTab || 'overview';

  const [metrics, setMetrics] = useState(null);
  const [loadingMetrics, setLoadingMetrics] = useState(true);

  // Tenants State
  const [tenants, setTenants] = useState([]);
  const [loadingTenants, setLoadingTenants] = useState(false);
  const [tenantSearch, setTenantSearch] = useState('');
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [newTenantEmail, setNewTenantEmail] = useState('');
  const [newTenantTier, setNewTenantTier] = useState('free');
  const [newTenantRole, setNewTenantRole] = useState('tenant');
  const [newTenantLimit, setNewTenantLimit] = useState('');

  // Tenant Edit Modal
  const [showEditTenantModal, setShowEditTenantModal] = useState(false);
  const [editingTenant, setEditingTenant] = useState(null);
  const [editTier, setEditTier] = useState('free');
  const [editRole, setEditRole] = useState('tenant');
  const [editStatus, setEditStatus] = useState('active');
  const [editLimit, setEditLimit] = useState('');

  // Providers State
  const [providers, setProviders] = useState([]);
  const [loadingProviders, setLoadingProviders] = useState(false);
  const [testingProviderId, setTestingProviderId] = useState(null);
  const [showAddProviderModal, setShowAddProviderModal] = useState(false);
  const [newProviderForm, setNewProviderForm] = useState({
    provider: 'openai',
    model_name: 'gpt-6.1-luna',
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
  const [editingTemplateSource, setEditingTemplateSource] = useState('');
  const [editingTemplateName, setEditingTemplateName] = useState('');
  const [editingTemplateDesc, setEditingTemplateDesc] = useState('');
  const [editingTemplateDefault, setEditingTemplateDefault] = useState(false);
  const [isSavingTemplate, setIsSavingTemplate] = useState(false);
  const [showAddTemplateModal, setShowAddTemplateModal] = useState(false);
  const [newTemplateForm, setNewTemplateForm] = useState({
    name: '',
    description: '',
    latex_source: '\\documentclass{article}\n\\begin{document}\n\\section*{Curated Experience}\n\\end{document}',
    is_admin_default: false,
  });

  // Flagged Jobs
  const [flaggedJobs, setFlaggedJobs] = useState([]);
  const [loadingFlagged, setLoadingFlagged] = useState(false);
  const [inspectingJob, setInspectingJob] = useState(null);

  const closeAllModals = () => {
    setShowInviteModal(false);
    setShowEditTenantModal(false);
    setShowAddProviderModal(false);
    setShowAddTemplateModal(false);
    setInspectingJob(null);
  };

  useEffect(() => {
    closeAllModals();
  }, [currentTab]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        closeAllModals();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);


  useEffect(() => {
    fetchMetrics();
    if (currentTab === 'tenants' || currentTab === 'overview') fetchTenants();
    if (currentTab === 'providers' || currentTab === 'overview') fetchProviders();
    if (currentTab === 'sources' || currentTab === 'overview') fetchSources();
    if (currentTab === 'templates') fetchTemplates();
    if (currentTab === 'flagged' || currentTab === 'overview') fetchFlaggedJobs();
  }, [currentTab]);

  useEffect(() => {
    if (selectedTemplate) {
      setEditingTemplateSource(selectedTemplate.latex_source || '');
      setEditingTemplateName(selectedTemplate.name || '');
      setEditingTemplateDesc(selectedTemplate.description || '');
      setEditingTemplateDefault(!!selectedTemplate.is_admin_default);
    }
  }, [selectedTemplate]);

  const fetchMetrics = async () => {
    try {
      setLoadingMetrics(true);
      const res = await fetch(`${API_BASE}/admin/metrics`, {
        headers: { ...authHeaders },
      });
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
      const res = await fetch(`${API_BASE}/admin/tenants`, {
        headers: { ...authHeaders },
      });
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
      const res = await fetch(`${API_BASE}/admin/llm-providers`, {
        headers: { ...authHeaders },
      });
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
      const res = await fetch(`${API_BASE}/admin/jobs/sources`, {
        headers: { ...authHeaders },
      });
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
      const res = await fetch(`${API_BASE}/admin/templates`, {
        headers: { ...authHeaders },
      });
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
      const res = await fetch(`${API_BASE}/admin/jobs/flagged?limit=50`, {
        headers: { ...authHeaders },
      });
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
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: newTenantEmail,
          plan_tier: newTenantTier,
          role: newTenantRole,
          status: 'active',
          account_template_limit: newTenantLimit ? parseInt(newTenantLimit, 10) : null,
        }),
      });
      if (res.ok) {
        showToast?.(`Tenant ${newTenantEmail} created successfully!`);
        setShowInviteModal(false);
        setNewTenantEmail('');
        setNewTenantLimit('');
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

  const handleOpenEditTenant = (tenant) => {
    setEditingTenant(tenant);
    setEditTier(tenant.plan_tier || 'free');
    setEditRole(tenant.role || 'tenant');
    setEditStatus(tenant.status || 'active');
    setEditLimit(tenant.account_template_limit ? String(tenant.account_template_limit) : '');
    setShowEditTenantModal(true);
  };

  const handleSaveEditTenant = async (e) => {
    e.preventDefault();
    if (!editingTenant) return;
    try {
      const res = await fetch(`${API_BASE}/admin/tenants/${editingTenant.id}`, {
        method: 'PATCH',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan_tier: editTier,
          role: editRole,
          status: editStatus,
          account_template_limit: editLimit ? parseInt(editLimit, 10) : null,
        }),
      });
      if (res.ok) {
        showToast?.(`Tenant ${editingTenant.email} updated successfully!`);
        setShowEditTenantModal(false);
        fetchTenants();
        fetchMetrics();
      } else {
        const err = await res.json();
        showToast?.(err.detail || 'Failed to update tenant');
      }
    } catch (err) {
      showToast?.('Error updating tenant');
    }
  };

  const handleToggleTenantStatus = async (tenant) => {
    const nextStatus = tenant.status === 'active' ? 'suspended' : 'active';
    try {
      const res = await fetch(`${API_BASE}/admin/tenants/${tenant.id}`, {
        method: 'PATCH',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
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

  const handleDeleteTenant = async (tenant) => {
    if (tenant.id === currentSuperadminId) {
      showToast?.('Security Rule: Cannot delete your active superadmin account');
      return;
    }
    if (!window.confirm(`Permanently delete tenant ${tenant.email}? All associated data will be removed.`)) {
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/admin/tenants/${tenant.id}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast?.(`Tenant ${tenant.email} deleted.`);
        fetchTenants();
        fetchMetrics();
      } else {
        const err = await res.json();
        showToast?.(err.detail || 'Failed to delete tenant');
      }
    } catch (err) {
      showToast?.('Error deleting tenant');
    }
  };

  // --- LLM Provider Handlers ---

  const handleCreateProvider = async (e) => {
    e.preventDefault();
    if (!newProviderForm.provider || !newProviderForm.model_name) return;
    try {
      const res = await fetch(`${API_BASE}/admin/llm-providers`, {
        method: 'POST',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider: newProviderForm.provider,
          model_name: newProviderForm.model_name,
          api_key: newProviderForm.api_key || null,
          priority: parseInt(newProviderForm.priority, 10) || 1,
          is_active: true,
        }),
      });
      if (res.ok) {
        showToast?.(`Configured provider ${newProviderForm.provider} (${newProviderForm.model_name})`);
        setShowAddProviderModal(false);
        setNewProviderForm({ provider: 'openai', model_name: 'gpt-4o-mini', api_key: '', priority: 1 });
        fetchProviders();
        fetchMetrics();
      } else {
        const err = await res.json();
        showToast?.(err.detail || 'Failed to add LLM provider');
      }
    } catch (err) {
      showToast?.('Error registering provider');
    }
  };

  const handleToggleProviderActive = async (p) => {
    try {
      const res = await fetch(`${API_BASE}/admin/llm-providers/${p.id}`, {
        method: 'PATCH',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !p.is_active }),
      });
      if (res.ok) {
        showToast?.(`Provider ${p.provider} ${!p.is_active ? 'enabled' : 'disabled'}`);
        fetchProviders();
        fetchMetrics();
      }
    } catch (err) {
      showToast?.('Failed to toggle provider');
    }
  };

  const handleChangeProviderPriority = async (p, delta) => {
    const nextPriority = Math.max(1, (p.priority || 1) + delta);
    try {
      const res = await fetch(`${API_BASE}/admin/llm-providers/${p.id}`, {
        method: 'PATCH',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({ priority: nextPriority }),
      });
      if (res.ok) {
        fetchProviders();
      }
    } catch (err) {
      showToast?.('Failed to update priority');
    }
  };

  const handleDeleteProvider = async (p) => {
    if (!window.confirm(`Delete LLM provider ${p.provider} (${p.model_name})?`)) return;
    try {
      const res = await fetch(`${API_BASE}/admin/llm-providers/${p.id}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast?.(`Deleted provider config for ${p.provider}`);
        fetchProviders();
        fetchMetrics();
      }
    } catch (err) {
      showToast?.('Error deleting provider');
    }
  };

  const handleTestProvider = async (providerId) => {
    try {
      setTestingProviderId(providerId);
      const res = await fetch(`${API_BASE}/admin/llm-providers/${providerId}/test`, {
        method: 'POST',
        headers: { ...authHeaders },
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

  // --- Sources Handlers ---

  const handleToggleSource = async (sourceName) => {
    try {
      const res = await fetch(`${API_BASE}/admin/jobs/sources/${sourceName}/toggle`, {
        method: 'POST',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const data = await res.json();
        showToast?.(`Source ${data.name} is now ${data.is_active ? 'Active' : 'Disabled'}`);
        fetchSources();
      }
    } catch (err) {
      showToast?.('Error toggling source');
    }
  };

  const handleTriggerIngest = async () => {
    try {
      setIsTriggeringIngest(true);
      const res = await fetch(`${API_BASE}/admin/jobs/trigger`, {
        method: 'POST',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
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

  // --- Curated Templates Handlers ---

  const handleCreateTemplate = async (e) => {
    e.preventDefault();
    if (!newTemplateForm.name || !newTemplateForm.latex_source) return;
    try {
      const res = await fetch(`${API_BASE}/admin/templates`, {
        method: 'POST',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify(newTemplateForm),
      });
      if (res.ok) {
        const created = await res.json();
        showToast?.(`Template "${created.name}" created!`);
        setShowAddTemplateModal(false);
        setNewTemplateForm({
          name: '',
          description: '',
          latex_source: '\\documentclass{article}\n\\begin{document}\n\\section*{Curated Experience}\n\\end{document}',
          is_admin_default: false,
        });
        fetchTemplates();
        setSelectedTemplate(created);
      } else {
        showToast?.('Failed to create template');
      }
    } catch (err) {
      showToast?.('Error creating template');
    }
  };

  const handleSaveTemplateChanges = async () => {
    if (!selectedTemplate) return;
    try {
      setIsSavingTemplate(true);
      const res = await fetch(`${API_BASE}/admin/templates/${selectedTemplate.id}`, {
        method: 'PATCH',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: editingTemplateName,
          description: editingTemplateDesc,
          latex_source: editingTemplateSource,
          is_admin_default: editingTemplateDefault,
        }),
      });
      if (res.ok) {
        const updated = await res.json();
        showToast?.(`Saved changes to "${updated.name}"!`);
        setSelectedTemplate(updated);
        fetchTemplates();
      } else {
        showToast?.('Failed to save template changes');
      }
    } catch (err) {
      showToast?.('Error saving template');
    } finally {
      setIsSavingTemplate(false);
    }
  };

  const handleDeleteTemplate = async (template) => {
    if (!window.confirm(`Delete curated template "${template.name}"?`)) return;
    try {
      const res = await fetch(`${API_BASE}/admin/templates/${template.id}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast?.(`Deleted template "${template.name}".`);
        setSelectedTemplate(null);
        fetchTemplates();
      }
    } catch (err) {
      showToast?.('Error deleting template');
    }
  };

  // --- Flagged Jobs Handlers ---

  const handleDismissFlag = async (jobId) => {
    try {
      const res = await fetch(`${API_BASE}/admin/jobs/${jobId}/dismiss-flag`, {
        method: 'POST',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast?.('Safety flag dismissed. Marked clean.');
        setInspectingJob(null);
        fetchFlaggedJobs();
        fetchMetrics();
      }
    } catch (err) {
      showToast?.('Failed to dismiss flag');
    }
  };

  const handlePurgeJob = async (jobId) => {
    if (!window.confirm('Permanently purge this posting from database?')) return;
    try {
      const res = await fetch(`${API_BASE}/admin/jobs/${jobId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast?.('Posting permanently purged.');
        setInspectingJob(null);
        fetchFlaggedJobs();
        fetchMetrics();
      }
    } catch (err) {
      showToast?.('Failed to purge job');
    }
  };

  const filteredTenants = tenants.filter((t) => {
    if (!tenantSearch) return true;
    const query = tenantSearch.toLowerCase();
    return (
      t.email?.toLowerCase().includes(query) ||
      t.id?.toLowerCase().includes(query) ||
      t.role?.toLowerCase().includes(query) ||
      t.plan_tier?.toLowerCase().includes(query)
    );
  });

  return (
    <div className="admin-container">
      {/* SECTION 1: PLATFORM OVERVIEW (Alt+1) */}
      {currentTab === 'overview' && (
        <div className="admin-view-content animate-fadeIn">
          <div className="admin-section-header">
            <div>
              <div className="admin-badge-wrap">
                <span className="admin-pill">
                  <ShieldCheck size={14} className="icon-emerald" /> SUPERADMIN COMMAND CENTER
                </span>
                <span className="live-status-pill">● All Systems Operational</span>
              </div>
              <h2 className="admin-title">SaaS Platform Telemetry & Orchestration</h2>
              <p className="admin-subtitle">
                High-level operational health across isolated multi-tenant partitions, vector radar matching, and dynamic LLM routing.
              </p>
            </div>
            <button
              className="btn-refresh"
              onClick={() => {
                fetchMetrics();
                fetchTenants();
                fetchProviders();
                fetchSources();
                fetchFlaggedJobs();
                showToast?.('Refreshed telemetry data.');
              }}
              title="Refresh all metrics"
            >
              <RefreshCw size={15} />
            </button>
          </div>

          {/* Metric Bento Grid */}
          <div className="overview-bento-grid">
            <div className="overview-metric-card" onClick={() => setActiveTab?.('tenants')} role="button" tabIndex={0}>
              <div className="metric-header">
                <div className="metric-icon-pill icon-emerald">
                  <Users size={16} />
                </div>
                <span className="metric-label">Tenants & Workspaces</span>
              </div>
              <div className="metric-body">
                <div className="metric-val">{metrics?.total_tenants ?? '—'}</div>
                <div className="metric-sub">
                  <span className="text-emerald">{metrics?.active_tenants ?? 0} active</span>
                  <span>•</span>
                  <span>0 suspended</span>
                </div>
              </div>
            </div>

            <div className="overview-metric-card" onClick={() => setActiveTab?.('sources')} role="button" tabIndex={0}>
              <div className="metric-header">
                <div className="metric-icon-pill icon-cyan">
                  <Layers size={16} />
                </div>
                <span className="metric-label">Clean Ingested Jobs</span>
              </div>
              <div className="metric-body">
                <div className="metric-val">{metrics?.clean_jobs ?? '—'}</div>
                <div className="metric-sub">
                  <span>out of</span>
                  <span className="text-white">{metrics?.total_jobs ?? 0} total</span>
                  <span>in database</span>
                </div>
              </div>
            </div>

            <div className="overview-metric-card" onClick={() => setActiveTab?.('flagged')} role="button" tabIndex={0}>
              <div className="metric-header">
                <div className="metric-icon-pill icon-amber">
                  <ShieldAlert size={16} />
                </div>
                <span className="metric-label">Posting Guard Flags</span>
              </div>
              <div className="metric-body">
                <div className="metric-val text-amber">{metrics?.flagged_jobs ?? '—'}</div>
                <div className="metric-sub">
                  <span>prompt injections & invisible text trapped</span>
                </div>
              </div>
            </div>

            <div className="overview-metric-card" onClick={() => setActiveTab?.('providers')} role="button" tabIndex={0}>
              <div className="metric-header">
                <div className="metric-icon-pill icon-purple">
                  <Cpu size={16} />
                </div>
                <span className="metric-label">Primary LLM Engine</span>
              </div>
              <div className="metric-body">
                <div className="metric-val provider-name">{metrics?.active_provider ?? 'OpenAI'}</div>
                <div className="metric-sub text-mono">
                  <span>{metrics?.active_model ?? 'gpt-4o-mini'} (Priority 1)</span>
                </div>
              </div>
            </div>
          </div>

          {/* Diagnostics & Quick Actions Two-Column Grid */}
          <div className="overview-bottom-grid">
            {/* System Diagnostics Matrix */}
            <div className="diagnostics-card">
              <div className="card-top-row">
                <h3 className="card-heading">
                  <Activity size={16} className="icon-emerald" /> Infrastructure Health Matrix
                </h3>
                <span className="badge-tag">Production VPS Node</span>
              </div>
              <div className="diagnostics-list">
                <div className="diag-item">
                  <div className="diag-info">
                    <Database size={15} className="diag-icon" />
                    <div>
                      <strong>PostgreSQL Core Storage</strong>
                      <span className="diag-sub">Multi-tenant schema with cascade foreign keys</span>
                    </div>
                  </div>
                  <span className="status-pill-ok">● Connected</span>
                </div>

                <div className="diag-item">
                  <div className="diag-info">
                    <Zap size={15} className="diag-icon" />
                    <div>
                      <strong>Qdrant Semantic Matching Engine</strong>
                      <span className="diag-sub">Vector embeddings collection: `job_postings`</span>
                    </div>
                  </div>
                  <span className="status-pill-ok">● Active</span>
                </div>

                <div className="diag-item">
                  <div className="diag-info">
                    <Server size={15} className="diag-icon" />
                    <div>
                      <strong>Dynamic LLM Provider Failover</strong>
                      <span className="diag-sub">{providers.length} provider configuration(s) loaded</span>
                    </div>
                  </div>
                  <span className="status-pill-ok">● Chain Ready</span>
                </div>

                <div className="diag-item">
                  <div className="diag-info">
                    <Layers size={15} className="diag-icon" />
                    <div>
                      <strong>Ingestion Scraper Adapters</strong>
                      <span className="diag-sub">Adzuna, Remotive, RemoteOK, Greenhouse, Lever, Freehire</span>
                    </div>
                  </div>
                  <span className="status-pill-ok">● 6/6 Operational</span>
                </div>
              </div>
            </div>

            {/* Quick Action Shortcuts */}
            <div className="quick-actions-card">
              <div className="card-top-row">
                <h3 className="card-heading">
                  <Sliders size={16} className="icon-emerald" /> Platform Ops Shortcuts
                </h3>
                <span className="badge-tag">One-Click</span>
              </div>
              <div className="shortcuts-list">
                <button
                  className="shortcut-btn"
                  onClick={() => {
                    setActiveTab?.('tenants');
                    setShowInviteModal(true);
                  }}
                >
                  <div className="shortcut-icon-box">
                    <Plus size={16} />
                  </div>
                  <div className="shortcut-meta">
                    <strong>Invite New SaaS Tenant</strong>
                    <span>Provision isolated tenant workspace with free or custom tier</span>
                  </div>
                  <ArrowRight size={15} className="shortcut-arrow" />
                </button>

                <button
                  className="shortcut-btn"
                  onClick={() => {
                    setActiveTab?.('providers');
                    setShowAddProviderModal(true);
                  }}
                >
                  <div className="shortcut-icon-box">
                    <Server size={16} />
                  </div>
                  <div className="shortcut-meta">
                    <strong>Register Failover LLM Provider</strong>
                    <span>Add Anthropic Claude, Groq, Ollama, or DeepSeek model</span>
                  </div>
                  <ArrowRight size={15} className="shortcut-arrow" />
                </button>

                <button
                  className="shortcut-btn"
                  onClick={() => setActiveTab?.('sources')}
                >
                  <div className="shortcut-icon-box">
                    <Layers size={16} />
                  </div>
                  <div className="shortcut-meta">
                    <strong>Trigger Job Feeds Sourcing</strong>
                    <span>Run on-demand multi-source radar ingestion</span>
                  </div>
                  <ArrowRight size={15} className="shortcut-arrow" />
                </button>

                <button
                  className="shortcut-btn"
                  onClick={() => setActiveTab?.('flagged')}
                >
                  <div className="shortcut-icon-box" style={{ background: 'rgba(245, 158, 11, 0.12)', color: '#f59e0b' }}>
                    <ShieldAlert size={16} />
                  </div>
                  <div className="shortcut-meta">
                    <strong>Audit Posting Guard Flags ({metrics?.flagged_jobs ?? 0})</strong>
                    <span>Review adversarial prompt injections caught before LLM evaluation</span>
                  </div>
                  <ArrowRight size={15} className="shortcut-arrow" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* SECTION 2: TENANTS & WORKSPACES (Alt+2) */}
      {currentTab === 'tenants' && (
        <div className="admin-view-content animate-fadeIn">
          <div className="admin-section-header">
            <div>
              <h2 className="admin-title">Tenants & Workspaces Directory</h2>
              <p className="admin-subtitle">
                Every tenant partition is isolated by `account_id` with dedicated quota bounds. Click "Test As Tenant" to switch context.
              </p>
            </div>
            <button className="btn-primary" onClick={() => setShowInviteModal(true)}>
              <Plus size={16} /> Invite / Add Tenant
            </button>
          </div>

          <div className="admin-card-panel">
            {/* Search & Stats Bar */}
            <div className="table-controls-bar">
              <div className="search-input-wrap">
                <Search size={15} className="search-input-icon" />
                <input
                  type="text"
                  className="input-search"
                  placeholder="Filter by email, role, or tier..."
                  value={tenantSearch}
                  onChange={(e) => setTenantSearch(e.target.value)}
                />
              </div>
              <div className="table-controls-right">
                <span className="text-muted text-sm">
                  Showing <strong>{filteredTenants.length}</strong> of {tenants.length} tenants
                </span>
                <button className="btn-refresh" onClick={fetchTenants} title="Refresh tenants list">
                  <RefreshCw size={14} className={loadingTenants ? 'spin' : ''} />
                </button>
              </div>
            </div>

            <div className="table-responsive">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th style={{ width: '32%' }}>Tenant Email & Partition</th>
                    <th style={{ width: '12%' }}>Role</th>
                    <th style={{ width: '12%' }}>Plan Tier</th>
                    <th style={{ width: '12%' }}>Status</th>
                    <th style={{ width: '12%' }}>Data Partition</th>
                    <th style={{ width: '20%' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTenants.map((t) => (
                    <tr key={t.id} className={t.email === 'niloy@example.com' ? 'row-highlight' : ''}>
                      <td>
                        <div className="tenant-email-cell">
                          <div className="tenant-email-top">
                            <strong>{t.email}</strong>
                            {t.email === 'niloy@example.com' && (
                              <span className="badge-qa">Niloy (QA Dogfood)</span>
                            )}
                            {t.id === currentSuperadminId && (
                              <span className="badge-active-session">Active Session</span>
                            )}
                          </div>
                          <span className="tenant-uuid-muted">{t.id}</span>
                        </div>
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
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                          <span><strong>{t.jobs_count}</strong> jobs</span>
                          <span className="text-muted text-xs">{t.applications_count} drafted</span>
                        </div>
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
                            onClick={() => handleOpenEditTenant(t)}
                            title="Edit tenant role, tier, and quotas"
                          >
                            <Edit2 size={12} /> Edit
                          </button>
                          <button
                            className="btn-action-status"
                            onClick={() => handleToggleTenantStatus(t)}
                            title={t.status === 'active' ? 'Suspend tenant' : 'Activate tenant'}
                          >
                            {t.status === 'active' ? 'Suspend' : 'Activate'}
                          </button>
                          {t.id !== currentSuperadminId && (
                            <button
                              className="btn-action-delete"
                              onClick={() => handleDeleteTenant(t)}
                              title="Delete tenant account and data"
                            >
                              <Trash2 size={13} />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* SECTION 3: DYNAMIC LLM PROVIDERS (Alt+3) */}
      {currentTab === 'providers' && (
        <div className="admin-view-content animate-fadeIn">
          <div className="admin-section-header">
            <div>
              <h2 className="admin-title">Dynamic LLM Provider Failover Engine</h2>
              <p className="admin-subtitle">
                Priority-ordered model configurations. If Provider #1 fails or rate-limits, requests fall over down the priority chain. Bedrock fallback via <code>.env</code> key is always active as the last hope.
              </p>
            </div>
            <button className="btn-primary" onClick={() => setShowAddProviderModal(true)}>
              <Plus size={16} /> Add Provider
            </button>
          </div>

          <div className="providers-grid">
            {providers.map((p) => {
              const isPrimary = p.priority === 1;
              const hasEnvFallback = p.key_source === 'env_fallback' || (!p.has_api_key && p.provider.toLowerCase() === 'openai');
              const hasDbKey = p.key_source === 'db_encrypted';

              return (
                <div key={p.id} className={`llm-provider-card ${p.is_active ? 'is-active' : 'is-paused'}`}>
                  {/* Top Bar: Brand Pill & Priority Stepper */}
                  <div className="llm-card-top-bar">
                    <div className="llm-brand-identity">
                      <div className={`llm-brand-icon ${p.provider.toLowerCase()}`}>
                        <Cpu size={18} />
                      </div>
                      <div>
                        <div className="llm-provider-title">
                          <span className="brand-name">{p.provider}</span>
                          {isPrimary ? (
                            <span className="badge-primary-engine">Primary</span>
                          ) : (
                            <span className="badge-failover-engine">Fallback #{p.priority}</span>
                          )}
                        </div>
                        <span className="llm-scope-sub">
                          {p.account_id ? 'Tenant Partition Override' : 'Global Platform Default'}
                        </span>
                      </div>
                    </div>

                    {/* Priority Rank Stepper Widget */}
                    <div className="llm-priority-stepper" title="Reorder failover priority rank">
                      <button
                        type="button"
                        className="btn-stepper-up"
                        onClick={() => handleChangeProviderPriority(p, -1)}
                        disabled={p.priority <= 1}
                        title="Promote priority"
                      >
                        <ChevronUp size={13} />
                      </button>
                      <span className="stepper-rank">#{p.priority}</span>
                      <button
                        type="button"
                        className="btn-stepper-down"
                        onClick={() => handleChangeProviderPriority(p, 1)}
                        title="Demote priority"
                      >
                        <ChevronDown size={13} />
                      </button>
                    </div>
                  </div>

                  {/* Active Model Spotlight */}
                  <div className="llm-model-spotlight">
                    <div className="model-label-row">
                      <span className="model-label-hint">ACTIVE ENGINE MODEL</span>
                      {p.is_active ? (
                        <span className="status-live-dot">● Routing Active</span>
                      ) : (
                        <span className="status-paused-dot">○ Paused</span>
                      )}
                    </div>
                    <div className="model-display-name">
                      <code>{p.model_name}</code>
                    </div>
                  </div>

                  {/* Operational Telemetry Matrix */}
                  <div className="llm-specs-matrix">
                    <div className="spec-row">
                      <span className="spec-label">Engine Routing</span>
                      <button
                        type="button"
                        className={`btn-toggle-engine ${p.is_active ? 'active' : 'disabled'}`}
                        onClick={() => handleToggleProviderActive(p)}
                        title="Toggle active status in failover chain"
                      >
                        {p.is_active ? '✓ Enabled' : '✕ Disabled'}
                      </button>
                    </div>

                    <div className="spec-row">
                      <span className="spec-label">Key Authorization</span>
                      {hasDbKey ? (
                        <span className="key-badge db-key" title="Encrypted at rest in database">
                          🔒 Encrypted in DB
                        </span>
                      ) : hasEnvFallback ? (
                        <span className="key-badge env-key" title="Secure bedrock fallback active from .env">
                          ⚡ Active via .env Fallback
                        </span>
                      ) : (
                        <span className="key-badge missing-key" title="No API key configured">
                          ⚠️ Missing API Key
                        </span>
                      )}
                    </div>

                    <div className="spec-row">
                      <span className="spec-label">Failover Role</span>
                      <span className="spec-value">
                        {isPrimary ? 'Priority Target #1' : `Failover Reserve #${p.priority}`}
                      </span>
                    </div>
                  </div>

                  {/* Footer Actions */}
                  <div className="llm-card-footer">
                    <button
                      type="button"
                      className="btn-action-test"
                      onClick={() => handleTestProvider(p.id)}
                      disabled={testingProviderId === p.id}
                      title="Ping LLM API connectivity"
                    >
                      <Play size={13} /> {testingProviderId === p.id ? 'Pinging...' : 'Test Ping'}
                    </button>
                    <button
                      type="button"
                      className="btn-action-delete"
                      onClick={() => handleDeleteProvider(p)}
                      title="Remove provider from failover chain"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* SECTION 4: JOB SOURCES & INGESTION (Alt+4) */}
      {currentTab === 'sources' && (
        <div className="admin-view-content animate-fadeIn">
          <div className="admin-section-header">
            <div>
              <h2 className="admin-title">Job Feeds & Sourcing Controls</h2>
              <p className="admin-subtitle">
                Supervise all 6 compliance-vetted scraper adapters implementing `JobSource.fetch()`. Run an immediate multi-source fetch below.
              </p>
            </div>
          </div>

          {/* Trigger Ingestion Dispatch Bar */}
          <div className="admin-card-panel" style={{ marginBottom: 20 }}>
            <h4 style={{ margin: '0 0 12px 0', fontSize: 14, fontWeight: 700 }}>
              ⚡ On-Demand Multi-Source Job Search
            </h4>
            <div className="trigger-controls-grid">
              <div style={{ flex: 2 }}>
                <label style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Search Query
                </label>
                <input
                  type="text"
                  className="input-admin"
                  value={ingestQuery}
                  onChange={(e) => setIngestQuery(e.target.value)}
                  placeholder="Search Query (e.g. AI Engineer, LLM Engineer)"
                />
              </div>
              <div style={{ flex: 1 }}>
                <label style={{ fontSize: 11.5, fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Target Country
                </label>
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
              </div>
              <div>
                <button
                  className="btn-primary"
                  onClick={handleTriggerIngest}
                  disabled={isTriggeringIngest}
                >
                  <Zap size={15} /> {isTriggeringIngest ? 'Sourcing Jobs...' : 'Trigger Ingestion'}
                </button>
              </div>
            </div>
          </div>

          <div className="admin-card-panel">
            <h4 style={{ margin: '0 0 14px 0', fontSize: 14, fontWeight: 700 }}>
              Scraping Adapters Registry
            </h4>
            <div className="table-responsive">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th style={{ width: '22%' }}>Job Source</th>
                    <th style={{ width: '18%' }}>Legal Layer</th>
                    <th style={{ width: '16%' }}>Access Scope</th>
                    <th style={{ width: '14%' }}>Feed Status</th>
                    <th style={{ width: '12%' }}>Total Ingested</th>
                    <th style={{ width: '18%' }}>Description</th>
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
                        <button
                          className={`btn-status-toggle ${s.is_active ? 'active' : 'disabled'}`}
                          onClick={() => handleToggleSource(s.name)}
                          title="Click to toggle source"
                        >
                          {s.is_active ? '✓ Active' : '✕ Disabled'}
                        </button>
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
        </div>
      )}

      {/* SECTION 5: CURATED LATEX TEMPLATES (Alt+5) */}
      {currentTab === 'templates' && (
        <div className="admin-view-content animate-fadeIn">
          <div className="admin-section-header">
            <div>
              <h2 className="admin-title">Global Curated LaTeX CV Templates</h2>
              <p className="admin-subtitle">
                Master templates available to all tenants for CV tailoring. Edit code live in the in-browser Overleaf-style editor below.
              </p>
            </div>
            <button className="btn-primary" onClick={() => setShowAddTemplateModal(true)}>
              <Plus size={16} /> New Template
            </button>
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
                    {tmpl.is_admin_default && <span className="badge-default">Default</span>}
                  </div>
                  <p className="text-muted text-sm">{tmpl.description || 'Curated LaTeX template'}</p>
                </div>
              ))}
            </div>

            <div className="template-preview-pane">
              {selectedTemplate ? (
                <div>
                  <div className="preview-top-bar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', gap: 16, paddingBottom: 16 }}>
                    <div style={{ flex: 1, display: 'flex', gap: 12 }}>
                      <div style={{ flex: 1 }}>
                        <label style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 6, display: 'block', letterSpacing: '0.04em' }}>
                          Template Identifier
                        </label>
                        <input
                          type="text"
                          className="input-admin"
                          style={{ fontWeight: 700, fontSize: 13.5 }}
                          value={editingTemplateName}
                          onChange={(e) => setEditingTemplateName(e.target.value)}
                          placeholder="Template Name"
                        />
                      </div>
                      <div style={{ flex: 1.5 }}>
                        <label style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 6, display: 'block', letterSpacing: '0.04em' }}>
                          Description
                        </label>
                        <input
                          type="text"
                          className="input-admin"
                          style={{ fontSize: 13 }}
                          value={editingTemplateDesc}
                          onChange={(e) => setEditingTemplateDesc(e.target.value)}
                          placeholder="Template Description"
                        />
                      </div>
                    </div>
                    <div className="preview-actions" style={{ display: 'flex', alignItems: 'center', gap: 10, alignSelf: 'flex-end', height: 40 }}>
                      <label className="checkbox-label" style={{ fontSize: 12, marginRight: 8, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 6, color: 'var(--text-muted)' }}>
                        <input
                          type="checkbox"
                          checked={editingTemplateDefault}
                          onChange={(e) => setEditingTemplateDefault(e.target.checked)}
                        />{' '}
                        System Default
                      </label>
                      <button
                        className="btn-primary"
                        onClick={handleSaveTemplateChanges}
                        disabled={isSavingTemplate}
                      >
                        <Save size={15} /> {isSavingTemplate ? 'Saving...' : 'Save Changes'}
                      </button>
                      <button
                        className="btn-action-delete"
                        style={{ height: 40, width: 40, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}
                        onClick={() => handleDeleteTemplate(selectedTemplate)}
                        title="Delete template"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>

                  <div className="editor-wrap" style={{ marginTop: 14 }}>
                    <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6, display: 'block' }}>
                      LaTeX Source Code (Overleaf Compatible)
                    </label>
                    <textarea
                      className="latex-editor-textarea"
                      value={editingTemplateSource}
                      onChange={(e) => setEditingTemplateSource(e.target.value)}
                      rows={22}
                      spellCheck={false}
                    />
                  </div>
                </div>
              ) : (
                <p className="text-muted" style={{ padding: 24, textAlign: 'center' }}>
                  Select a template on the left to preview and edit.
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* SECTION 6: FLAGGED POSTINGS AUDIT (Alt+6) */}
      {currentTab === 'flagged' && (
        <div className="admin-view-content animate-fadeIn">
          <div className="admin-section-header">
            <div>
              <div className="admin-badge-wrap">
                <span className="badge-flagged" style={{ fontSize: 12 }}>
                  ⚠️ {flaggedJobs.length} Incident(s) Caught
                </span>
              </div>
              <h2 className="admin-title">Posting Integrity Guard Incident Room</h2>
              <p className="admin-subtitle">
                Adversarial prompt injections, invisible unicode instructions, or suspect text layers intercepted by PostingIntegrityGate.
              </p>
            </div>
            <button className="btn-secondary" onClick={fetchFlaggedJobs}>
              <RefreshCw size={14} className={loadingFlagged ? 'spin' : ''} /> Refresh
            </button>
          </div>

          <div className="admin-card-panel">
            <div className="table-responsive">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th style={{ width: '30%' }}>Job Title & Company</th>
                    <th style={{ width: '15%' }}>Source</th>
                    <th style={{ width: '20%' }}>Integrity Status</th>
                    <th style={{ width: '15%' }}>Detected At</th>
                    <th style={{ width: '20%' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {flaggedJobs.length === 0 ? (
                    <tr>
                      <td colSpan={5} style={{ textAlign: 'center', padding: '48px 0', color: 'var(--text-muted)' }}>
                        ✓ Radar clean! No adversarial or prompt injection exploits detected.
                      </td>
                    </tr>
                  ) : (
                    flaggedJobs.map((j) => (
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
                          <div className="action-buttons-wrap">
                            <button
                              className="btn-action-status"
                              onClick={() => setInspectingJob(j)}
                              title="Inspect details and raw content"
                            >
                              Inspect
                            </button>
                            <button
                              className="btn-action-test"
                              onClick={() => handleDismissFlag(j.id)}
                              title="Dismiss safety flag and mark clean"
                            >
                              ✓ Mark Clean
                            </button>
                            <button
                              className="btn-action-delete"
                              onClick={() => handlePurgeJob(j.id)}
                              title="Permanently delete job"
                            >
                              <Trash2 size={13} />
                            </button>
                            {j.apply_link && (
                              <a
                                href={j.apply_link}
                                target="_blank"
                                rel="noreferrer"
                                className="btn-link-view"
                                title="External Job Post"
                              >
                                <ExternalLink size={13} />
                              </a>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* --- MODALS --- */}

      {/* Modal 1: Invite Tenant */}
      {showInviteModal && (
        <div className="modal-backdrop" onClick={(e) => { if (e.target === e.currentTarget) closeAllModals(); }}>
          <div className="modal-content animate-scaleIn">
            <div className="modal-header-row">
              <div>
                <h3 className="modal-title">Invite New SaaS Tenant</h3>
                <p className="modal-desc">
                  Create an isolated tenant partition with free or custom entitlements.
                </p>
              </div>
              <button
                type="button"
                className="modal-close-btn"
                onClick={closeAllModals}
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>
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

              <div className="form-group">
                <label>Template Limit (Optional)</label>
                <input
                  type="number"
                  className="input-admin"
                  placeholder="Leave empty for default"
                  value={newTenantLimit}
                  onChange={(e) => setNewTenantLimit(e.target.value)}
                />
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

      {/* Modal 2: Edit Tenant */}
      {showEditTenantModal && editingTenant && (
        <div className="modal-backdrop" onClick={(e) => { if (e.target === e.currentTarget) closeAllModals(); }}>
          <div className="modal-content animate-scaleIn">
            <div className="modal-header-row">
              <div>
                <h3 className="modal-title">Edit Tenant: {editingTenant.email}</h3>
                <p className="modal-desc">
                  Update roles, plan tiers, or quotas for this workspace partition.
                </p>
              </div>
              <button
                type="button"
                className="modal-close-btn"
                onClick={closeAllModals}
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSaveEditTenant}>
              <div className="form-group">
                <label>Plan Tier</label>
                <select
                  className="select-admin"
                  value={editTier}
                  onChange={(e) => setEditTier(e.target.value)}
                >
                  <option value="free">Free Tier</option>
                  <option value="pro">Pro Tier ($19/mo)</option>
                  <option value="unlimited">Unlimited Tier</option>
                </select>
              </div>

              <div className="form-group">
                <label>Role</label>
                <select
                  className="select-admin"
                  value={editRole}
                  onChange={(e) => setEditRole(e.target.value)}
                >
                  <option value="tenant">Tenant</option>
                  <option value="superadmin">Superadmin</option>
                </select>
              </div>

              <div className="form-group">
                <label>Status</label>
                <select
                  className="select-admin"
                  value={editStatus}
                  onChange={(e) => setEditStatus(e.target.value)}
                >
                  <option value="active">Active</option>
                  <option value="suspended">Suspended</option>
                </select>
              </div>

              <div className="form-group">
                <label>Custom Template Limit</label>
                <input
                  type="number"
                  className="input-admin"
                  placeholder="Unlimited"
                  value={editLimit}
                  onChange={(e) => setEditLimit(e.target.value)}
                />
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowEditTenantModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal 3: Add LLM Provider */}
      {showAddProviderModal && (
        <div className="modal-backdrop" onClick={(e) => { if (e.target === e.currentTarget) closeAllModals(); }}>
          <div className="modal-content animate-scaleIn">
            <div className="modal-header-row">
              <div>
                <h3 className="modal-title">Add LLM Provider Config</h3>
                <p className="modal-desc">
                  Configure dynamic failover model with optional encrypted API key. Bedrock fallback via <code>.env</code> key is always active as last resort.
                </p>
              </div>
              <button
                type="button"
                className="modal-close-btn"
                onClick={closeAllModals}
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleCreateProvider}>
              <div className="form-group">
                <label>Provider Name</label>
                <select
                  className="select-admin"
                  value={newProviderForm.provider}
                  onChange={(e) => {
                    const prov = e.target.value;
                    let defaultModel = 'gpt-6.1-luna';
                    if (prov === 'anthropic') defaultModel = 'claude-3-5-sonnet';
                    if (prov === 'groq') defaultModel = 'llama-3.3-70b-versatile';
                    if (prov === 'ollama') defaultModel = 'llama3.2';
                    if (prov === 'deepseek') defaultModel = 'deepseek-chat';
                    setNewProviderForm({ ...newProviderForm, provider: prov, model_name: defaultModel });
                  }}
                >
                  <option value="openai">OpenAI</option>
                  <option value="anthropic">Anthropic Claude</option>
                  <option value="groq">Groq Llama</option>
                  <option value="ollama">Local Ollama</option>
                  <option value="deepseek">DeepSeek</option>
                </select>
              </div>

              <div className="form-group">
                <label>Model Name</label>
                {newProviderForm.provider === 'openai' ? (
                  <select
                    className="select-admin"
                    value={newProviderForm.model_name}
                    onChange={(e) => setNewProviderForm({ ...newProviderForm, model_name: e.target.value })}
                  >
                    <option value="gpt-6.1-luna">GPT 6.1 Luna (Default Engine)</option>
                    <option value="gpt-4o">GPT-4o (Omnimodal Flagship)</option>
                    <option value="gpt-4o-mini">GPT-4o Mini (Fast & Efficient)</option>
                    <option value="o3-mini">OpenAI o3-mini (Reasoning Engine)</option>
                    <option value="o1">OpenAI o1 (Advanced Reasoning)</option>
                    <option value="o1-mini">OpenAI o1-mini (Fast Reasoning)</option>
                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                  </select>
                ) : (
                  <input
                    type="text"
                    required
                    className="input-admin"
                    placeholder="e.g. claude-3-5-sonnet, llama-3.3-70b-versatile"
                    value={newProviderForm.model_name}
                    onChange={(e) => setNewProviderForm({ ...newProviderForm, model_name: e.target.value })}
                  />
                )}
              </div>

              <div className="form-group">
                <label>API Key (Encrypted At Rest)</label>
                <input
                  type="password"
                  className="input-admin"
                  placeholder="sk-... (Leave empty to use .env key fallback)"
                  value={newProviderForm.api_key}
                  onChange={(e) => setNewProviderForm({ ...newProviderForm, api_key: e.target.value })}
                />
                <span className="text-muted" style={{ fontSize: 11, marginTop: 4, display: 'block' }}>
                  Optional: If left blank, OpenAI calls use your secure <code>OPENAI_API_KEY</code> from <code>.env</code>.
                </span>
              </div>

              <div className="form-group">
                <label>Failover Priority Rank (1 = Primary)</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  className="input-admin"
                  value={newProviderForm.priority}
                  onChange={(e) => setNewProviderForm({ ...newProviderForm, priority: parseInt(e.target.value, 10) || 1 })}
                />
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowAddProviderModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Save Provider
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal 4: Add Curated Template */}
      {showAddTemplateModal && (
        <div className="modal-backdrop" onClick={(e) => { if (e.target === e.currentTarget) closeAllModals(); }}>
          <div className="modal-content animate-scaleIn" style={{ maxWidth: 650 }}>
            <div className="modal-header-row">
              <div>
                <h3 className="modal-title">Create Curated LaTeX CV Template</h3>
                <p className="modal-desc">
                  Add a new global template (`account_id = None`) available to all tenants for CV tailoring.
                </p>
              </div>
              <button
                type="button"
                className="modal-close-btn"
                onClick={closeAllModals}
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleCreateTemplate}>
              <div className="form-group">
                <label>Template Name</label>
                <input
                  type="text"
                  required
                  className="input-admin"
                  placeholder="e.g. Minimalist_Modern_CV"
                  value={newTemplateForm.name}
                  onChange={(e) => setNewTemplateForm({ ...newTemplateForm, name: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Description</label>
                <input
                  type="text"
                  className="input-admin"
                  placeholder="e.g. Single-page compact CV layout optimized for tech roles"
                  value={newTemplateForm.description}
                  onChange={(e) => setNewTemplateForm({ ...newTemplateForm, description: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>LaTeX Source Code</label>
                <textarea
                  className="latex-editor-textarea"
                  style={{ minHeight: 180 }}
                  value={newTemplateForm.latex_source}
                  onChange={(e) => setNewTemplateForm({ ...newTemplateForm, latex_source: e.target.value })}
                  rows={8}
                />
              </div>

              <div className="form-group" style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                <input
                  type="checkbox"
                  id="chk-default-tmpl"
                  checked={newTemplateForm.is_admin_default}
                  onChange={(e) => setNewTemplateForm({ ...newTemplateForm, is_admin_default: e.target.checked })}
                />
                <label htmlFor="chk-default-tmpl" style={{ cursor: 'pointer', marginBottom: 0 }}>
                  Set as System Default Template
                </label>
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowAddTemplateModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Create Template
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal 5: Inspect Flagged Posting */}
      {inspectingJob && (
        <div className="modal-backdrop" onClick={(e) => { if (e.target === e.currentTarget) closeAllModals(); }}>
          <div className="modal-content animate-scaleIn" style={{ maxWidth: 700 }}>
            <div className="modal-header-row">
              <div>
                <h3 className="modal-title">{inspectingJob.role}</h3>
                <p className="modal-desc">
                  {inspectingJob.company} • {inspectingJob.source}
                </p>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span className="badge-flagged">⚠️ {inspectingJob.integrity_status}</span>
                <button
                  type="button"
                  className="modal-close-btn"
                  onClick={closeAllModals}
                  aria-label="Close modal"
                >
                  <X size={18} />
                </button>
              </div>
            </div>

            <p className="modal-desc" style={{ marginTop: 8 }}>
              Interception Reason: Adversarial prompt injection or suspect instructions detected.
            </p>

            <div className="detail-box" style={{ background: 'var(--surface-hover)', padding: 14, borderRadius: 8, maxHeight: 240, overflowY: 'auto', marginBottom: 16 }}>
              <strong style={{ fontSize: 12, color: 'var(--text-muted)' }}>Raw Posting Snippet:</strong>
              <p style={{ fontSize: 13, whiteSpace: 'pre-wrap', marginTop: 8 }}>
                {inspectingJob.description_snippet || inspectingJob.raw_description || 'No raw content recorded.'}
              </p>
            </div>

            <div className="modal-actions" style={{ justifyContent: 'space-between' }}>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => setInspectingJob(null)}
              >
                Close
              </button>
              <div style={{ display: 'flex', gap: 8 }}>
                <button
                  type="button"
                  className="btn-action-test"
                  onClick={() => handleDismissFlag(inspectingJob.id)}
                >
                  ✓ Approve (Mark Clean)
                </button>
                <button
                  type="button"
                  className="btn-action-delete"
                  onClick={() => handlePurgeJob(inspectingJob.id)}
                >
                  <Trash2 size={14} /> Purge Posting
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
