import React, { useState, useMemo } from 'react';
import {
  Kanban,
  Send,
  Clock,
  Building2,
  Eye,
  Plus,
} from 'lucide-react';

export default function PipelineView({
  applications = [],
  loading = false,
  onUpdateStatus,
  onDraftFollowUp,
  onSendFollowUp,
  onViewMaterials,
  onNavigate,
  showToast,
}) {
  const [selectedColumnFilter, setSelectedColumnFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Kanban Stage Definitions
  const stages = [
    { id: 'draft', label: 'Drafted', color: 'stage-draft', icon: '📝' },
    { id: 'sent', label: 'Sent / Applied', color: 'stage-sent', icon: '🚀' },
    { id: 'follow_up_due', label: 'Follow-Up Due', color: 'stage-due', icon: '⏰' },
    { id: 'responded', label: 'Responded', color: 'stage-responded', icon: '💬' },
    { id: 'interview', label: 'Interviewing', color: 'stage-interview', icon: '🏆' },
    { id: 'offer', label: 'Offer Received', color: 'stage-offer', icon: '🎉' },
    { id: 'rejected', label: 'Archived / Rejected', color: 'stage-rejected', icon: '❌' },
  ];

  // Helper to determine whether follow-up is due
  const isFollowUpDue = (app) => {
    if (app.status !== 'sent' || !app.sent_at || app.follow_up_count >= 2) return false;
    if (!app.follow_up_due) return false;
    const due = new Date(app.follow_up_due);
    return due <= new Date();
  };

  // Group applications by stage
  const groupedApps = useMemo(() => {
    const map = {
      draft: [],
      sent: [],
      follow_up_due: [],
      responded: [],
      interview: [],
      offer: [],
      rejected: [],
    };

    applications.forEach((app) => {
      // Text search filter
      if (searchTerm.trim()) {
        const q = searchTerm.toLowerCase();
        const role = app.job?.title?.toLowerCase() || '';
        const comp = app.job?.company?.toLowerCase() || '';
        if (!role.includes(q) && !comp.includes(q)) return;
      }

      if (isFollowUpDue(app)) {
        map.follow_up_due.push(app);
      } else if (app.status === 'draft') {
        map.draft.push(app);
      } else if (app.status === 'sent') {
        map.sent.push(app);
      } else if (app.status === 'responded') {
        map.responded.push(app);
      } else if (app.status === 'interview' || app.status === 'interviewing') {
        map.interview.push(app);
      } else if (app.status === 'offer' || app.status === 'offered') {
        map.offer.push(app);
      } else if (app.status === 'rejected' || app.status === 'declined') {
        map.rejected.push(app);
      } else {
        map.sent.push(app);
      }
    });

    return map;
  }, [applications, searchTerm]);

  return (
    <div className="section-container pipeline-view">
      {/* Pipeline Header */}
      <div className="pipeline-header panel-card">
        <div className="pipeline-title-group">
          <Kanban className="pipeline-icon" />
          <div>
            <h3>Autonomous Application Pipeline & Lifecycle Tracker</h3>
            <p className="pipeline-subtext">
              Track multi-stage application progression, schedule 10-day follow-ups (strictly capped at 2), and manage candidate status.
            </p>
          </div>
        </div>

        <div className="pipeline-filter-controls">
          <input
            type="text"
            placeholder="Search company or role..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pipeline-search-input"
          />
          <button
            className="action-btn-primary"
            onClick={() => onNavigate('studio')}
          >
            <Plus className="btn-icon" />
            <span>New Application</span>
          </button>
        </div>
      </div>

      {/* Visual Kanban Columns Grid */}
      <div className="kanban-board-container">
        {stages.map((stage) => {
          const appsInStage = groupedApps[stage.id] || [];

          return (
            <div key={stage.id} className={`kanban-column ${stage.color}`}>
              <div className="column-header">
                <div className="column-title-left">
                  <span className="stage-emoji">{stage.icon}</span>
                  <span className="column-name">{stage.label}</span>
                </div>
                <span className="column-badge">{appsInStage.length}</span>
              </div>

              <div className="column-cards-scroll">
                {appsInStage.map((app) => {
                  const job = app.job || {};
                  const isDue = isFollowUpDue(app);

                  return (
                    <div key={app.id} className="kanban-card">
                      <div className="card-top-meta">
                        <span className="card-company">
                          <Building2 className="icon-xxs" />
                          <span>{job.company || 'Direct Opportunity'}</span>
                        </span>
                        <span className="card-channel-pill">{app.channel || 'Email'}</span>
                      </div>

                      <h5 className="card-title">{job.title || job.role || 'Untitled Role'}</h5>

                      <div className="card-timestamps">
                        {app.sent_at ? (
                          <div className="time-item">
                            <Send className="icon-xxs" />
                            <span>Sent: {new Date(app.sent_at).toLocaleDateString()}</span>
                          </div>
                        ) : (
                          <div className="time-item draft-time">
                            <span>Saved as Draft</span>
                          </div>
                        )}

                        {app.follow_up_due && app.status === 'sent' && (
                          <div className={`time-item ${isDue ? 'time-alert' : ''}`}>
                            <Clock className="icon-xxs" />
                            <span>
                              {isDue ? 'Follow-Up Due Now' : `Follow-Up: ${new Date(app.follow_up_due).toLocaleDateString()}`}
                            </span>
                          </div>
                        )}
                      </div>

                      {/* Follow-up count indicator */}
                      {app.follow_up_count > 0 && (
                        <div className="follow-up-count-pill">
                          <span>{app.follow_up_count} of 2 Follow-Ups Sent</span>
                        </div>
                      )}

                      {/* Quick Status Advancement Dropdown */}
                      <div className="card-status-select-row">
                        <select
                          value={app.status}
                          onChange={(e) => onUpdateStatus(app.id, e.target.value)}
                          className="status-dropdown"
                        >
                          <option value="draft">Draft</option>
                          <option value="sent">Sent</option>
                          <option value="responded">Responded</option>
                          <option value="interview">Interview</option>
                          <option value="offer">Offer</option>
                          <option value="rejected">Rejected</option>
                        </select>

                        <button
                          className="view-materials-btn"
                          onClick={() => onViewMaterials(app)}
                          title="View Tailored CV & Outreach"
                        >
                          <Eye className="icon-xs" />
                        </button>
                      </div>

                      {/* Follow-up Action CTA if due or sent */}
                      {app.status === 'sent' && app.follow_up_count < 2 && (
                        <button
                          className={`draft-followup-btn ${isDue ? 'pulse-alert' : ''}`}
                          onClick={() => onDraftFollowUp(app)}
                        >
                          <span>{isDue ? 'Draft Follow-Up Due' : 'Draft Next Follow-Up'}</span>
                        </button>
                      )}
                    </div>
                  );
                })}

                {appsInStage.length === 0 && (
                  <div className="column-empty-placeholder">
                    <span>No applications</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
