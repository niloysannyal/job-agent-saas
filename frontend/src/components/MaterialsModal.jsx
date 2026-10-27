import React, { useState } from 'react';
import {
  FileText,
  Copy,
} from 'lucide-react';

export default function MaterialsModal({
  app,
  onClose,
  showToast,
}) {
  const [activeTab, setActiveTab] = useState('cover'); // cover | outreach | notes

  if (!app) return null;

  const handleCopy = (text, label) => {
    navigator.clipboard.writeText(text);
    showToast(`${label} copied to clipboard!`);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card panel-card materials-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-header-left">
            <FileText className="icon-sm" />
            <div>
              <h3>Submitted Application Materials</h3>
              <p className="modal-sub">
                {app.job?.title} @ {app.job?.company}
              </p>
            </div>
          </div>
          <button className="close-modal-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="sub-nav-tabs">
          <button
            className={`sub-tab-btn ${activeTab === 'cover' ? 'active' : ''}`}
            onClick={() => setActiveTab('cover')}
          >
            <span>Cover Letter</span>
          </button>
          <button
            className={`sub-tab-btn ${activeTab === 'outreach' ? 'active' : ''}`}
            onClick={() => setActiveTab('outreach')}
          >
            <span>Outreach Drafts</span>
          </button>
          <button
            className={`sub-tab-btn ${activeTab === 'notes' ? 'active' : ''}`}
            onClick={() => setActiveTab('notes')}
          >
            <span>Internal Notes</span>
          </button>
        </div>

        {activeTab === 'cover' && (
          <div className="materials-content-block">
            <div className="editor-toolbar">
              <span>Cover Letter Submitted</span>
              <button
                className="action-btn-secondary"
                onClick={() => handleCopy(app.cover_letter_draft || '', 'Cover letter')}
              >
                <Copy className="btn-icon-xs" />
                <span>Copy</span>
              </button>
            </div>
            <pre className="materials-pre">{app.cover_letter_draft || 'No cover letter recorded.'}</pre>
          </div>
        )}

        {activeTab === 'outreach' && (
          <div className="materials-content-block">
            <div className="editor-toolbar">
              <span>Channel Outreach Messages</span>
            </div>
            <pre className="materials-pre">
              {JSON.stringify(app.outreach_drafts || {}, null, 2)}
            </pre>
          </div>
        )}

        {activeTab === 'notes' && (
          <div className="materials-content-block">
            <pre className="materials-pre">{app.notes || 'No notes added for this application.'}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
