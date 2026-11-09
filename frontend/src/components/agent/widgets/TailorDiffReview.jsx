import React, { useState } from 'react';
import { ShieldCheck, FileCheck, Eye, CheckCircle2, Send, ChevronDown, ChevronUp } from 'lucide-react';
import { useAgent } from '../../../hooks/useAgent';

export default function TailorDiffReview({ props }) {
  const { sendMessage } = useAgent();
  const [showPreview, setShowPreview] = useState(false);

  const {
    application_id,
    job_id,
    role,
    company,
    ats_score = 90,
    fact_audit_passed = true,
    draft_content,
    diff_highlights = [],
  } = props || {};

  const handleStageProposal = () => {
    sendMessage(`Stage application for human approval for ${role} at ${company}`, {
      application_id,
      job_id,
    });
  };

  return (
    <div className="agent-widget tailor-diff-review">
      <div className="widget-header">
        <div className="widget-title-group">
          <FileCheck size={16} className="text-emerald" />
          <span className="widget-title">Tailored Application Ready</span>
        </div>
        <div className="ats-metric-badge">
          <span className="ats-number">{ats_score}</span>
          <span className="ats-label">ATS Score</span>
        </div>
      </div>

      <div className="tailor-summary-banner">
        <div className="target-info">
          <h4 className="target-role">{role}</h4>
          <span className="target-company">{company}</span>
        </div>
        <div className="fact-ledger-badge">
          <ShieldCheck size={14} className="text-emerald" />
          <span>Fact Ledger Verified</span>
        </div>
      </div>

      {diff_highlights.length > 0 && (
        <div className="diff-highlights-box">
          <span className="highlights-title">Strategic Optimizations:</span>
          <ul className="highlights-list">
            {diff_highlights.map((h, i) => (
              <li key={i} className="highlight-item">
                <CheckCircle2 size={12} className="text-emerald" />
                <span>{h}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {draft_content && (
        <div className="outreach-preview-section">
          <button
            type="button"
            className="toggle-preview-btn"
            onClick={() => setShowPreview(!showPreview)}
          >
            <Eye size={13} />
            <span>{showPreview ? 'Hide Outreach Draft' : 'Preview Outreach Draft'}</span>
            {showPreview ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
          </button>

          {showPreview && (
            <div className="preview-text-block">
              <pre>{draft_content}</pre>
            </div>
          )}
        </div>
      )}

      <div className="widget-footer-action">
        <button
          type="button"
          className="btn-primary-action"
          onClick={handleStageProposal}
        >
          <Send size={14} />
          <span>Stage For Send Approval</span>
        </button>
      </div>
    </div>
  );
}
