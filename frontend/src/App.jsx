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

  // Modal Inspection
  const [inspectingJob, setInspectingJob] = useState(null);

  // Toast Helper
  const showToast = (msg, duration = 4000) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), duration);
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

  return (
    <div className="app-container">
      {/* Header Area */}
      <header className="app-header">
        <div className="brand-wrapper">
          <div className="brand-icon">⚡</div>
          <div className="brand-text">
            <h1 id="app-title">AGY Job Application Agent SaaS</h1>
            <div className="brand-sub">
              <span>Autonomous Search & Match Engine</span>
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
                      className="btn btn-secondary btn-sm"
                      style={{ opacity: 0.8 }}
                      onClick={() => showToast(`Module 2 (Apply): Tailoring pipeline staged for "${job.role} at ${job.company}".`)}
                      title="Stage for LaTeX CV tailoring & outreach generation"
                    >
                      Tailor CV (Module 2)
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </main>

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

      {/* Live Toast Notification */}
      {toastMessage && (
        <div className="toast" role="status">
          <span>{toastMessage}</span>
        </div>
      )}
    </div>
  );
}
