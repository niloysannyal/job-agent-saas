import React, { useState, useEffect } from 'react';
import { ShieldCheck, RefreshCw, Send, Clock, RotateCcw, CheckCircle2 } from 'lucide-react';

export default function StudioApprovalGate({
  isSending = false,
  onApproveAndSend,
  onCancelSend,
  tailorResult,
  applications = [],
  activeJobId,
  editedCoverDraft,
  editedLatex,
}) {
  const applicationId =
    tailorResult?.application?.id ||
    applications.find((a) => a.job_id === activeJobId)?.id;

  const activeApp = applications.find((a) => a.id === applicationId || a.job_id === activeJobId);
  const isQueued = activeApp?.status === 'queued' || activeApp?.status === 'queued_in_hold';
  const isSent = activeApp?.status === 'sent' || activeApp?.status === 'applied';
  const isNeedsEdit = activeApp?.status === 'needs_edit';

  const [countdown, setCountdown] = useState(30);

  useEffect(() => {
    if (!isQueued) {
      setCountdown(30);
      return;
    }
    const interval = setInterval(() => {
      setCountdown((prev) => (prev <= 1 ? 0 : prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [isQueued]);

  return (
    <div className="send-gate-card">
      <div className="gate-notice-left">
        <ShieldCheck className="gate-shield-icon" />
        <div>
          <h4>Strict Human-in-the-Loop Send Gate</h4>
          <p>
            {isQueued ? (
              <>Application is in the <strong>Outbox Hold Queue (Undo Window)</strong>. Poller worker will dispatch via OAuth upon release.</>
            ) : isNeedsEdit ? (
              <span style={{ color: '#f87171' }}>Fact verification check flagged unverified statements. Please review the tailored CV above and edit facts before dispatching.</span>
            ) : isSent ? (
              <>Application was <strong>confirmed and dispatched</strong> to hiring team.</>
            ) : (
              <>This application is saved in <strong>Draft</strong> status. Review the preview above, then confirm to enqueue.</>
            )}
          </p>
        </div>
      </div>

      <div className="gate-actions-right">
        {isQueued ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', color: '#fbbf24', fontSize: '0.85rem' }}>
              <Clock size={14} className="icon-pulse" />
              <span>Undo: {countdown}s</span>
            </div>
            {onCancelSend && countdown > 0 && (
              <button
                type="button"
                className="btn-undo-send"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.35rem',
                  padding: '0.5rem 0.9rem',
                  borderRadius: '6px',
                  background: 'rgba(239, 68, 68, 0.15)',
                  border: '1px solid rgba(239, 68, 68, 0.4)',
                  color: '#f87171',
                  cursor: 'pointer',
                  fontWeight: 600,
                }}
                onClick={() => onCancelSend({ applicationId })}
              >
                <RotateCcw size={13} />
                <span>Undo Send</span>
              </button>
            )}
          </div>
        ) : isSent ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#34d399', fontWeight: 600 }}>
            <CheckCircle2 size={16} />
            <span>Applied</span>
          </div>
        ) : (
          <button
            className="approve-send-btn"
            disabled={isSending}
            onClick={() =>
              onApproveAndSend({
                applicationId,
                jobId: activeJobId,
                coverDraft: editedCoverDraft,
                tailoredLatex: editedLatex,
              })
            }
          >
            {isSending ? (
              <>
                <RefreshCw className="btn-icon icon-spin" />
                <span>Enqueuing...</span>
              </>
            ) : (
              <>
                <Send className="btn-icon" />
                <span>Approve & Send</span>
              </>
            )}
          </button>
        )}
      </div>
    </div>
  );
}
