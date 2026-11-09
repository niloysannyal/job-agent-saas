import React from 'react';
import { ShieldCheck, RefreshCw, Send } from 'lucide-react';

export default function StudioApprovalGate({
  isSending = false,
  onApproveAndSend,
  tailorResult,
  applications = [],
  activeJobId,
  editedCoverDraft,
  editedLatex,
}) {
  const applicationId =
    tailorResult?.application?.id ||
    applications.find((a) => a.job_id === activeJobId)?.id;

  return (
    <div className="send-gate-card">
      <div className="gate-notice-left">
        <ShieldCheck className="gate-shield-icon" />
        <div>
          <h4>Strict Human-in-the-Loop Send Gate</h4>
          <p>
            This application is saved in <strong>Draft</strong> status. The platform never auto-sends.
            Review the materials in the preview pane above, then click below to confirm.
          </p>
        </div>
      </div>

      <div className="gate-actions-right">
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
              <span>Confirming...</span>
            </>
          ) : (
            <>
              <Send className="btn-icon" />
              <span>Approve & Mark Sent</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}

