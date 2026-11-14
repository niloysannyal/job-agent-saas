import React, { useState, useEffect } from 'react';
import { Send, CheckCircle2, XCircle, AlertCircle, Fingerprint, Mail, Clock, RotateCcw } from 'lucide-react';
import { useAgent } from '../../../hooks/useAgent';

export default function SendApprovalGate({ props }) {
  const { approveProposal, rejectProposal, cancelProposal } = useAgent();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const {
    proposal_id,
    status = 'pending',
    undo_expires_at,
    company,
    role,
    recipient,
    draft_body,
    ats_score = 90,
    cv_sha256,
    downgrade_reason,
    is_trusted,
  } = props || {};

  const [isEditing, setIsEditing] = useState(false);
  const [editedBody, setEditedBody] = useState(draft_body || '');

  const isQueued = status === 'queued' || status === 'queued_in_hold';
  const isNeedsEdit = status === 'needs_edit';
  const isExecuted = status === 'executed' || status === 'approved' || status === 'sent' || status === 'applied';
  const isRejected = status === 'rejected';
  const isAborted = status === 'aborted';
  const isPending = status === 'pending' || status === 'waiting_approval';

  // Calculate remaining seconds for the 30s countdown
  const [countdown, setCountdown] = useState(() => {
    if (undo_expires_at) {
      const remaining = Math.max(0, Math.round((new Date(undo_expires_at).getTime() - Date.now()) / 1000));
      return remaining > 0 ? remaining : 0;
    }
    return 30;
  });

  useEffect(() => {
    if (!isQueued || countdown <= 0) return;
    const interval = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [isQueued, countdown]);

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

  const handleCancel = async () => {
    if (!proposal_id || isSubmitting) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      if (cancelProposal) {
        await cancelProposal(proposal_id);
      } else {
        await rejectProposal(proposal_id);
      }
    } catch (err) {
      setErrorMsg(err.message || 'Cancellation failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEditSubmit = async () => {
    if (!proposal_id || isSubmitting) return;
    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      await approveProposal(proposal_id, {
        action: 'edit',
        edited_body: editedBody,
      });
      setIsEditing(false);
    } catch (err) {
      setErrorMsg(err.message || 'Edit resubmission failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={`agent-widget send-approval-gate status-${status}`}>
      <div className="widget-header">
        <div className="widget-title-group">
          <Send size={16} className={isExecuted ? 'text-emerald' : isQueued ? 'text-amber' : 'text-amber'} />
          <span className="widget-title">Human-in-the-Loop Send Gate</span>
        </div>
        <div className={`status-pill pill-${status}`}>
          {isPending && <Clock size={11} />}
          {isQueued && <Clock size={11} className="icon-pulse" />}
          {isNeedsEdit && <AlertCircle size={11} className="text-coral" />}
          {isExecuted && <CheckCircle2 size={11} />}
          {isRejected && <XCircle size={11} />}
          {isAborted && <RotateCcw size={11} />}
          <span>{status.toUpperCase()}</span>
        </div>
      </div>

      {downgrade_reason && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', padding: '0.5rem 0.75rem', borderRadius: '6px', background: 'rgba(245, 158, 11, 0.12)', border: '1px solid rgba(245, 158, 11, 0.3)', color: '#fbbf24', fontSize: '0.78rem', marginBottom: '0.75rem' }}>
          <AlertCircle size={13} style={{ flexShrink: 0 }} />
          <span><strong>Policy Guard:</strong> {downgrade_reason}</span>
        </div>
      )}

      {isNeedsEdit && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', padding: '0.5rem 0.75rem', borderRadius: '6px', background: 'rgba(239, 68, 68, 0.12)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#f87171', fontSize: '0.78rem', marginBottom: '0.75rem' }}>
          <AlertCircle size={13} style={{ flexShrink: 0 }} />
          <span><strong>Fact Verification:</strong> Unverified claims flagged after retry. Please edit below.</span>
        </div>
      )}

      <div className="proposal-body-card">
        <div className="proposal-entity">
          <div className="entity-label">Target Role & Company</div>
          <div className="entity-val">{role} — <span className="highlight-text">{company}</span></div>
        </div>

        {recipient && (
          <div className="proposal-meta-row">
            <Mail size={12} className="text-muted" />
            <span className="meta-text">{recipient} {is_trusted && <span style={{ color: '#34d399', fontSize: '0.72rem', marginLeft: '0.3rem' }}>(Trusted TOFU)</span>}</span>
          </div>
        )}

        {cv_sha256 && (
          <div className="proposal-meta-row">
            <Fingerprint size={12} className="text-muted" />
            <span className="meta-text mono">CV Digest: {cv_sha256}</span>
          </div>
        )}

        {isEditing ? (
          <div style={{ marginTop: '0.6rem' }}>
            <label style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'block', marginBottom: '0.25rem' }}>Edit Outreach Message:</label>
            <textarea
              value={editedBody}
              onChange={(e) => setEditedBody(e.target.value)}
              rows={5}
              style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', background: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.15)', color: '#f1f5f9', fontSize: '0.8rem', fontFamily: 'inherit', resize: 'vertical' }}
            />
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.4rem' }}>
              <button
                type="button"
                className="btn-gate-approve"
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem' }}
                disabled={isSubmitting}
                onClick={handleEditSubmit}
              >
                <span>Save & Re-Audit</span>
              </button>
              <button
                type="button"
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', background: 'transparent', border: '1px solid rgba(255,255,255,0.2)', color: '#94a3b8', borderRadius: '6px', cursor: 'pointer' }}
                onClick={() => setIsEditing(false)}
              >
                <span>Cancel</span>
              </button>
            </div>
          </div>
        ) : (
          draft_body && (
            <div className="draft-snapshot-box">
              <div className="snapshot-header">Outreach Message Snapshot</div>
              <p className="snapshot-text">{draft_body.slice(0, 240)}{draft_body.length > 240 ? '...' : ''}</p>
            </div>
          )
        )}
      </div>

      {errorMsg && (
        <div className="gate-error-banner">
          <AlertCircle size={13} />
          <span>{errorMsg}</span>
        </div>
      )}

      {isPending && !isEditing && (
        <div className="gate-actions-row">
          <button
            type="button"
            className="btn-gate-approve"
            disabled={isSubmitting}
            onClick={handleApprove}
          >
            <CheckCircle2 size={14} />
            <span>{isSubmitting ? 'Queuing...' : 'Approve & Send'}</span>
          </button>
          <button
            type="button"
            style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', padding: '0.4rem 0.75rem', borderRadius: '6px', background: 'rgba(59, 130, 246, 0.15)', border: '1px solid rgba(59, 130, 246, 0.35)', color: '#60a5fa', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer' }}
            disabled={isSubmitting}
            onClick={() => setIsEditing(true)}
          >
            <span>Edit Copy</span>
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

      {isQueued && (
        <div className="gate-queued-box" style={{ marginTop: '0.75rem', padding: '0.75rem', borderRadius: '8px', background: 'rgba(245, 158, 11, 0.08)', border: '1px solid rgba(245, 158, 11, 0.25)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.82rem', color: '#fbbf24' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Clock size={13} />
              <span>Outbox Hold: {countdown > 0 ? `${countdown}s remaining to undo` : 'Hold released. Outbox poller dispatching...'}</span>
            </div>
            {countdown > 0 && (
              <button
                type="button"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.3rem',
                  padding: '0.3rem 0.6rem',
                  fontSize: '0.75rem',
                  borderRadius: '6px',
                  background: 'rgba(239, 68, 68, 0.15)',
                  border: '1px solid rgba(239, 68, 68, 0.4)',
                  color: '#f87171',
                  cursor: isSubmitting ? 'not-allowed' : 'pointer',
                  fontWeight: 600,
                }}
                disabled={isSubmitting}
                onClick={handleCancel}
              >
                <RotateCcw size={12} />
                <span>{isSubmitting ? 'Cancelling...' : `Undo (${countdown}s)`}</span>
              </button>
            )}
          </div>
          <div style={{ width: '100%', height: '4px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '2px', overflow: 'hidden' }}>
            <div
              style={{
                width: `${Math.min(100, (countdown / 30) * 100)}%`,
                height: '100%',
                background: '#fbbf24',
                transition: 'width 1s linear',
              }}
            />
          </div>
        </div>
      )}

      {isExecuted && (
        <div className="gate-executed-banner">
          <CheckCircle2 size={16} className="text-emerald" />
          <span>Application successfully dispatched. Added to Monitor Kanban.</span>
        </div>
      )}

      {isAborted && (
        <div className="gate-rejected-banner" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem', color: '#f87171' }}>
          <RotateCcw size={15} />
          <span>Dispatch cancelled by candidate during countdown. Reverted to draft.</span>
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
