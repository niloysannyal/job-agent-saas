import React from 'react';
import { TrendingUp, Clock, Mail, CheckCircle, ArrowRight } from 'lucide-react';
import { useAgent } from '../../../hooks/useAgent';

export default function FunnelInsight({ props }) {
  const { sendMessage } = useAgent();
  const { funnel_counts = {}, recent_applications = [] } = props || {};

  const handleFollowUps = () => {
    sendMessage("Check which applications are due for a 7-day follow-up and prepare drafts", {
      action: "follow_ups",
    });
  };

  return (
    <div className="agent-widget funnel-insight">
      <div className="widget-header">
        <div className="widget-title-group">
          <TrendingUp size={16} className="text-emerald" />
          <span className="widget-title">Pipeline Health & Funnel</span>
        </div>
        <span className="widget-badge">Live Monitor</span>
      </div>

      <div className="funnel-metrics-grid">
        <div className="funnel-metric-card">
          <span className="metric-val">{funnel_counts.draft || 0}</span>
          <span className="metric-lbl">Drafts</span>
        </div>
        <div className="funnel-metric-card highlight">
          <span className="metric-val">{funnel_counts.applied || 0}</span>
          <span className="metric-lbl">Applied</span>
        </div>
        <div className="funnel-metric-card success">
          <span className="metric-val">{funnel_counts.interviewing || 0}</span>
          <span className="metric-lbl">Interviewing</span>
        </div>
        <div className="funnel-metric-card gold">
          <span className="metric-val">{funnel_counts.offer || 0}</span>
          <span className="metric-lbl">Offers</span>
        </div>
      </div>

      {recent_applications.length > 0 && (
        <div className="funnel-recent-list">
          <div className="list-title">Recent Submissions:</div>
          {recent_applications.map((app, i) => (
            <div key={i} className="funnel-app-row">
              <div className="app-info">
                <span className="app-role">{app.job_title}</span>
                <span className="app-company">{app.company}</span>
              </div>
              <span className={`status-tag status-${(app.status || 'applied').toLowerCase()}`}>
                {app.status || 'applied'}
              </span>
            </div>
          ))}
        </div>
      )}

      <div className="widget-footer-action">
        <button
          type="button"
          className="btn-outline-action"
          onClick={handleFollowUps}
        >
          <Mail size={13} />
          <span>Draft Due Follow-Ups</span>
        </button>
      </div>
    </div>
  );
}
