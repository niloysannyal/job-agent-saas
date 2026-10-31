import React, { useState, useMemo } from 'react';
import {
  Search,
  Filter,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  AlertTriangle,
  ExternalLink,
  Building2,
  MapPin,
  RefreshCw,
  Eye,
  SlidersHorizontal,
  Banknote,
  Wifi,
  Clock,
  Calendar,
  CheckCircle2,
  XCircle,
} from 'lucide-react';

export function formatSalary(job) {
  if (job.salary && job.salary.trim() && job.salary.trim().toLowerCase() !== 'null') {
    return { text: job.salary.trim(), isDefined: true };
  }
  if (job.salary_min != null && job.salary_max != null) {
    const curr = job.currency || '$';
    return {
      text: `${curr}${Number(job.salary_min).toLocaleString()} - ${curr}${Number(job.salary_max).toLocaleString()}`,
      isDefined: true,
    };
  }
  if (job.salary_min != null) {
    const curr = job.currency || '$';
    return { text: `From ${curr}${Number(job.salary_min).toLocaleString()}`, isDefined: true };
  }
  if (job.salary_max != null) {
    const curr = job.currency || '$';
    return { text: `Up to ${curr}${Number(job.salary_max).toLocaleString()}`, isDefined: true };
  }
  return { text: 'Negotiable / Undisclosed', isDefined: false };
}

