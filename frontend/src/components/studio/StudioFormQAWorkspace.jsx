import React from 'react';
import {
  CheckSquare,
  Zap,
  Bookmark,
  RefreshCw,
  Sparkles,
  Copy,
  HelpCircle,
  Compass,
  Check,
  ExternalLink,
} from 'lucide-react';

export function StudioFormQAEditor({
  formQuestions = [],
  formAnswers = {},
  bookmarkletJs,
  handleCopyBookmarklet,
  handleGenerateFormAnswers,
  isGeneratingAnswers,
  handleCopyAllAnswers,
  handleDetectChannel,
  isDetectingChannel,
  copiedQuestionId,
  handleCopyQuestionAnswer,
  handleFormAnswerChange,
}) {
  return (
    <div className="form-qa-editor-view">
      {/* Top Action Row */}
      <div className="form-qa-action-row">
        <div className="qa-action-info">
          <CheckSquare className="icon-xs text-emerald" />
          <span>{formQuestions.length} Structured Form Fields Detected</span>
        </div>

        <div className="qa-action-buttons">
          {bookmarkletJs && (
            <a
              href={bookmarkletJs}
              className="draggable-bookmarklet-badge"
              title="Drag this link to your browser bookmarks bar! Click it on any job application page to auto-fill."
              onClick={(e) => {
                if (!e.defaultPrevented) {
                  e.preventDefault();
                  handleCopyBookmarklet();
                }
              }}
            >
              <Zap className="btn-icon-xxs text-amber" />
              <span>
                Drag: <strong>⚡ JobEazy Autofill</strong>
              </span>
            </a>
          )}

          <button
            className="action-btn-xs action-btn-accent"
            disabled={isGeneratingAnswers || formQuestions.length === 0}
            onClick={handleGenerateFormAnswers}
            title="Synthesizes candidate angles and verifies facts against STAR stories and fact ledger"
          >
            {isGeneratingAnswers ? (
              <>
                <RefreshCw className="btn-icon-xxs icon-spin" />
                <span>Synthesizing STAR Answers...</span>
              </>
            ) : (
              <>
                <Sparkles className="btn-icon-xxs" />
                <span>Generate Tailored Answers</span>
              </>
            )}
          </button>

          <button
            className="action-btn-xs"
            onClick={handleCopyBookmarklet}
            title="Copy browser bookmarklet to autofill Google Forms & ATS applications with 1 click"
          >
            <Bookmark className="btn-icon-xxs" />
            <span>Autofill Bookmarklet</span>
          </button>

          <button
            className="action-btn-xs"
            disabled={formQuestions.length === 0}
            onClick={handleCopyAllAnswers}
          >
            <Copy className="btn-icon-xxs" />
            <span>Copy All Answers</span>
          </button>
        </div>
      </div>

      {formQuestions.length === 0 ? (
        <div className="empty-qa-state">
          <HelpCircle className="empty-qa-icon" />
          <h4>No Questions Detected Yet</h4>
          <p>
            Click <strong>Detect Channel & Forms</strong> above to scan the target posting and apply
            URL for Google Forms, ATS, or custom questionnaire fields.
          </p>
          <button
            className="action-btn-secondary"
            disabled={isDetectingChannel}
            onClick={() => handleDetectChannel()}
          >
            <Compass className="btn-icon-xs" />
            <span>Detect Questions Now</span>
          </button>
        </div>
      ) : (
        <div className="qa-cards-scroll">
          {formQuestions.map((q, idx) => {
            const ansObj = formAnswers[q.id];
            const val = ansObj?.answer || '';
            const angles = ansObj?.candidate_angles || [];
            const facts = ansObj?.verified_facts_used || [];
            const charCount = ansObj?.char_count != null ? ansObj.char_count : val.length;
            const isCopied = copiedQuestionId === q.id;

            return (
              <div key={q.id || idx} className="qa-card">
                <div className="qa-card-header">
                  <div className="qa-prompt-wrap">
                    <span className="qa-q-num">Q{idx + 1}</span>
                    <strong className="qa-prompt-text">{q.prompt}</strong>
                  </div>
                  <button
                    className={`action-btn-xs ${isCopied ? 'btn-copied' : ''}`}
                    onClick={() => handleCopyQuestionAnswer(q.id, val, q.prompt)}
                    title="Copy answer to clipboard"
                  >
                    {isCopied ? (
                      <Check className="btn-icon-xxs text-emerald" />
                    ) : (
                      <Copy className="btn-icon-xxs" />
                    )}
                    <span>{isCopied ? 'Copied!' : 'Copy Field'}</span>
                  </button>
                </div>

                {angles.length > 0 && (
                  <div className="qa-angles-row">
                    <span className="angles-label">Strategic Angles:</span>
                    {angles.map((ang, aIdx) => (
                      <span key={aIdx} className="angle-tag">
                        {ang}
                      </span>
                    ))}
                  </div>
                )}

                <textarea
                  rows={4}
                  className="qa-answer-input"
                  value={val}
                  placeholder="Click 'Generate Tailored Answers' or type response..."
                  onChange={(e) => handleFormAnswerChange(q.id, e.target.value)}
                />

                <div className="qa-card-footer">
                  <div className="qa-footer-facts">
                    {facts.length > 0 && (
                      <span className="facts-count-badge">
                        ✓ Verified {facts.length} Fact{facts.length > 1 ? 's' : ''}
                      </span>
                    )}
                  </div>
                  <span className="qa-char-count">{charCount} characters</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export function StudioFormQADispatchHub({ channelInspection, profile }) {
  return (
    <div className="form-qa-dispatch-hub">
      <div className="column-toolbar overleaf-toolbar">
        <div className="overleaf-toolbar-left">
          <div className="column-title">
            <CheckSquare className="icon-xxs text-emerald" />
            <strong>Form Dispatch Hub & 1-Click Guide</strong>
          </div>
        </div>
      </div>

      <div className="dispatch-hub-body">
        <div className="dispatch-card-item">
          <h5>Target Platform & Detection:</h5>
          <p className="dispatch-status-text">
            {channelInspection?.action_summary ||
              'Review synthesized answers on the left. Click "Copy Field" to paste into the external application form.'}
          </p>
          {channelInspection?.apply_url && (
            <a
              href={channelInspection.apply_url}
              target="_blank"
              rel="noreferrer"
              className="dispatch-external-btn"
            >
              <span>Open Form in New Tab</span>
              <ExternalLink className="icon-xxs" />
            </a>
          )}
        </div>

        <div className="dispatch-card-item">
          <h5>Quick 3-Step Autofill Workflow:</h5>
          <ol className="dispatch-steps">
            <li>
              <strong>1. Synthesize:</strong> Click "Generate Tailored Answers" to craft structured
              responses grounded in your STAR story bank.
            </li>
            <li>
              <strong>2. Open Form:</strong> Open the target Google Form or ATS portal in a
              neighboring tab.
            </li>
            <li>
              <strong>3. 1-Click Paste:</strong> Click "Copy Field" on each answer to paste into
              the corresponding form field with zero re-typing.
            </li>
          </ol>
        </div>

        <div className="dispatch-card-item">
          <h5>Verified Profile References:</h5>
          <div className="dispatch-ref-grid">
            <div className="ref-row">
              <span className="ref-k">Full Name:</span>
              <span className="ref-v">{profile?.full_name || 'Niloy Sannyal'}</span>
            </div>
            <div className="ref-row">
              <span className="ref-k">Email:</span>
              <span className="ref-v">niloysannyal@gmail.com</span>
            </div>
            <div className="ref-row">
              <span className="ref-k">Portfolio:</span>
              <span className="ref-v">{profile?.portfolio_url || 'https://www.niloysannyal.me/'}</span>
            </div>
            <div className="ref-row">
              <span className="ref-k">GitHub:</span>
              <span className="ref-v">{profile?.github_url || 'https://github.com/niloysannyal'}</span>
            </div>
            <div className="ref-row">
              <span className="ref-k">Notice:</span>
              <span className="ref-v">{profile?.notice_period || '2 weeks'}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

