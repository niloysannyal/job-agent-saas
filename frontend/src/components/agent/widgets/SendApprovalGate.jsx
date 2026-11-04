import React, { useState } from 'react';
import { Send, CheckCircle2, XCircle, AlertCircle, Fingerprint, Mail, Clock } from 'lucide-react';
import { useAgent } from '../../../hooks/useAgent';

export default function SendApprovalGate({ props }) {
  const { approveProposal, rejectProposal } = useAgent();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const {
    proposal_id,
    status = 'pending',
    company,
    role,
    recipient,
    draft_body,
    ats_score = 90,
    cv_sha256,
  } = props || {};

  const isExecuted = status === 'executed' || status === 'approved';
  const isRejected = status === 'rejected';
  const isPending = status === 'pending';

  const handleApprove = async () => {
    if (!proposal_id || isSubmitting) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await approveProposal(proposal_id);
    } catch (err) {
      setErrorMsg(err.message || 'Approval failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReject = async () => {
    if (!proposal_id || isSubmitting) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await rejectProposal(proposal_id);
    } catch (err) {
      setErrorMsg(err.message || 'Rejection failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={`agent-widget send-approval-gate status-${status}`}>
      <div className="widget-header">
        <div className="widget-title-group">
          <Send size={16} className={isExecuted ? 'text-emerald' : 'text-amber'} />
          <span className="widget-title">Human-in-the-Loop Send Gate</span>
        </div>
        <div className={`status-pill pill-${status}`}>
          {isPending && <Clock size={11} />}
          {isExecuted && <CheckCircle2 size={11} />}
          {isRejected && <XCircle size={11} />}
          <span>{status.toUpperCase()}</span>
        </div>
      </div>

      <div className="proposal-body-card">
        <div className="proposal-entity">
          <div className="entity-label">Target Role & Company</div>
          <div className="entity-val">{role} — <span className="highlight-text">{company}</span></div>
        </div>

        {recipient && (
          <div className="proposal-meta-row">
            <Mail size={12} className="text-muted" />
            <span className="meta-text">{recipient}</span>
          </div>
        )}

        {cv_sha256 && (
          <div className="proposal-meta-row">
            <Fingerprint size={12} className="text-muted" />
            <span className="meta-text mono">CV Digest: {cv_sha256}</span>
          </div>
        )}

        {draft_body && (
          <div className="draft-snapshot-box">
            <div className="snapshot-header">Outreach Message Snapshot</div>
            <p className="snapshot-text">{draft_body.slice(0, 240)}{draft_body.length > 240 ? '...' : ''}</p>
          </div>
        )}
      </div>

      {errorMsg && (
        <div className="gate-error-banner">
          <AlertCircle size={13} />
          <span>{errorMsg}</span>
        </div>
      )}

      {isPending && (
        <div className="gate-actions-row">
          <button
            type="button"
            className="btn-gate-approve"
            disabled={isSubmitting}
            onClick={handleApprove}
          >
            <CheckCircle2 size={14} />
            <span>{isSubmitting ? 'Dispatching...' : 'Approve & Send'}</span>
          </button>
          <button
            type="button"
            className="btn-gate-reject"
            disabled={isSubmitting}
            onClick={handleReject}
          >
            <XCircle size={14} />
            <span>Reject</span>
          </button>
        </div>
      )}

      {isExecuted && (
        <div className="gate-executed-banner">
          <CheckCircle2 size={16} className="text-emerald" />
          <span>Application successfully dispatched. Added to Monitor Kanban.</span>
        </div>
      )}

      {isRejected && (
        <div className="gate-rejected-banner">
          <XCircle size={16} className="text-coral" />
          <span>Proposal was rejected. Agent will revise upon request.</span>
        </div>
      )}
    </div>
  );
}
