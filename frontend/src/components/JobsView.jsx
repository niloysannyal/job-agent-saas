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

export default function JobsView({
  jobs = [],
  loading = false,
  onIngest,
  isIngesting = false,
  onInspectJob,
  onSelectJobForStudio,
  targetDesignations = [],
}) {
  // Ingest Controls
  const [ingestQuery, setIngestQuery] = useState('AI Engineer');
  const [ingestWhere, setIngestWhere] = useState('Remote');
  const [ingestSource, setIngestSource] = useState('all');
  const [ingestLimit, setIngestLimit] = useState(10);

  // Filters & Search
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDesignation, setSelectedDesignation] = useState('all');
  const [selectedSource, setSelectedSource] = useState('all');
  const [scoreFilter, setScoreFilter] = useState('all'); // all | high | moderate
  const [guardFilter, setGuardFilter] = useState('all'); // all | clean | flagged
  const [sortBy, setSortBy] = useState('score'); // score | date | company

  // Filtered & Sorted Jobs
  const filteredJobs = useMemo(() => {
    return jobs.filter((job) => {
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
        if (job.posting_integrity_verdict === 'FLAGGED') return false;
      } else if (guardFilter === 'flagged') {
        if (job.posting_integrity_verdict !== 'FLAGGED') return false;
      }

      return true;
    }).sort((a, b) => {
      if (sortBy === 'score') {
        return (b.match_score ?? 0) - (a.match_score ?? 0);
      }
      if (sortBy === 'company') {
        return (a.company || '').localeCompare(b.company || '');
      }
      return new Date(b.created_at || 0) - new Date(a.created_at || 0);
    });
  }, [jobs, searchQuery, selectedDesignation, selectedSource, scoreFilter, guardFilter, sortBy]);

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
                Fetches raw postings via official APIs (Remotive, RemoteOK, Adzuna, Greenhouse, Lever, Freehire) and runs Posting Guard + Vector Scoring.
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
              placeholder="e.g. AI Engineer, LLM, MLOps"
            />
          </div>

          <div className="input-group">
            <label>Location / Mode</label>
            <input
              type="text"
              value={ingestWhere}
              onChange={(e) => setIngestWhere(e.target.value)}
              placeholder="Remote, EU, Dhaka..."
            />
          </div>

          <div className="input-group">
            <label>Source Feed</label>
            <select
              value={ingestSource}
              onChange={(e) => setIngestSource(e.target.value)}
            >
              <option value="all">All Available Sources</option>
              <option value="linkedin">LinkedIn</option>
              <option value="remotive">Remotive</option>
              <option value="remoteok">RemoteOK</option>
              <option value="adzuna">Adzuna</option>
              <option value="freehire">Freehire.me</option>
            </select>
          </div>

          <div className="input-group limit-input">
            <label>Limit</label>
            <input
              type="number"
              min="1"
              max="50"
              value={ingestLimit}
              onChange={(e) => setIngestLimit(parseInt(e.target.value) || 10)}
            />
          </div>

          <div className="input-group submit-group">
            <label>&nbsp;</label>
            <button
              className="action-btn-primary"
              disabled={isIngesting}
              onClick={() =>
                onIngest({
                  query: ingestQuery,
                  location: ingestWhere,
                  source: ingestSource === 'all' ? undefined : ingestSource,
                  limit: ingestLimit,
                })
              }
            >
              {isIngesting ? (
                <>
                  <RefreshCw className="btn-icon icon-spin" />
                  <span>Ingesting Feeds...</span>
                </>
              ) : (
                <>
                  <Sparkles className="btn-icon" />
                  <span>Ingest Opportunities</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Filter & Search Toolbar */}
      <div className="jobs-filter-toolbar panel-card">
        <div className="search-box">
          <Search className="search-icon" />
          <input
            type="text"
            placeholder="Search by role, company name, or technology..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <button className="clear-search-btn" onClick={() => setSearchQuery('')}>
              ×
            </button>
          )}
        </div>

        <div className="filters-row">
          <div className="filter-item">
            <label>Role:</label>
            <select
              value={selectedDesignation}
              onChange={(e) => setSelectedDesignation(e.target.value)}
            >
              <option value="all">All Designations</option>
              {targetDesignations.map((d) => (
                <option key={d.id || d.title} value={d.title}>
                  {d.title}
                </option>
              ))}
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
            <label>Integrity Guard:</label>
            <select
              value={guardFilter}
              onChange={(e) => setGuardFilter(e.target.value)}
            >
              <option value="all">All Postings</option>
              <option value="clean">Verified Clean</option>
              <option value="flagged">Flagged Only</option>
            </select>
          </div>

          <div className="filter-item">
            <label>Sort By:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="score">Match Score (High → Low)</option>
              <option value="date">Date Ingested (Newest)</option>
              <option value="company">Company (A → Z)</option>
            </select>
          </div>
        </div>

        <div className="results-counter">
          <span>Showing <strong>{filteredJobs.length}</strong> of {jobs.length} opportunities</span>
        </div>
      </div>

      {/* Opportunities Grid */}
      <div className="opportunities-grid">
        {filteredJobs.map((job) => {
          const rawScore = job.match_score != null ? (job.match_score <= 1.0 ? job.match_score * 100 : job.match_score) : null;
          const matchScore = rawScore != null ? Math.round(rawScore) : null;
          const isHighMatch = matchScore != null && matchScore >= 75;
          const isMidMatch = matchScore != null && matchScore >= 50 && matchScore < 75;
          const isClean = job.posting_integrity_verdict !== 'FLAGGED';
          const salaryInfo = formatSalary(job);

          return (
            <div key={job.id} className="opportunity-card panel-card">
              <div className="opp-header">
                <div className="opp-meta">
                  <div className="company-badge">
                    <Building2 className="icon-xs" />
                    <span>{job.company || 'Unknown Company'}</span>
                  </div>
                  <div className="location-badge">
                    <MapPin className="icon-xs" />
                    <span>{job.location || 'Remote'}</span>
                  </div>
                </div>

                <div className="score-pill-wrapper">
                  <div className={`score-badge ${isHighMatch ? 'score-high' : isMidMatch ? 'score-mid' : 'score-low'}`}>
                    <span className="score-value">{matchScore != null ? `${matchScore}%` : '--'}</span>
                    <span className="score-label">Fit</span>
                  </div>
                </div>
              </div>

              <h4 className="opp-title">{job.title || job.role}</h4>

              {/* Prominent Salary Badge */}
              <div className="opp-salary-row">
                <div className={`salary-badge ${salaryInfo.isDefined ? 'salary-defined' : 'salary-undisclosed'}`}>
                  <Banknote className="icon-xs" />
                  <span>{salaryInfo.text}</span>
                </div>
              </div>

              <p className="opp-description">
                {job.description?.replace(/<[^>]*>/g, '').slice(0, 150) || 'No job summary provided.'}...
              </p>

              {/* Attribution and Guard Status */}
              <div className="opp-tags-row">
                <span className="source-tag">
                  {job.source?.toLowerCase().includes('linkedin') && 'via LinkedIn'}
                  {job.source?.toLowerCase().includes('remoteok') && 'via RemoteOK'}
                  {job.source?.toLowerCase().includes('freehire') && 'via freehire.me'}
                  {!job.source?.toLowerCase().includes('linkedin') && !job.source?.toLowerCase().includes('remoteok') && !job.source?.toLowerCase().includes('freehire') && job.source}
                </span>

                {isClean ? (
                  <span className="guard-tag-clean">
                    <ShieldCheck className="icon-xxs" />
                    <span>Clean</span>
                  </span>
                ) : (
                  <span className="guard-tag-flagged" title="Potential prompt injection or hidden text flagged">
                    <AlertTriangle className="icon-xxs" />
                    <span>Flagged</span>
                  </span>
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
                  <span>Inspect</span>
                </button>

                <button
                  className="studio-btn"
                  onClick={() => onSelectJobForStudio(job)}
                >
                  <span>Apply in Studio</span>
                  <ArrowRight className="btn-icon-xs" />
                </button>
              </div>
            </div>
          );
        })}

        {filteredJobs.length === 0 && !loading && (
          <div className="empty-state-panel panel-card">
            <Sparkles className="empty-icon" />
            <h3>No matching opportunities found</h3>
            <p>Try adjusting your search query, fit threshold, or ingest a new feed above.</p>
          </div>
        )}
      </div>
    </div>
  );
}

