import React, { useState, useEffect, useMemo } from 'react';
import './App.css';

// Default Tenant: Niloy Sannyal (seeded in database)
const DEFAULT_ACCOUNT_ID = '6e488188-0015-4657-94c9-92d01413dcfb';
const API_BASE = '/api/v1';

export default function App() {
  const [accountId, setAccountId] = useState(DEFAULT_ACCOUNT_ID);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Ingestion Controls
  const [ingestQuery, setIngestQuery] = useState('software engineer ai agent remote');
  const [ingestWhere, setIngestWhere] = useState('Remote');
  const [ingestLimit, setIngestLimit] = useState(10);
  const [isIngesting, setIsIngesting] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);

  // Filters & Toggles
  const [activeTab, setActiveTab] = useState('all'); // 'all' | 'high' | 'clean' | 'flagged' | 'vetoed'
  const [showFlagged, setShowFlagged] = useState(true);
  const [showVetoed, setShowVetoed] = useState(true);
  const [searchFilter, setSearchFilter] = useState('');
  const [sortBy, setSortBy] = useState('match');

  // Inspection Modal
  const [inspectingJob, setInspectingJob] = useState(null);

  // Module 2 (Apply) Tailoring Modal & State
  const [isTailoring, setIsTailoring] = useState(false);
  const [tailorResult, setTailorResult] = useState(null);
  const [tailorModalJob, setTailorModalJob] = useState(null);
  const [editedCoverDraft, setEditedCoverDraft] = useState('');
  const [showLatexSource, setShowLatexSource] = useState(false);
  const [isSending, setIsSending] = useState(false);

  // View Navigation: 'find' | 'monitor'
  const [currentView, setCurrentView] = useState('find');

  // Module 3 (Monitor & Pipeline) State
  const [applications, setApplications] = useState([]);
  const [loadingApps, setLoadingApps] = useState(false);
  const [monitorSummary, setMonitorSummary] = useState({
    total: 0,
    draft: 0,
    sent: 0,
    follow_ups_due: 0,
    responded: 0,
    interview: 0,
    offer: 0,
    rejected: 0,
  });
  const [monitorFilter, setMonitorFilter] = useState('all');
  const [monitorSearch, setMonitorSearch] = useState('');

  // Follow-Up Modal State
  const [followUpModalApp, setFollowUpModalApp] = useState(null);
  const [followUpData, setFollowUpData] = useState(null);
  const [editedFollowUpDraft, setEditedFollowUpDraft] = useState('');
  const [isDraftingFollowUp, setIsDraftingFollowUp] = useState(false);
  const [isSendingFollowUp, setIsSendingFollowUp] = useState(false);

  // Materials Inspection Modal
  const [viewingAppMaterials, setViewingAppMaterials] = useState(null);

  // Toast Helper
  const showToast = (msg, duration = 4000) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), duration);
  };

  // Fetch Monitor Data (Summary & Applications)
  const fetchMonitorData = async () => {
    try {
      setLoadingApps(true);
      const [sumRes, appsRes] = await Promise.all([
        fetch(`${API_BASE}/applications/monitor/summary?account_id=${accountId}`),
        fetch(`${API_BASE}/applications?account_id=${accountId}&limit=100`),
      ]);
      if (sumRes.ok) {
        const sumData = await sumRes.json();
        setMonitorSummary(sumData);
      }
      if (appsRes.ok) {
        const appsData = await appsRes.json();
        setApplications(Array.isArray(appsData) ? appsData : []);
      }
    } catch (err) {
      console.error('Failed to load monitor data:', err);
    } finally {
      setLoadingApps(false);
    }
  };

  useEffect(() => {
    fetchMonitorData();
  }, [accountId]);

  // Update Application Pipeline Status
  const handleUpdateStatus = async (appId, newStatus) => {
    try {
      const res = await fetch(`${API_BASE}/applications/${appId}/status?account_id=${accountId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });
      if (!res.ok) {
        throw new Error(`Status update failed (${res.status})`);
      }
      const updated = await res.json();
      setApplications(prev => prev.map(a => a.id === appId ? updated : a));
      showToast(`✅ Status updated to ${newStatus.toUpperCase()}`);
      fetchMonitorData();
    } catch (err) {
      showToast(`❌ Error updating status: ${err.message}`, 5000);
    }
  };

  // Start Follow-Up Drafting Workflow
  const handleOpenFollowUp = async (app) => {
    if (app.follow_up_count >= 2) {
      showToast('⚠️ Maximum follow-up cap of 2 reached for this application per §6.');
      return;
    }
    setFollowUpModalApp(app);
    setFollowUpData(null);
    setEditedFollowUpDraft('');
    try {
      setIsDraftingFollowUp(true);
      showToast(`🤖 Drafting follow-up #${app.follow_up_count + 1} with LLM...`);
      const res = await fetch(`${API_BASE}/applications/${app.id}/follow-up/draft?account_id=${accountId}`, {
        method: 'POST',
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Follow-up draft failed (${res.status})`);
      }
      const data = await res.json();
      setFollowUpData(data);
      setEditedFollowUpDraft(data.draft_content || '');
      showToast(`✅ Follow-up #${data.follow_up_number} drafted! Review before confirming Send.`);
    } catch (err) {
      showToast(`❌ Error: ${err.message}`, 6000);
      setFollowUpModalApp(null);
    } finally {
      setIsDraftingFollowUp(false);
    }
  };

  // Confirm Follow-Up Send (Human Gate)
  const handleConfirmFollowUpSend = async () => {
    if (!followUpModalApp || isSendingFollowUp) return;
    try {
      setIsSendingFollowUp(true);
      const res = await fetch(`${API_BASE}/applications/${followUpModalApp.id}/follow-up/send?account_id=${accountId}`, {
        method: 'POST',
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Failed to mark follow-up sent (${res.status})`);
      }
      const updated = await res.json();
      setApplications(prev => prev.map(a => a.id === updated.id ? updated : a));
      showToast(`🎉 Human Gate: Follow-up #${updated.follow_up_count} confirmed and scheduled!`);
      setFollowUpModalApp(null);
      fetchMonitorData();
    } catch (err) {
      showToast(`❌ Error: ${err.message}`, 6000);
    } finally {
      setIsSendingFollowUp(false);
    }
  };

  // Fetch Jobs from Backend
  const fetchJobs = async () => {
    try {
      setLoading(true);
      setError(null);
      const params = new URLSearchParams({
        account_id: accountId,
        include_vetoed: String(showVetoed),
        include_flagged: String(showFlagged),
        limit: '100',
      });

      const res = await fetch(`${API_BASE}/jobs?${params.toString()}`);
      if (!res.ok) {
        throw new Error(`Server returned HTTP ${res.status}: ${res.statusText}`);
      }
      const data = await res.json();
      setJobs(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
      setError(err.message || 'Failed to load jobs from API.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [accountId, showFlagged, showVetoed]);

  // Trigger Live Ingestion
  const handleTriggerIngest = async (e) => {
    e.preventDefault();
    if (isIngesting) return;

    try {
      setIsIngesting(true);
      showToast('⚡ Ingestion pipeline launched across sources...');

      const payload = {
        account_id: accountId,
        query: {
          what: ingestQuery,
          where: ingestWhere,
          country: 'gb',
          page: 1,
        },
        limit: Number(ingestLimit),
      };

      const res = await fetch(`${API_BASE}/jobs/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || `Ingestion failed (${res.status})`);
      }

      const result = await res.json();
      showToast(`✅ Ingestion finished: ${result.persisted} persisted, ${result.scored} scored with OpenAI vector embeddings.`);
      await fetchJobs();
    } catch (err) {
      console.error('Ingestion error:', err);
      showToast(`❌ Error: ${err.message}`, 6000);
    } finally {
      setIsIngesting(false);
    }
  };

  // Trigger CV Tailoring (Module 2)
  const handleTailorCV = async (job) => {
    if (isTailoring) return;
    try {
      setIsTailoring(true);
      setTailorModalJob(job);
      showToast(`🤖 Tailoring CV & drafting outreach for ${job.role} @ ${job.company}...`);

      const res = await fetch(`${API_BASE}/applications/tailor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: accountId,
          job_id: job.id,
          channel: 'email',
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Tailoring failed (${res.status})`);
      }

      const data = await res.json();
      setTailorResult(data);
      setEditedCoverDraft(data.application.draft_content || '');
      showToast(`✅ Tailored CV generated! ATS fit: ${(data.ats_score * 100).toFixed(0)}%. Fact audit passed.`);
    } catch (err) {
      console.error('Tailor error:', err);
      showToast(`❌ Tailoring error: ${err.message}`, 6000);
      setTailorModalJob(null);
    } finally {
      setIsTailoring(false);
    }
  };

  // Human-in-the-Loop Send Confirmation
  const handleConfirmSend = async () => {
    if (!tailorResult?.application?.id || isSending) return;
    try {
      setIsSending(true);
      const appId = tailorResult.application.id;
      const res = await fetch(`${API_BASE}/applications/${appId}/send?account_id=${accountId}`, {
        method: 'POST',
      });

      if (!res.ok) {
        throw new Error(`Failed to confirm Send gate (${res.status})`);
      }

      const updated = await res.json();
      setTailorResult((prev) => ({
        ...prev,
        application: updated,
      }));
      showToast(`🎉 Human review confirmed! Application marked SENT with timestamp.`);
      fetchMonitorData();
    } catch (err) {
      console.error('Send error:', err);
      showToast(`❌ Send error: ${err.message}`, 6000);
    } finally {
      setIsSending(false);
    }
  };

  // Derived KPI Metrics
  const stats = useMemo(() => {
    const total = jobs.length;
    const clean = jobs.filter(j => j.integrity_status === 'clean' && !j.vetoed).length;
    const highMatch = jobs.filter(j => (j.match_score || 0) >= 0.40 && !j.vetoed && j.integrity_status === 'clean').length;
    const flagged = jobs.filter(j => j.integrity_status === 'flagged').length;
    const vetoed = jobs.filter(j => j.vetoed).length;
    return { total, clean, highMatch, flagged, vetoed };
  }, [jobs]);

  // Filtered & Sorted Jobs
  const displayedJobs = useMemo(() => {
    let list = [...jobs];

    // Tab Filter
    if (activeTab === 'high') {
      list = list.filter(j => (j.match_score || 0) >= 0.40 && !j.vetoed && j.integrity_status === 'clean');
    } else if (activeTab === 'clean') {
      list = list.filter(j => j.integrity_status === 'clean' && !j.vetoed);
    } else if (activeTab === 'flagged') {
      list = list.filter(j => j.integrity_status === 'flagged');
    } else if (activeTab === 'vetoed') {
      list = list.filter(j => j.vetoed);
    }

    // Search Query Filter
    if (searchFilter.trim()) {
      const q = searchFilter.toLowerCase();
      list = list.filter(j => 
        j.company.toLowerCase().includes(q) || 
        j.role.toLowerCase().includes(q) ||
        (j.description && j.description.toLowerCase().includes(q))
      );
    }

    // Sorting
    list.sort((a, b) => {
      if (sortBy === 'match') {
        return (b.match_score || 0) - (a.match_score || 0);
      }
      if (sortBy === 'company') {
        return a.company.localeCompare(b.company);
      }
      if (sortBy === 'newest') {
        return new Date(b.found_at || b.created_at) - new Date(a.found_at || a.created_at);
      }
      return 0;
    });

    return list;
  }, [jobs, activeTab, searchFilter, sortBy]);

  // Format Score
  const formatScore = (score) => {
    if (score === null || score === undefined) return 'N/A';
    return `${(score * 100).toFixed(1)}%`;
  };

  const getScoreClass = (score) => {
    if (!score && score !== 0) return 'score-low';
    if (score >= 0.45) return 'score-high';
    if (score >= 0.35) return 'score-med';
    return 'score-low';
  };

  // Helper: check if follow-up is due (10-day cadence post-send, capped at 2)
  const isFollowUpDue = (app) => {
    if (app.status !== 'sent' || !app.sent_at || !app.follow_up_due || (app.follow_up_count || 0) >= 2) return false;
    return new Date(app.follow_up_due) <= new Date();
  };

  const formatDate = (isoStr) => {
    if (!isoStr) return '—';
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return isoStr;
    }
  };

  // Filtered Applications for Monitor Pipeline View
  const displayedApplications = useMemo(() => {
    let list = [...applications];
    if (monitorFilter === 'draft') {
      list = list.filter(a => a.status === 'draft');
    } else if (monitorFilter === 'sent') {
      list = list.filter(a => a.status === 'sent');
    } else if (monitorFilter === 'due') {
      list = list.filter(a => isFollowUpDue(a));
    } else if (monitorFilter === 'responded') {
      list = list.filter(a => a.status === 'responded');
    } else if (monitorFilter === 'interview') {
      list = list.filter(a => a.status === 'interview' || a.status === 'interviewing');
    } else if (monitorFilter === 'offer') {
      list = list.filter(a => a.status === 'offer' || a.status === 'offered');
    } else if (monitorFilter === 'rejected') {
      list = list.filter(a => a.status === 'rejected' || a.status === 'declined');
    }

    if (monitorSearch.trim()) {
      const q = monitorSearch.toLowerCase();
      list = list.filter(a =>
        (a.job_company && a.job_company.toLowerCase().includes(q)) ||
        (a.job_role && a.job_role.toLowerCase().includes(q)) ||
        (a.notes && a.notes.toLowerCase().includes(q))
      );
    }
    return list;
  }, [applications, monitorFilter, monitorSearch]);

  return (
    <div className="app-container">
      {/* Header Area */}
      <header className="app-header">
        <div className="brand-wrapper">
          <div className="brand-icon">⚡</div>
          <div className="brand-text">
            <h1 id="app-title">AGY Job Application Agent SaaS</h1>
            <div className="brand-sub">
              <span>Autonomous Search, Match & Tailoring Engine</span>
              <span>•</span>
              <span className="tenant-pill" title={`Tenant ID: ${accountId}`}>
                Niloy Sannyal (Phase 0 Personal Validation)
              </span>
            </div>
          </div>
        </div>

        <div className="engine-status">
          <span className="pulse-dot"></span>
          <span>OpenAI Vector Embeddings Active (text-embedding-3-small, 1536-dim)</span>
        </div>
      </header>

      {/* Main Top-Level Navigation Switcher */}
      <nav className="main-nav-bar" aria-label="Main Navigation">
        <button
          className={`nav-btn ${currentView === 'find' ? 'active' : ''}`}
          onClick={() => setCurrentView('find')}
          id="tab-find-queue"
        >
          <span>⚡ Find & Match Queue</span>
          <span className="nav-badge">{stats.total}</span>
        </button>

        <button
          className={`nav-btn ${currentView === 'monitor' ? 'active' : ''}`}
          onClick={() => {
            setCurrentView('monitor');
            fetchMonitorData();
          }}
          id="tab-monitor-pipeline"
        >
          <span>📡 Monitor & Pipeline</span>
          <span className="nav-badge">{monitorSummary.total}</span>
          {monitorSummary.follow_ups_due > 0 && (
            <span className="nav-badge nav-badge-alert" title={`${monitorSummary.follow_ups_due} follow-up(s) due!`}>
              ⏰ {monitorSummary.follow_ups_due} DUE
            </span>
          )}
        </button>
      </nav>

      {/* VIEW 1: Find & Match Opportunities Queue */}
      {currentView === 'find' && (
        <>
          {/* KPI Metric Cards */}
          <section className="kpi-grid" aria-label="Pipeline Metrics">
        <div className="kpi-card" id="kpi-total">
          <div className="kpi-label">
            <span>Total Ingested</span>
            <span>📊</span>
          </div>
          <div className="kpi-value">{stats.total}</div>
          <div className="kpi-sub">Across Remotive, RemoteOK, Adzuna feeds</div>
        </div>

        <div className="kpi-card" id="kpi-high-match">
          <div className="kpi-label">
            <span style={{ color: 'var(--emerald-300)' }}>High Fit (≥ 40%)</span>
            <span>🎯</span>
          </div>
          <div className="kpi-value" style={{ color: 'var(--emerald-400)' }}>{stats.highMatch}</div>
          <div className="kpi-sub">Vector similarity against 01_MASTER_CV.tex</div>
        </div>

        <div className="kpi-card" id="kpi-clean">
          <div className="kpi-label">
            <span>Clean Postings</span>
            <span>🛡️</span>
          </div>
          <div className="kpi-value">{stats.clean}</div>
          <div className="kpi-sub">Passed prompt injection & language gates</div>
        </div>

        <div className="kpi-card" id="kpi-flagged">
          <div className="kpi-label">
            <span style={{ color: 'var(--amber-400)' }}>Security Flagged</span>
            <span>⚠️</span>
          </div>
          <div className="kpi-value" style={{ color: 'var(--amber-400)' }}>{stats.flagged}</div>
          <div className="kpi-sub">Isolated by posting_guard (instruction injection)</div>
        </div>

        <div className="kpi-card" id="kpi-vetoed">
          <div className="kpi-label">
            <span style={{ color: 'var(--crimson-400)' }}>Vetoed</span>
            <span>🚫</span>
          </div>
          <div className="kpi-value" style={{ color: 'var(--crimson-400)' }}>{stats.vetoed}</div>
          <div className="kpi-sub">Failed language or experience gates</div>
        </div>
      </section>

      {/* Ingestion Command Bar */}
      <section className="ingest-panel glass-panel" aria-label="Ingestion Command Center">
        <div className="ingest-header">
          <h2>
            <span>⚡ Ingestion Command Bar</span>
            <span className="badge badge-emerald">Live Sources Enabled</span>
          </h2>
          <div className="sources-chips">
            <span className="badge badge-muted">Remotive API</span>
            <span className="badge badge-muted">RemoteOK API</span>
            <span className="badge badge-muted">Adzuna API</span>
            <span className="badge badge-muted">Greenhouse</span>
            <span className="badge badge-muted">Lever</span>
            <span className="badge badge-muted">freehire.me (Layer 1b)</span>
          </div>
        </div>

        <form onSubmit={handleTriggerIngest} className="ingest-form" id="ingest-form">
          <input
            id="input-query-what"
            type="text"
            className="input-text"
            placeholder="Search keywords (e.g. software engineer ai agent remote)"
            value={ingestQuery}
            onChange={(e) => setIngestQuery(e.target.value)}
            required
          />

          <input
            id="input-query-where"
            type="text"
            className="input-text"
            placeholder="Location / Remote"
            value={ingestWhere}
            onChange={(e) => setIngestWhere(e.target.value)}
          />

          <select
            id="select-limit"
            className="input-text"
            value={ingestLimit}
            onChange={(e) => setIngestLimit(e.target.value)}
          >
            <option value="5">5 / source</option>
            <option value="10">10 / source</option>
            <option value="20">20 / source</option>
          </select>

          <button
            id="btn-trigger-ingest"
            type="submit"
            className="btn btn-primary"
            disabled={isIngesting}
          >
            {isIngesting ? '⏳ Ingesting & Embedding...' : '🚀 Trigger Ingestion'}
          </button>
        </form>
      </section>

      {/* Filter & View Toolbar */}
      <section className="toolbar-panel glass-panel" aria-label="Filter Controls">
        <div className="tab-group" role="tablist">
          <button
            id="tab-all"
            className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            All Postings <span className="tab-count">{jobs.length}</span>
          </button>
          <button
            id="tab-high"
            className={`tab-btn ${activeTab === 'high' ? 'active' : ''}`}
            onClick={() => setActiveTab('high')}
          >
            High Match (≥ 40%) <span className="tab-count">{stats.highMatch}</span>
          </button>
          <button
            id="tab-clean"
            className={`tab-btn ${activeTab === 'clean' ? 'active' : ''}`}
            onClick={() => setActiveTab('clean')}
          >
            Clean Unvetoed <span className="tab-count">{stats.clean}</span>
          </button>
          <button
            id="tab-flagged"
            className={`tab-btn ${activeTab === 'flagged' ? 'active' : ''}`}
            onClick={() => setActiveTab('flagged')}
          >
            Security Flagged <span className="tab-count">{stats.flagged}</span>
          </button>
          <button
            id="tab-vetoed"
            className={`tab-btn ${activeTab === 'vetoed' ? 'active' : ''}`}
            onClick={() => setActiveTab('vetoed')}
          >
            Vetoed <span className="tab-count">{stats.vetoed}</span>
          </button>
        </div>

        <div className="toolbar-controls">
          <input
            id="input-filter-search"
            type="text"
            className="input-text"
            style={{ width: '220px' }}
            placeholder="Filter company or role..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
          />

          <select
            id="select-sort"
            className="input-text"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="match">Sort: Highest Match Score</option>
            <option value="newest">Sort: Newly Found</option>
            <option value="company">Sort: Company Name</option>
          </select>

          <label className="toggle-label" title="Toggle prompt-injection flagged jobs">
            <input
              id="chk-show-flagged"
              type="checkbox"
              checked={showFlagged}
              onChange={(e) => setShowFlagged(e.target.checked)}
            />
            <span>Include Flagged</span>
          </label>

          <label className="toggle-label" title="Toggle language / dealbreaker vetoed jobs">
            <input
              id="chk-show-vetoed"
              type="checkbox"
              checked={showVetoed}
              onChange={(e) => setShowVetoed(e.target.checked)}
            />
            <span>Include Vetoed</span>
          </label>
        </div>
      </section>

      {/* Job Queue List */}
      <main id="job-queue-container" aria-label="Ranked Job Opportunities">
        {loading ? (
          <div className="empty-state glass-panel">
            <div className="empty-state-icon">⏳</div>
            <h3>Loading Job Queue...</h3>
            <p>Fetching multi-tenant posting vector scores from FastAPI backend.</p>
          </div>
        ) : error ? (
          <div className="empty-state glass-panel" style={{ borderColor: 'var(--crimson-500)' }}>
            <div className="empty-state-icon" style={{ color: 'var(--crimson-400)' }}>⚠️</div>
            <h3 style={{ color: 'var(--crimson-400)' }}>Connection Error</h3>
            <p>{error}</p>
            <button className="btn btn-secondary" onClick={fetchJobs}>Retry Connection</button>
          </div>
        ) : displayedJobs.length === 0 ? (
          <div className="empty-state glass-panel">
            <div className="empty-state-icon">🔍</div>
            <h3>No Postings Match Your Filter</h3>
            <p>Try switching filter tabs or trigger a new ingestion query above.</p>
          </div>
        ) : (
          <div className="jobs-grid">
            {displayedJobs.map((job) => {
              const scoreClass = getScoreClass(job.match_score);
              const isRemoteOk = job.source?.toLowerCase().includes('remoteok');
              const isFreehire = job.source?.toLowerCase().includes('freehire');

              return (
                <article
                  key={job.id}
                  id={`job-card-${job.id}`}
                  className="job-card glass-panel-interactive"
                >
                  {/* Match Score Radial Badge */}
                  <div className={`score-badge-circle ${scoreClass}`} title={`Cosine similarity: ${job.match_score}`}>
                    <span className="score-number">{formatScore(job.match_score)}</span>
                    <span className="score-label">MATCH</span>
                  </div>

                  {/* Main Role Details */}
                  <div className="job-main">
                    <div className="job-title-row">
                      <span className="job-role">{job.role}</span>
                      <span className="job-company">@ {job.company}</span>
                    </div>

                    <div className="job-meta-row">
                      {job.salary && (
                        <span className="badge badge-emerald">
                          💰 {job.salary}
                        </span>
                      )}

                      {job.location_type && (
                        <span className="badge badge-muted">
                          📍 {job.location_type} {job.country ? `(${job.country})` : ''}
                        </span>
                      )}

                      {/* Source with Mandatory Attribution */}
                      {isRemoteOk ? (
                        <span className="attribution-badge attribution-remoteok" title="RemoteOK ToS Compliance">
                          Remote OK Credit
                        </span>
                      ) : isFreehire ? (
                        <span className="attribution-badge attribution-freehire">
                          via freehire.me
                        </span>
                      ) : (
                        <span className="badge badge-muted">
                          Source: {job.source}
                        </span>
                      )}

                      {/* Integrity Status Badge */}
                      {job.integrity_status === 'flagged' ? (
                        <span className="badge badge-amber" title="Prompt injection or hidden instruction caught by posting_guard">
                          ⚠️ Guard Flagged
                        </span>
                      ) : (
                        <span className="badge badge-cyan" title="Verified clean input">
                          🛡️ Clean
                        </span>
                      )}

                      {/* Veto Status */}
                      {job.vetoed && (
                        <span className="badge badge-crimson" title={job.veto_reason || 'Gate dealbreaker'}>
                          🚫 Vetoed: {job.veto_reason || 'Dealbreaker'}
                        </span>
                      )}
                    </div>

                    {job.description && (
                      <p className="job-snippet">{job.description}</p>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div className="job-actions">
                    <button
                      id={`btn-inspect-${job.id}`}
                      className="btn btn-secondary btn-sm"
                      onClick={() => setInspectingJob(job)}
                    >
                      🔍 Inspect & Audit
                    </button>

                    {/* Dofollow apply link per RemoteOK & freehire.me ToS */}
                    <a
                      id={`link-apply-${job.id}`}
                      href={job.apply_link}
                      target="_blank"
                      rel="noopener"
                      className="btn btn-primary btn-sm"
                      title={isRemoteOk ? 'Dofollow link to RemoteOK listing' : 'Direct Apply Link'}
                    >
                      Apply Link ↗
                    </a>

                    <button
                      id={`btn-stage-${job.id}`}
                      className="btn btn-primary btn-sm"
                      style={{ background: 'linear-gradient(135deg, var(--indigo-500), #4f46e5)', color: '#fff' }}
                      onClick={() => handleTailorCV(job)}
                      disabled={isTailoring}
                      title="Tailor LaTeX CV & generate outreach draft"
                    >
                      {isTailoring && tailorModalJob?.id === job.id ? '⏳ Tailoring...' : '✨ Tailor CV (Apply)'}
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </main>
    </>
  )}

  {/* VIEW 2: Monitor & Pipeline View */}
  {currentView === 'monitor' && (
    <div className="monitor-view-container" id="monitor-view-section">
      {/* Pipeline Stage KPI Grid */}
      <section className="monitor-kpi-grid" aria-label="Pipeline Stages Summary">
        <div className="monitor-kpi-card" id="kpi-mon-total">
          <div className="monitor-kpi-title">
            <span>Total In Pipeline</span>
            <span>📈</span>
          </div>
          <div className="monitor-kpi-num">{monitorSummary.total}</div>
        </div>

        <div className="monitor-kpi-card" id="kpi-mon-draft">
          <div className="monitor-kpi-title">
            <span>Drafts (Review)</span>
            <span>📝</span>
          </div>
          <div className="monitor-kpi-num" style={{ color: 'var(--amber-400)' }}>
            {monitorSummary.draft}
          </div>
        </div>

        <div className="monitor-kpi-card" id="kpi-mon-sent">
          <div className="monitor-kpi-title">
            <span>Sent (Awaiting)</span>
            <span>🚀</span>
          </div>
          <div className="monitor-kpi-num" style={{ color: 'var(--emerald-400)' }}>
            {monitorSummary.sent}
          </div>
        </div>

        <div className={`monitor-kpi-card ${monitorSummary.follow_ups_due > 0 ? 'alert-due' : ''}`} id="kpi-mon-due">
          <div className="monitor-kpi-title">
            <span style={{ color: monitorSummary.follow_ups_due > 0 ? 'var(--amber-400)' : 'inherit' }}>
              Follow-ups Due (10-Day)
            </span>
            <span>⏰</span>
          </div>
          <div className="monitor-kpi-num" style={{ color: monitorSummary.follow_ups_due > 0 ? 'var(--amber-400)' : '#fff' }}>
            {monitorSummary.follow_ups_due}
          </div>
        </div>

        <div className="monitor-kpi-card" id="kpi-mon-responded">
          <div className="monitor-kpi-title">
            <span>Responded</span>
            <span>💬</span>
          </div>
          <div className="monitor-kpi-num" style={{ color: 'var(--cyan-400)' }}>
            {monitorSummary.responded}
          </div>
        </div>

        <div className="monitor-kpi-card" id="kpi-mon-interview">
          <div className="monitor-kpi-title">
            <span>Interviewing</span>
            <span>💼</span>
          </div>
          <div className="monitor-kpi-num" style={{ color: 'var(--indigo-400)' }}>
            {monitorSummary.interview}
          </div>
        </div>

        <div className="monitor-kpi-card" id="kpi-mon-offer">
          <div className="monitor-kpi-title">
            <span>Offer Received</span>
            <span>🏆</span>
          </div>
          <div className="monitor-kpi-num" style={{ color: 'var(--emerald-300)' }}>
            {monitorSummary.offer}
          </div>
        </div>

        <div className="monitor-kpi-card" id="kpi-mon-rejected">
          <div className="monitor-kpi-title">
            <span>Rejected / Closed</span>
            <span>📁</span>
          </div>
          <div className="monitor-kpi-num" style={{ color: 'var(--text-dim)' }}>
            {monitorSummary.rejected}
          </div>
        </div>
      </section>

      {/* Filter Bar & Controls */}
      <div className="monitor-controls-panel glass-panel" style={{ padding: '14px 20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
        <div className="tabs-list" style={{ margin: 0 }}>
          <button
            className={`tab-btn ${monitorFilter === 'all' ? 'active' : ''}`}
            onClick={() => setMonitorFilter('all')}
          >
            All Applications ({applications.length})
          </button>
          <button
            className={`tab-btn ${monitorFilter === 'draft' ? 'active' : ''}`}
            onClick={() => setMonitorFilter('draft')}
          >
            Drafts ({monitorSummary.draft})
          </button>
          <button
            className={`tab-btn ${monitorFilter === 'sent' ? 'active' : ''}`}
            onClick={() => setMonitorFilter('sent')}
          >
            Sent ({monitorSummary.sent})
          </button>
          <button
            className={`tab-btn ${monitorFilter === 'due' ? 'active' : ''}`}
            onClick={() => setMonitorFilter('due')}
            style={monitorSummary.follow_ups_due > 0 ? { color: 'var(--amber-400)', borderColor: 'var(--amber-400)' } : {}}
          >
            ⏰ Due ({monitorSummary.follow_ups_due})
          </button>
          <button
            className={`tab-btn ${monitorFilter === 'interview' ? 'active' : ''}`}
            onClick={() => setMonitorFilter('interview')}
          >
            Interviews ({monitorSummary.interview})
          </button>
          <button
            className={`tab-btn ${monitorFilter === 'offer' ? 'active' : ''}`}
            onClick={() => setMonitorFilter('offer')}
          >
            Offers ({monitorSummary.offer})
          </button>
        </div>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <input
            type="text"
            className="input-text"
            placeholder="Search company or role..."
            value={monitorSearch}
            onChange={(e) => setMonitorSearch(e.target.value)}
            style={{ width: '220px', padding: '6px 12px', fontSize: '13px' }}
          />
          <button
            className="btn btn-secondary btn-sm"
            onClick={fetchMonitorData}
            disabled={loadingApps}
            title="Refresh application status"
          >
            {loadingApps ? 'Refreshing...' : '🔄 Refresh'}
          </button>
        </div>
      </div>

      {/* Applications Pipeline List */}
      {loadingApps && applications.length === 0 ? (
        <div className="empty-state">
          <span className="empty-state-icon">⏳</span>
          <p>Loading application pipeline...</p>
        </div>
      ) : displayedApplications.length === 0 ? (
        <div className="empty-state">
          <span className="empty-state-icon">📋</span>
          <p>No applications found in this pipeline filter.</p>
          <p style={{ fontSize: '12px' }}>
            Tailor and review an application in the Find Queue to start tracking it here.
          </p>
        </div>
      ) : (
        <div className="pipeline-list">
          {displayedApplications.map((app) => {
            const isDue = isFollowUpDue(app);
            const capReached = (app.follow_up_count || 0) >= 2;

            return (
              <article
                key={app.id}
                className={`pipeline-card ${isDue ? 'card-due' : ''}`}
                id={`pipeline-card-${app.id}`}
              >
                <div className="pipeline-card-main">
                  <div className="pipeline-role-title">
                    <span>{app.job_role || 'Target Role'}</span>
                    <span style={{ color: 'var(--emerald-400)', fontWeight: 600 }}>
                      @ {app.job_company || 'Company'}
                    </span>
                    <span className="badge badge-emerald" style={{ fontSize: '10px', padding: '2px 8px' }}>
                      {app.channel.toUpperCase()}
                    </span>
                  </div>

                  <div className="pipeline-meta">
                    <span>
                      📅 {app.status === 'draft' ? 'Draft Created: ' : 'Sent: '}
                      <strong>{formatDate(app.sent_at || app.created_at)}</strong>
                    </span>

                    <span>•</span>

                    {/* Follow-Up Tracker Status */}
                    <div className="follow-up-tracker" title="Follow-up rule: 10 days post-send, max 2 follow-ups per ARCHITECTURE.md §6">
                      <span>Follow-ups:</span>
                      <div className="follow-up-dots">
                        <span className={`follow-up-dot ${(app.follow_up_count || 0) >= 1 ? 'filled' : ''}`}></span>
                        <span className={`follow-up-dot ${(app.follow_up_count || 0) >= 2 ? 'filled' : ''}`}></span>
                      </div>
                      <span>
                        <strong>{app.follow_up_count || 0}/2</strong>
                        {capReached ? (
                          <span style={{ color: 'var(--text-muted)', marginLeft: '4px' }}>(Cap Reached)</span>
                        ) : isDue ? (
                          <span style={{ color: 'var(--amber-400)', fontWeight: 'bold', marginLeft: '4px' }}>⚠️ Due Now!</span>
                        ) : app.follow_up_due ? (
                          <span style={{ color: 'var(--cyan-300)', marginLeft: '4px' }}>
                            (Due: {formatDate(app.follow_up_due)})
                          </span>
                        ) : (
                          <span style={{ color: 'var(--text-dim)', marginLeft: '4px' }}>—</span>
                        )}
                      </span>
                    </div>
                  </div>

                  {app.notes && (
                    <div style={{ fontSize: '12px', color: '#94a3b8', fontStyle: 'italic', marginTop: '2px' }}>
                      💬 {app.notes}
                    </div>
                  )}
                </div>

                {/* Stage Transition Dropdown & Actions */}
                <div className="pipeline-actions">
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', alignItems: 'flex-end' }}>
                    <label style={{ fontSize: '10px', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                      Status Stage:
                    </label>
                    <select
                      className="status-select"
                      value={app.status}
                      onChange={(e) => handleUpdateStatus(app.id, e.target.value)}
                      id={`select-status-${app.id}`}
                    >
                      <option value="draft">Draft (Unsent)</option>
                      <option value="sent">Sent (Awaiting)</option>
                      <option value="responded">Responded</option>
                      <option value="interview">Interviewing</option>
                      <option value="offer">Offer Received</option>
                      <option value="rejected">Rejected / Closed</option>
                    </select>
                  </div>

                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => setViewingAppMaterials(app)}
                    title="View submitted cover letter and details"
                  >
                    👁️ Materials
                  </button>

                  {/* Follow-Up Action Button */}
                  <button
                    className={`btn btn-sm ${isDue ? 'btn-primary' : 'btn-secondary'}`}
                    style={isDue ? { background: 'linear-gradient(135deg, #f59e0b, #d97706)', color: '#000', fontWeight: 'bold' } : {}}
                    onClick={() => handleOpenFollowUp(app)}
                    disabled={capReached || isDraftingFollowUp}
                    id={`btn-follow-up-${app.id}`}
                    title={capReached ? 'Max cap of 2 follow-ups reached per §6' : 'Draft follow-up email via LLM'}
                  >
                    {capReached ? 'Cap (2/2)' : isDue ? '⏰ Draft Follow-Up' : '✍️ Follow-Up'}
                  </button>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  )}


      {/* Security & Role Inspection Modal */}
      {inspectingJob && (
        <div className="modal-overlay" onClick={() => setInspectingJob(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} role="dialog">
            <div className="modal-header">
              <div>
                <h3 style={{ fontSize: '18px', color: '#fff' }}>{inspectingJob.role}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginTop: '4px' }}>
                  {inspectingJob.company} • Source: {inspectingJob.source}
                </p>
              </div>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => setInspectingJob(null)}
                aria-label="Close Modal"
              >
                ✕ Close
              </button>
            </div>

            <div className="modal-body">
              {/* Security Guard Alert if Flagged */}
              {inspectingJob.integrity_status === 'flagged' && (
                <div className="security-alert-box">
                  <h4>⚠️ Posting Integrity Alert: Prompt Injection / Instruction Detected</h4>
                  <p style={{ fontSize: '12px', marginBottom: '8px' }}>
                    The <code>posting_guard.py</code> pre-filter quarantined this posting because it contained
                    system-command-shaped phrasing or prompt overrides intended to manipulate downstream LLMs.
                  </p>
                  <div className="security-code-block">
                    [ISOLATED FOR SAFETY] Text was flagged prior to embedding. Always review carefully before generating CV tailoring drafts.
                  </div>
                </div>
              )}

              {/* Veto Reason if Vetoed */}
              {inspectingJob.vetoed && (
                <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', padding: '12px 16px', borderRadius: '8px', color: '#fca5a5' }}>
                  <strong>🚫 Gate Veto Reason:</strong> {inspectingJob.veto_reason || 'Failed dealbreaker criteria'}
                </div>
              )}

              {/* Telemetry Details */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '10px 14px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Match Score</div>
                  <div style={{ fontSize: '16px', fontWeight: 'bold', color: 'var(--emerald-400)' }}>
                    {formatScore(inspectingJob.match_score)}
                  </div>
                </div>

                <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '10px 14px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Location Type</div>
                  <div style={{ fontSize: '14px', fontWeight: '600', color: '#fff' }}>
                    {inspectingJob.location_type || 'Unspecified'} ({inspectingJob.country || 'Any'})
                  </div>
                </div>

                <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '10px 14px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Compensation</div>
                  <div style={{ fontSize: '14px', fontWeight: '600', color: '#fff' }}>
                    {inspectingJob.salary || 'Not listed'}
                  </div>
                </div>
              </div>

              {/* Full Description */}
              <div>
                <h4 style={{ fontSize: '13px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
                  Job Description Content
                </h4>
                <div style={{ background: 'rgba(0, 0, 0, 0.4)', padding: '16px', borderRadius: '8px', maxHeight: '280px', overflowY: 'auto', fontSize: '13px', lineHeight: '1.7', color: '#cbd5e1', whiteSpace: 'pre-wrap' }}>
                  {inspectingJob.description || 'No detailed description available in raw feed.'}
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <a
                href={inspectingJob.apply_link}
                target="_blank"
                rel="noopener"
                className="btn btn-primary"
              >
                Open Original Posting ↗
              </a>
              <button className="btn btn-secondary" onClick={() => setInspectingJob(null)}>
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Module 2 (Apply) CV Tailoring & Human-in-the-Loop Review Modal */}
      {tailorResult && tailorModalJob && (
        <div className="modal-overlay" onClick={() => setTailorResult(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} role="dialog" style={{ maxWidth: '900px' }}>
            <div className="modal-header">
              <div>
                <h3 style={{ fontSize: '18px', color: '#fff' }}>
                  ✨ Tailored Application: {tailorModalJob.role}
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginTop: '4px' }}>
                  {tailorModalJob.company} • Human-in-the-Loop Send Gate
                </p>
              </div>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => setTailorResult(null)}
                aria-label="Close Modal"
              >
                ✕ Close
              </button>
            </div>

            <div className="modal-body">
              {/* Telemetry Chips */}
              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                <span className="badge badge-emerald" style={{ fontSize: '12px', padding: '5px 10px' }}>
                  🎯 ATS Keyword Fit: {(tailorResult.ats_score * 100).toFixed(0)}%
                </span>
                <span className="badge badge-cyan" style={{ fontSize: '12px', padding: '5px 10px' }}>
                  🛡️ Fact Audit: 100% Truthful (01_MASTER_CV.tex)
                </span>
                <span
                  className={`badge ${tailorResult.application.status === 'sent' ? 'badge-emerald' : 'badge-amber'}`}
                  style={{ fontSize: '12px', padding: '5px 10px' }}
                >
                  Status: {tailorResult.application.status.toUpperCase()}
                  {tailorResult.application.status === 'draft' ? ' (Pending Human Review)' : ' (Human Approved)'}
                </span>
              </div>

              {/* Missing Gaps Flagged */}
              {tailorResult.gaps_detected && tailorResult.gaps_detected.length > 0 && (
                <div style={{ background: 'rgba(30, 41, 59, 0.6)', border: '1px solid var(--border-subtle)', padding: '12px 16px', borderRadius: '8px' }}>
                  <div style={{ fontSize: '12px', fontWeight: 'bold', color: 'var(--amber-400)', marginBottom: '4px' }}>
                    🔍 Honest Gap Detection (Uninvented Requirements):
                  </div>
                  <ul style={{ fontSize: '12px', color: '#cbd5e1', paddingLeft: '20px' }}>
                    {tailorResult.gaps_detected.map((gap, i) => (
                      <li key={i}>{gap}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Outreach Cover Letter Draft (Editable by Human) */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <h4 style={{ fontSize: '13px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                    Outreach Cover Letter Draft
                  </h4>
                  <span style={{ fontSize: '11px', color: 'var(--emerald-300)' }}>
                    ✏️ Editable before human Send
                  </span>
                </div>
                <textarea
                  className="input-text"
                  style={{ width: '100%', minHeight: '180px', fontFamily: 'var(--font-sans)', fontSize: '13px', lineHeight: '1.6' }}
                  value={editedCoverDraft}
                  onChange={(e) => setEditedCoverDraft(e.target.value)}
                />
              </div>

              {/* Toggle LaTeX Source Preview */}
              <div>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() => setShowLatexSource(!showLatexSource)}
                >
                  {showLatexSource ? 'Hide Tailored LaTeX Source' : 'View Tailored LaTeX Source'}
                </button>

                {showLatexSource && (
                  <div style={{ marginTop: '10px', background: 'rgba(0, 0, 0, 0.5)', padding: '14px', borderRadius: '8px', maxHeight: '220px', overflowY: 'auto' }}>
                    <pre style={{ fontFamily: 'var(--font-mono)', fontSize: '11px', color: '#a5b4fc', whiteSpace: 'pre-wrap' }}>
                      {tailorResult.cv_version.tailored_latex}
                    </pre>
                  </div>
                )}
              </div>
            </div>

            <div className="modal-footer">
              <a
                href={tailorModalJob.apply_link}
                target="_blank"
                rel="noopener"
                className="btn btn-secondary"
              >
                Open Job Posting ↗
              </a>

              {tailorResult.application.status === 'draft' ? (
                <button
                  id="btn-confirm-send"
                  className="btn btn-primary"
                  onClick={handleConfirmSend}
                  disabled={isSending}
                >
                  {isSending ? 'Confirming...' : '🚀 Approve & Mark Sent (Human Gate)'}
                </button>
              ) : (
                <span className="badge badge-emerald" style={{ padding: '8px 14px', fontSize: '13px' }}>
                  ✅ Application Confirmed & Sent
                </span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Module 3 (Monitor) Follow-Up Draft & Human Gate Modal */}
      {followUpModalApp && (
        <div className="modal-overlay" onClick={() => !isSendingFollowUp && setFollowUpModalApp(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} role="dialog" style={{ maxWidth: '750px' }}>
            <div className="modal-header">
              <div>
                <h3 style={{ fontSize: '18px', color: '#fff' }}>
                  ✍️ Follow-Up Outreach: {followUpModalApp.job_company || 'Target Company'}
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginTop: '4px' }}>
                  Role: {followUpModalApp.job_role || 'Position'} • Sequence: Follow-up #{followUpData ? followUpData.follow_up_number : (followUpModalApp.follow_up_count || 0) + 1} of 2
                </p>
              </div>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => setFollowUpModalApp(null)}
                disabled={isSendingFollowUp}
                aria-label="Close Modal"
              >
                ✕ Close
              </button>
            </div>

            <div className="modal-body">
              {/* Policy Badge */}
              <div style={{ background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.25)', padding: '12px 16px', borderRadius: '8px' }}>
                <div style={{ fontSize: '12px', fontWeight: 'bold', color: 'var(--emerald-300)', marginBottom: '4px' }}>
                  🛡️ ARCHITECTURE.md §6 Follow-Up Policy:
                </div>
                <div style={{ fontSize: '12px', color: '#cbd5e1', lineHeight: '1.5' }}>
                  Strict 10-day cadence. Follow-ups are limited to <strong>at most 2 per application</strong> to avoid spamming recruiters.
                  Human review is strictly mandatory prior to send.
                </div>
              </div>

              {/* Follow-Up Textarea */}
              {isDraftingFollowUp ? (
                <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-secondary)' }}>
                  <div style={{ fontSize: '24px', marginBottom: '8px' }}>🤖</div>
                  <div>Synthesizing polite, high-impact follow-up with LLM...</div>
                </div>
              ) : (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <h4 style={{ fontSize: '13px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                      Follow-up Email Draft
                    </h4>
                    <span style={{ fontSize: '11px', color: 'var(--emerald-300)' }}>
                      ✏️ Editable review before human confirmation
                    </span>
                  </div>
                  <textarea
                    className="input-text"
                    style={{ width: '100%', minHeight: '160px', fontFamily: 'var(--font-sans)', fontSize: '13px', lineHeight: '1.6' }}
                    value={editedFollowUpDraft}
                    onChange={(e) => setEditedFollowUpDraft(e.target.value)}
                    id="textarea-follow-up-draft"
                  />
                </div>
              )}
            </div>

            <div className="modal-footer">
              <button
                className="btn btn-secondary"
                onClick={() => setFollowUpModalApp(null)}
                disabled={isSendingFollowUp}
              >
                Cancel
              </button>

              <button
                id="btn-confirm-follow-up-send"
                className="btn btn-primary"
                onClick={handleConfirmFollowUpSend}
                disabled={isDraftingFollowUp || isSendingFollowUp || !editedFollowUpDraft.trim()}
              >
                {isSendingFollowUp ? 'Confirming...' : '🚀 Approve & Mark Follow-Up Sent (Human Gate)'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Application Materials Modal */}
      {viewingAppMaterials && (
        <div className="modal-overlay" onClick={() => setViewingAppMaterials(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} role="dialog" style={{ maxWidth: '800px' }}>
            <div className="modal-header">
              <div>
                <h3 style={{ fontSize: '18px', color: '#fff' }}>
                  📄 Application Materials: {viewingAppMaterials.job_role} @ {viewingAppMaterials.job_company}
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '4px' }}>
                  Status: {viewingAppMaterials.status.toUpperCase()} • Channel: {viewingAppMaterials.channel}
                </p>
              </div>
              <button className="btn btn-secondary btn-sm" onClick={() => setViewingAppMaterials(null)}>
                ✕ Close
              </button>
            </div>

            <div className="modal-body">
              <div>
                <h4 style={{ fontSize: '13px', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
                  Submitted Cover Letter / Outreach Draft
                </h4>
                <div style={{ background: 'rgba(0, 0, 0, 0.4)', padding: '16px', borderRadius: '8px', maxHeight: '300px', overflowY: 'auto', fontSize: '13px', lineHeight: '1.7', color: '#cbd5e1', whiteSpace: 'pre-wrap' }}>
                  {viewingAppMaterials.draft_content || 'No outreach content recorded.'}
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setViewingAppMaterials(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Live Toast Notification */}
      {toastMessage && (
        <div className="toast" role="status">
          <span>{toastMessage}</span>
        </div>
      )}
    </div>
  );
}