export function formatPostingDate(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return null;
  const diffDays = Math.floor((new Date() - d) / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return 'Posted today';
  if (diffDays === 1) return 'Posted yesterday';
  if (diffDays < 30) return `Posted ${diffDays}d ago`;
  return `Posted ${d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}`;
}

export default function JobsView({
  jobs = [],
  loading = false,
  onIngest,
  isIngesting = false,
  onInspectJob,
  onSelectJobForStudio,
  targetDesignations = [],
  authHeaders = {},
  showToast,
}) {
  // Ingest Controls
  const [ingestQuery, setIngestQuery] = useState(
    targetDesignations[0]?.title || 'Backend Engineer'
  );
  const [ingestWhere, setIngestWhere] = useState('Remote');
  const [ingestSource, setIngestSource] = useState('all');
  const [ingestLimit, setIngestLimit] = useState(15);

  // Filters & Search
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDesignation, setSelectedDesignation] = useState('all');
  const [selectedSource, setSelectedSource] = useState('all');
  const [scoreFilter, setScoreFilter] = useState('all'); // all | high | moderate
  const [workplaceFilter, setWorkplaceFilter] = useState('all'); // all | remote | hybrid | onsite
  const [recencyFilter, setRecencyFilter] = useState('all'); // all | 1 | 7 | 14 | 30
  const [hideExpired, setHideExpired] = useState(true);
  const [guardFilter, setGuardFilter] = useState('all'); // all | clean | flagged
  const [sortBy, setSortBy] = useState('score'); // score | posted_at | date | company

  // Liveness check state tracking per job id
  const [checkingLiveness, setCheckingLiveness] = useState({});
  const [jobOverrides, setJobOverrides] = useState({});

  const handleCheckLiveness = async (job) => {
    try {
      setCheckingLiveness((prev) => ({ ...prev, [job.id]: true }));
      const res = await fetch(`/api/v1/jobs/${job.id}/check-liveness`, {
        method: 'POST',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const data = await res.json();
        setJobOverrides((prev) => ({
          ...prev,
          [job.id]: {
            is_active: data.is_active,
            integrity_status: data.integrity_status,
          },
        }));
        if (data.is_active) {
          showToast?.('Link verified active and accepting applications!');
        } else {
          showToast?.('Posting link appears dead or closed (HTTP error/expired).');
        }
      }
    } catch (err) {
      showToast?.('Could not verify link liveness.');
    } finally {
      setCheckingLiveness((prev) => ({ ...prev, [job.id]: false }));
    }
  };

  // Filtered & Sorted Jobs
  const filteredJobs = useMemo(() => {
    const now = new Date();

    return jobs.filter((rawJob) => {
      const override = jobOverrides[rawJob.id] || {};
      const job = { ...rawJob, ...override };

      // Hide dead links & expired deadlines
      if (hideExpired) {
        if (job.is_active === false) return false;
        if (job.integrity_status === 'dead_link') return false;
        if (job.deadline) {
          const dl = new Date(job.deadline);
          if (!isNaN(dl.getTime()) && dl < now) return false;
        }
      }

      // Workplace filter
      if (workplaceFilter !== 'all') {
        const mode = (job.location_type || '').toLowerCase();
        if (workplaceFilter === 'remote' && mode !== 'remote') return false;
        if (workplaceFilter === 'hybrid' && mode !== 'hybrid') return false;
        if (workplaceFilter === 'onsite' && mode !== 'onsite' && mode !== 'on-site') return false;
      }

      // Recency filter (days)
      if (recencyFilter !== 'all') {
        const days = parseInt(recencyFilter, 10);
        const postedDate = job.posted_at ? new Date(job.posted_at) : (job.created_at ? new Date(job.created_at) : null);
        if (postedDate && !isNaN(postedDate.getTime())) {
          const diffDays = (now - postedDate) / (1000 * 60 * 60 * 24);
          if (diffDays > days) return false;
        }
      }

      // Text search
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const jobRole = job.title || job.role || '';
        const matchesTitle = jobRole.toLowerCase().includes(q);
        const matchesCompany = job.company?.toLowerCase().includes(q);
        const matchesDesc = job.description?.toLowerCase().includes(q);
        if (!matchesTitle && !matchesCompany && !matchesDesc) return false;
      }

      // Designation filter
      if (selectedDesignation !== 'all') {
        const jobRole = job.title || job.role || '';
        const matchesDesig = jobRole.toLowerCase().includes(selectedDesignation.toLowerCase());
        if (!matchesDesig) return false;
      }

      // Source filter
      if (selectedSource !== 'all') {
        if (job.source?.toLowerCase() !== selectedSource.toLowerCase()) return false;
      }

      // Score filter
      if (scoreFilter === 'high') {
        if ((job.match_score ?? 0) < 80) return false;
      } else if (scoreFilter === 'moderate') {
        if ((job.match_score ?? 0) < 60) return false;
      }

      // Guard filter
      if (guardFilter === 'clean') {
        if (job.integrity_status === 'flagged' || job.posting_integrity_verdict === 'FLAGGED') return false;
      } else if (guardFilter === 'flagged') {
        if (job.integrity_status !== 'flagged' && job.posting_integrity_verdict !== 'FLAGGED') return false;
      }

      return true;
    }).sort((a, b) => {
      if (sortBy === 'score') {
        return (b.match_score ?? 0) - (a.match_score ?? 0);
      }
      if (sortBy === 'posted_at') {
        const dateA = new Date(a.posted_at || a.created_at || 0);
        const dateB = new Date(b.posted_at || b.created_at || 0);
        return dateB - dateA;
      }
      if (sortBy === 'company') {
        return (a.company || '').localeCompare(b.company || '');
      }
      return new Date(b.created_at || 0) - new Date(a.created_at || 0);
    });
  }, [jobs, searchQuery, selectedDesignation, selectedSource, scoreFilter, workplaceFilter, recencyFilter, hideExpired, guardFilter, sortBy, jobOverrides]);

  const uniqueSources = useMemo(() => {
    const set = new Set();
    jobs.forEach((j) => {
      if (j.source) set.add(j.source);
    });
    return Array.from(set);
  }, [jobs]);

  return (
    <div className="section-container jobs-view">
      {/* Top Feed Ingestion Console */}
      <div className="panel-card ingestion-console">
        <div className="console-header">
          <div className="console-title-group">
            <Sparkles className="console-icon" />
            <div>
              <h3>Autonomous Job Sourcing & Vector Ingestion</h3>
              <p className="console-subtext">
                Ingest real postings across all technical & private company roles (Greenhouse, Lever, Adzuna, Remotive, RemoteOK, Freehire).
              </p>
            </div>
          </div>
        </div>

        <div className="ingestion-inputs-grid">
          <div className="input-group">
            <label>Query</label>
            <input
              type="text"
              value={ingestQuery}
              onChange={(e) => setIngestQuery(e.target.value)}
              placeholder="e.g. Backend Engineer, Systems Architect, Product Manager"
            />
          </div>

          <div className="input-group">
            <label>Location / Mode</label>
            <input
              type="text"
              value={ingestWhere}
              onChange={(e) => setIngestWhere(e.target.value)}
              placeholder="Remote, EU, London, San Francisco..."
            />
          </div>

          <div className="input-group">
            <label>Source Feed</label>
            <select
              value={ingestSource}
              onChange={(e) => setIngestSource(e.target.value)}
            >
              <option value="all">All Connected Feeds</option>
              <option value="greenhouse">Greenhouse (Anthropic, Canonical, GitLab)</option>
              <option value="lever">Lever (Spotify, Netflix)</option>
              <option value="adzuna">Adzuna (19 Countries)</option>
              <option value="remotive">Remotive (Remote Tech)</option>
              <option value="remoteok">RemoteOK</option>
              <option value="freehire">freehire.me</option>
            </select>
          </div>

          <div className="input-group input-group-limit">
            <label>Fetch Limit</label>
            <select
              value={ingestLimit}
              onChange={(e) => setIngestLimit(Number(e.target.value))}
            >
              <option value={10}>10 jobs</option>
              <option value={20}>20 jobs</option>
              <option value={50}>50 jobs</option>
            </select>
          </div>

          <div className="input-group-action">
            <button
              className="action-btn-primary full-width"
              disabled={isIngesting || !ingestQuery.trim()}
              onClick={() => {
                if (onIngest) {
                  const sources = ingestSource === 'all' ? undefined : [ingestSource];
                  onIngest(ingestQuery.trim(), sources, ingestWhere);
                }
              }}
            >
              <RefreshCw className={`btn-icon ${isIngesting ? 'spin' : ''}`} />
              <span>{isIngesting ? 'Ingesting...' : 'Run Search'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* FILTER & CONTROL TOOLBAR */}
      <div className="panel-card toolbar-panel">
        {/* Workplace Mode Pills */}
        <div className="workplace-pills-row">
          <span className="pills-label">Workplace Mode:</span>
          <button
            className={`pill-btn ${workplaceFilter === 'all' ? 'active' : ''}`}
            onClick={() => setWorkplaceFilter('all')}
          >
            All Workplaces
          </button>
          <button
            className={`pill-btn ${workplaceFilter === 'remote' ? 'active' : ''}`}
            onClick={() => setWorkplaceFilter('remote')}
          >
            <Wifi size={14} /> Full Remote
          </button>
          <button
            className={`pill-btn ${workplaceFilter === 'hybrid' ? 'active' : ''}`}
            onClick={() => setWorkplaceFilter('hybrid')}
          >
            Hybrid
          </button>
          <button
            className={`pill-btn ${workplaceFilter === 'onsite' ? 'active' : ''}`}
            onClick={() => setWorkplaceFilter('onsite')}
          >
            On-site
          </button>
        </div>

        {/* Search & Advanced Filters */}
        <div className="filters-grid">
          <div className="search-box">
            <Search className="search-icon" />
            <input
              type="text"
              placeholder="Search title, company, skills..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="filter-item">
            <label>Recency:</label>
            <select
              value={recencyFilter}
              onChange={(e) => setRecencyFilter(e.target.value)}
            >
              <option value="all">Anytime</option>
              <option value="1">Past 24 Hours</option>
              <option value="7">Past 7 Days</option>
              <option value="14">Past 14 Days</option>
              <option value="30">Past 30 Days</option>
            </select>
          </div>

          <div className="filter-item">
            <label>Fit Score:</label>
            <select
              value={scoreFilter}
              onChange={(e) => setScoreFilter(e.target.value)}
            >
              <option value="all">All Scores</option>
              <option value="high">High Fit (&gt;80%)</option>
              <option value="moderate">Moderate Fit (&gt;60%)</option>
            </select>
          </div>

          <div className="filter-item">
            <label>Source:</label>
            <select
              value={selectedSource}
              onChange={(e) => setSelectedSource(e.target.value)}
            >
              <option value="all">All Sources</option>
              {uniqueSources.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-item">
            <label>Sort By:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="score">Match Score (High → Low)</option>
              <option value="posted_at">Posting Date (Newest)</option>
              <option value="date">Date Ingested (Newest)</option>
              <option value="company">Company (A → Z)</option>
            </select>
          </div>

          <div className="filter-item filter-toggle">
            <label className="checkbox-toggle">
              <input
                type="checkbox"
                checked={hideExpired}
                onChange={(e) => setHideExpired(e.target.checked)}
              />
              <span>Hide Expired / Dead Links</span>
            </label>
          </div>
        </div>

        <div className="results-counter">
          <span>Showing <strong>{filteredJobs.length}</strong> of {jobs.length} opportunities</span>
        </div>
      </div>

      {/* OPPORTUNITIES GRID */}
      <div className="opportunities-grid">
        {loading ? (
          <div className="loading-state">
            <RefreshCw className="spin" size={32} />
            <p>Scanning job radar...</p>
          </div>
        ) : filteredJobs.length === 0 ? (
          <div className="empty-panel-state">
            <Building2 size={40} className="dim-icon" />
            <h4>No jobs match your current filters</h4>
            <p>Try switching workplace mode to "All Workplaces" or clearing search terms.</p>
          </div>
        ) : (
          filteredJobs.map((rawJob) => {
            const override = jobOverrides[rawJob.id] || {};
            const job = { ...rawJob, ...override };

            const rawScore = job.match_score != null ? (job.match_score <= 1.0 ? job.match_score * 100 : job.match_score) : null;
            const matchScore = rawScore != null ? Math.round(rawScore) : null;
            const isHighMatch = matchScore != null && matchScore >= 75;
            const isMidMatch = matchScore != null && matchScore >= 50 && matchScore < 75;
            const isClean = job.integrity_status !== 'flagged' && job.posting_integrity_verdict !== 'FLAGGED';
            const isDeadLink = job.integrity_status === 'dead_link' || job.is_active === false;
            const salaryInfo = formatSalary(job);
            const postedDateFormatted = formatPostingDate(job.posted_at || job.created_at);

            // Workplace label and styling
            const locType = (job.location_type || 'onsite').toLowerCase();
            const workplaceBadgeClass = locType === 'remote' ? 'badge-remote' : locType === 'hybrid' ? 'badge-hybrid' : 'badge-onsite';
            const workplaceLabel = locType === 'remote' ? 'Remote' : locType === 'hybrid' ? 'Hybrid' : 'On-site';

            return (
              <div key={job.id} className={`opportunity-card panel-card ${isDeadLink ? 'card-dead-link' : ''}`}>
                <div className="opp-header">
                  <div className="opp-meta">
                    <div className="company-badge">
                      <Building2 className="icon-xs" />
                      <span>{job.company || 'Unknown Company'}</span>
                    </div>
                    {/* Prominent Workplace Badge */}
                    <span className={`workplace-badge ${workplaceBadgeClass}`}>
                      {locType === 'remote' && <Wifi size={12} />}
                      {workplaceLabel}
                    </span>
                  </div>

                  <div className="score-pill-wrapper">
                    <div className={`score-badge ${isHighMatch ? 'score-high' : isMidMatch ? 'score-mid' : 'score-low'}`}>
                      <span className="score-value">{matchScore != null ? `${matchScore}%` : '--'}</span>
                      <span className="score-label">Fit</span>
                    </div>
                  </div>
                </div>

                <h4 className="opp-title">{job.title || job.role}</h4>

                {/* Location & Dates Meta Row */}
                <div className="opp-location-date-row">
                  <div className="loc-text">
                    <MapPin size={13} />
                    <span>{job.city && job.country ? `${job.city}, ${job.country}` : (job.location || 'Remote')}</span>
                  </div>
                  {postedDateFormatted && (
                    <div className="date-text">
                      <Clock size={13} />
                      <span>{postedDateFormatted}</span>
                    </div>
                  )}
                  {job.deadline && (
                    <div className="deadline-text">
                      <Calendar size={13} />
                      <span>Due: {new Date(job.deadline).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</span>
                    </div>
                  )}
                </div>

                {/* Salary Badge */}
                <div className="opp-salary-row">
                  <div className={`salary-badge ${salaryInfo.isDefined ? 'salary-defined' : 'salary-undisclosed'}`}>
                    <Banknote className="icon-xs" />
                    <span>{salaryInfo.text}</span>
                  </div>
                </div>

                <p className="opp-description">
                  {job.description?.replace(/<[^>]*>/g, '').slice(0, 160) || 'No job summary provided.'}...
                </p>

                {/* Attribution and Guard Status */}
                <div className="opp-tags-row">
                  <span className="source-tag">via {job.source || 'Aggregator'}</span>

                  {isClean ? (
                    <span className="guard-tag-clean">
                      <ShieldCheck className="icon-xxs" />
                      <span>Verified Clean</span>
                    </span>
                  ) : (
                    <span className="guard-tag-flagged" title="Potential prompt injection or hidden text flagged">
                      <AlertTriangle className="icon-xxs" />
                      <span>Flagged</span>
                    </span>
                  )}

                  {isDeadLink ? (
                    <span className="guard-tag-dead">
                      <XCircle className="icon-xxs" />
                      <span>Link Inactive</span>
                    </span>
                  ) : (
                    <button
                      className="btn-liveness-check"
                      onClick={() => handleCheckLiveness(job)}
                      disabled={checkingLiveness[job.id]}
                      title="Test if application page is currently active"
                    >
                      {checkingLiveness[job.id] ? (
                        <RefreshCw size={11} className="spin" />
                      ) : (
                        <CheckCircle2 size={11} />
                      )}
                      <span>{checkingLiveness[job.id] ? 'Checking...' : 'Check Link'}</span>
                    </button>
                  )}
                </div>

                {/* Action Buttons */}
                <div className="opp-footer">
                  <button
                    className="inspect-btn"
                    onClick={() => onInspectJob(job)}
                    title="View full posting and match details"
                  >
                    <Eye className="btn-icon-xs" />
                    <span>Details</span>
                  </button>

                  <button
                    className="tailor-btn"
                    onClick={() => onSelectJobForStudio(job)}
                    disabled={isDeadLink}
                  >
                    <span>Tailor Application</span>
                    <ArrowRight className="btn-icon-xs" />
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
