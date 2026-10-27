import React from 'react';
import {
  TrendingUp,
  Target,
  Send,
  Clock,
  Award,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Compass,
} from 'lucide-react';

export default function DashboardView({
  stats = {},
  monitorSummary = {},
  profile = {},
  topJobs = [],
  onNavigate,
  onSelectJobForStudio,
}) {
  const totalIngested = stats.total || 0;
  const highMatchCount = stats.high || 0;
  const totalSent = monitorSummary.sent || 0;
  const followUpsDue = monitorSummary.follow_ups_due || 0;
  const interviewsCount = monitorSummary.interview || 0;
  const offersCount = monitorSummary.offer || 0;

  const conversionRate = totalSent > 0 
    ? Math.round(((interviewsCount + offersCount) / totalSent) * 100) 
    : 0;

  const designations = profile?.target_designations || [];

  return (
    <div className="section-container dashboard-view">
      {/* Top Banner */}
      <div className="dashboard-hero-banner">
        <div className="hero-text">
          <h2>
            Welcome back, <span className="highlight-text">{profile?.full_name || 'Niloy'}</span>
          </h2>
          <p className="hero-subtext">
            {profile?.one_liner || 'AI/ML Engineer building and deploying scalable AI-powered systems.'}
          </p>
        </div>
        <div className="hero-quick-actions">
          <button
            className="action-btn-primary"
            onClick={() => onNavigate('jobs')}
          >
            <Sparkles className="btn-icon" />
            <span>Ingest Job Opportunities</span>
          </button>
          <button
            className="action-btn-secondary"
            onClick={() => onNavigate('studio')}
          >
            <span>Open Application Studio</span>
            <ArrowRight className="btn-icon" />
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="kpi-cards-grid">
        <div className="kpi-card" onClick={() => onNavigate('jobs')}>
          <div className="kpi-header">
            <span className="kpi-title">Ingested Opportunities</span>
            <div className="kpi-icon-pill icon-blue">
              <Compass className="icon-sm" />
            </div>
          </div>
          <div className="kpi-body">
            <div className="kpi-number">{totalIngested}</div>
            <div className="kpi-trend positive">
              <span>Feeds: Remotive, RemoteOK, Adzuna</span>
            </div>
          </div>
        </div>

        <div className="kpi-card" onClick={() => onNavigate('jobs')}>
          <div className="kpi-header">
            <span className="kpi-title">High Semantic Fit (&gt;80%)</span>
            <div className="kpi-icon-pill icon-emerald">
              <Target className="icon-sm" />
            </div>
          </div>
          <div className="kpi-body">
            <div className="kpi-number">{highMatchCount}</div>
            <div className="kpi-trend positive">
              <span>Ready for Application Studio</span>
            </div>
          </div>
        </div>

        <div className="kpi-card" onClick={() => onNavigate('pipeline')}>
          <div className="kpi-header">
            <span className="kpi-title">Applications Sent</span>
            <div className="kpi-icon-pill icon-cyan">
              <Send className="icon-sm" />
            </div>
          </div>
          <div className="kpi-body">
            <div className="kpi-number">{totalSent}</div>
            <div className="kpi-trend neutral">
              <span>{monitorSummary.draft || 0} tailored drafts pending</span>
            </div>
          </div>
        </div>

        <div className={`kpi-card ${followUpsDue > 0 ? 'kpi-card-alert' : ''}`} onClick={() => onNavigate('pipeline')}>
          <div className="kpi-header">
            <span className="kpi-title">Follow-Ups Due</span>
            <div className="kpi-icon-pill icon-amber">
              <Clock className="icon-sm" />
            </div>
          </div>
          <div className="kpi-body">
            <div className="kpi-number">{followUpsDue}</div>
            <div className="kpi-trend warning">
              <span>{followUpsDue > 0 ? 'Action required in Pipeline' : 'All follow-ups up to date'}</span>
            </div>
          </div>
        </div>

        <div className="kpi-card" onClick={() => onNavigate('pipeline')}>
          <div className="kpi-header">
            <span className="kpi-title">Interview Conversion</span>
            <div className="kpi-icon-pill icon-purple">
              <Award className="icon-sm" />
            </div>
          </div>
          <div className="kpi-body">
            <div className="kpi-number">{conversionRate}%</div>
            <div className="kpi-trend positive">
              <span>{interviewsCount} Interviews • {offersCount} Offers</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Funnel & Target Roles */}
      <div className="dashboard-analytics-grid">
        {/* Pipeline Funnel */}
        <div className="panel-card funnel-panel">
          <div className="panel-header">
            <div className="panel-title-group">
              <TrendingUp className="panel-icon" />
              <h3>Application Lifecycle Funnel</h3>
            </div>
            <span className="panel-badge">Autonomous SaaS Loop</span>
          </div>

          <div className="funnel-container">
            <div className="funnel-stage">
              <div className="stage-meta">
                <span className="stage-name">1. Ingested & Scored</span>
                <span className="stage-count">{totalIngested}</span>
              </div>
              <div className="funnel-progress-bar">
                <div className="progress-fill fill-blue" style={{ width: '100%' }}></div>
              </div>
            </div>

            <div className="funnel-stage">
              <div className="stage-meta">
                <span className="stage-name">2. High Fit Opportunities</span>
                <span className="stage-count">{highMatchCount}</span>
              </div>
              <div className="funnel-progress-bar">
                <div
                  className="progress-fill fill-emerald"
                  style={{ width: `${totalIngested > 0 ? Math.round((highMatchCount / totalIngested) * 100) : 0}%` }}
                ></div>
              </div>
            </div>

            <div className="funnel-stage">
              <div className="stage-meta">
                <span className="stage-name">3. Tailored Drafts Created</span>
                <span className="stage-count">{monitorSummary.draft || 0}</span>
              </div>
              <div className="funnel-progress-bar">
                <div
                  className="progress-fill fill-amber"
                  style={{ width: `${totalIngested > 0 ? Math.min(100, Math.round(((monitorSummary.draft || 0) / Math.max(1, highMatchCount)) * 100)) : 0}%` }}
                ></div>
              </div>
            </div>

            <div className="funnel-stage">
              <div className="stage-meta">
                <span className="stage-name">4. Human Approved & Sent</span>
                <span className="stage-count">{totalSent}</span>
              </div>
              <div className="funnel-progress-bar">
                <div
                  className="progress-fill fill-cyan"
                  style={{ width: `${totalIngested > 0 ? Math.min(100, Math.round((totalSent / Math.max(1, highMatchCount)) * 100)) : 0}%` }}
                ></div>
              </div>
            </div>

            <div className="funnel-stage">
              <div className="stage-meta">
                <span className="stage-name">5. Interview & Stage Advancements</span>
                <span className="stage-count">{interviewsCount + offersCount}</span>
              </div>
              <div className="funnel-progress-bar">
                <div
                  className="progress-fill fill-purple"
                  style={{ width: `${totalSent > 0 ? Math.min(100, Math.round(((interviewsCount + offersCount) / totalSent) * 100)) : 0}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Target Roles & Identity */}
        <div className="panel-card identity-panel">
          <div className="panel-header">
            <div className="panel-title-group">
              <Target className="panel-icon" />
              <h3>Target Roles & Priorities</h3>
            </div>
            <button className="panel-link-btn" onClick={() => onNavigate('profile')}>
              Edit Roles
            </button>
          </div>

          <p className="panel-subtext">
            Active roles calibrated for semantic matching against job feeds.
          </p>

          <div className="target-roles-pill-cloud">
            {designations.length > 0 ? (
              designations.map((d) => (
                <div key={d.id || d.title} className="role-pill">
                  <span className="priority-badge">#{d.priority + 1}</span>
                  <span className="role-pill-title">{d.title}</span>
                </div>
              ))
            ) : (
              <p className="empty-subtext">No target designations configured yet.</p>
            )}
          </div>

          <div className="guard-reminder-card">
            <ShieldCheck className="reminder-icon" />
            <div>
              <strong>Human Gate Protection Active</strong>
              <p>Every application and follow-up strictly pauses at Draft until you approve.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Top High Fit Matches Preview */}
      <div className="panel-card top-matches-panel">
        <div className="panel-header">
          <div className="panel-title-group">
            <Sparkles className="panel-icon" />
            <h3>Top Recommended Opportunities</h3>
          </div>
          <button className="panel-link-btn" onClick={() => onNavigate('jobs')}>
            View All Jobs ({totalIngested})
          </button>
        </div>

        <div className="top-matches-grid">
          {topJobs.slice(0, 3).map((job) => (
            <div key={job.id} className="top-match-card">
              <div className="top-match-header">
                <div className="match-score-badge">
                  <span>{job.match_score != null ? Math.round(job.match_score <= 1.0 ? job.match_score * 100 : job.match_score) : '--'}%</span>
                </div>
                <div className="match-source-badge">
                  {job.source}
                </div>
              </div>
              <h4 className="top-match-title">{job.title || job.role}</h4>
              <p className="top-match-company">{job.company} • {job.location || 'Remote'}</p>
              <div className="top-match-footer">
                <button
                  className="studio-cta-btn"
                  onClick={() => onSelectJobForStudio(job)}
                >
                  <span>Apply in Studio</span>
                  <ArrowRight className="btn-icon-xs" />
                </button>
              </div>
            </div>
          ))}

          {topJobs.length === 0 && (
            <div className="empty-matches-placeholder">
              <p>No job opportunities ingested yet.</p>
              <button
                className="action-btn-primary"
                onClick={() => onNavigate('jobs')}
              >
                Ingest Opportunities Now
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

