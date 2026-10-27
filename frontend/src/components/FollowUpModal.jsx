import React, { useState } from 'react';
import {
  Clock,
  Send,
  ShieldCheck,
  RefreshCw,
  Copy,
} from 'lucide-react';

export default function FollowUpModal({
  app,
  followUpData,
  onClose,
  onSendFollowUp,
  isSending = false,
  showToast,
}) {
  const [draftContent, setDraftContent] = useState(
    followUpData?.draft_content ||
      `Hi ${app?.job?.company || 'Team'},\n\nI wanted to follow up on my application for the ${app?.job?.title || 'open role'} sent on ${app?.sent_at ? new Date(app.sent_at).toLocaleDateString() : 'earlier'}. I remain very interested in contributing my hands-on production AI systems experience to your team.\n\nBest regards,\nNiloy Sannyal`
  );

  if (!app) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(draftContent);
    showToast('Follow-up message copied to clipboard!');
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card panel-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-header-left">
            <Clock className="icon-sm icon-amber" />
            <h3>10-Day Follow-Up Review Gate</h3>
          </div>
          <button className="close-modal-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-meta-bar">
          <div>
            <strong>{app.job?.title}</strong> @ {app.job?.company}
          </div>
          <span className="badge-counter">
            Follow-Up #{(app.follow_up_count || 0) + 1} of 2
          </span>
        </div>

        <div className="draft-editor-wrapper">
          <div className="editor-toolbar">
            <span>Editable Outreach Follow-Up Draft</span>
            <button className="action-btn-secondary" onClick={handleCopy}>
              <Copy className="btn-icon-xs" />
              <span>Copy</span>
            </button>
          </div>
          <textarea
            rows={8}
            className="draft-textarea"
            value={draftContent}
            onChange={(e) => setDraftContent(e.target.value)}
          />
        </div>

        <div className="send-gate-card">
          <div className="gate-notice-left">
            <ShieldCheck className="gate-shield-icon" />
            <div>
              <h4>Human Review Enforced</h4>
              <p>Strictly capped at 2 follow-ups per application per platform policy.</p>
            </div>
          </div>

          <div className="gate-actions-right">
            <button
              className="approve-send-btn"
              disabled={isSending}
              onClick={() => onSendFollowUp(app.id, draftContent)}
            >
              {isSending ? (
                <>
                  <RefreshCw className="btn-icon icon-spin" />
                  <span>Recording...</span>
                </>
              ) : (
                <>
                  <Send className="btn-icon" />
                  <span>Confirm & Send Follow-Up</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
