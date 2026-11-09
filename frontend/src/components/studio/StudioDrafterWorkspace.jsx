import React from 'react';
import {
  Terminal,
  FileText,
  Mail,
  CheckSquare,
  Bookmark,
  Zap,
  Copy,
  Download,
  Scissors,
  HelpCircle,
  Compass,
  RefreshCw,
  Sparkles,
  Eye,
  ZoomIn,
  ZoomOut,
  Printer,
  ExternalLink,
  Check,
} from 'lucide-react';
import StudioFactAuditBadge from './StudioFactAuditBadge';
import { StudioFormQAEditor, StudioFormQADispatchHub } from './StudioFormQAWorkspace';
import { decodeHtmlEntities } from '../../utils/latexCompiler';

export default function StudioDrafterWorkspace({
  activeDraftTab,
  setActiveDraftTab,
  channel,
  formQuestions = [],
  formAnswers = {},
  bookmarkletJs,
  handleCopyBookmarklet,
  handleCopyAllAnswers,
  handleCopyDraft,
  handleDownloadLatex,
  handleCompactToPages,
  editedCoverDraft,
  setEditedCoverDraft,
  editedOutreachDraft,
  setEditedOutreachDraft,
  editedLatex,
  setEditedLatex,
  handleKeyDown,
  customCompany,
  customRole,
  profile,
  channelInspection,
  handleDownloadEml,
  googleConnected,
  isDraftingGmail,
  handleDraftInGmail,
  handleConnectGmail,
  gmailDraftLink,
  isGeneratingAnswers,
  handleGenerateFormAnswers,
  handleDetectChannel,
  isDetectingChannel,
  copiedQuestionId,
  handleCopyQuestionAnswer,
  handleFormAnswerChange,
  handleCompile,
  isCompiling,
  zoomLevel,
  setZoomLevel,
  handleDownloadPdf,
  handlePrint,
  previewRef,
  paginatedPages = [],
  parsedDoc,
}) {
  return (
    <div className="split-workspace-panel panel-card overleaf-workspace">
      {/* Workspace Subheader Navigation */}
      <div className="workspace-tabs-bar">
        <div className="draft-tabs-group">
          <button
            className={`draft-tab ${activeDraftTab === 'latex' ? 'active' : ''}`}
            onClick={() => setActiveDraftTab('latex')}
          >
            <Terminal className="tab-icon-sm" />
            <span>Tailored LaTeX CV (Overleaf Engine)</span>
          </button>
          <button
            className={`draft-tab ${activeDraftTab === 'cover' ? 'active' : ''}`}
            onClick={() => setActiveDraftTab('cover')}
          >
            <FileText className="tab-icon-sm" />
            <span>Cover Letter Draft</span>
          </button>
          <button
            className={`draft-tab ${activeDraftTab === 'outreach' ? 'active' : ''}`}
            onClick={() => setActiveDraftTab('outreach')}
          >
            <Mail className="tab-icon-sm" />
            <span>Channel Outreach ({channel.toUpperCase()})</span>
          </button>
          <button
            className={`draft-tab ${activeDraftTab === 'form_qa' ? 'active' : ''}`}
            onClick={() => setActiveDraftTab('form_qa')}
          >
            <CheckSquare className="tab-icon-sm" />
            <span>Form Questionnaire ({formQuestions.length})</span>
          </button>
        </div>

        <StudioFactAuditBadge />
      </div>

      {/* 2-COLUMN SPLIT CONTAINER (OR 1-COLUMN FOR OUTREACH EMAIL) */}
      <div className={`split-editor-grid overleaf-grid ${activeDraftTab === 'outreach' ? 'outreach-single-column' : ''}`}>
        {/* LEFT COLUMN: CODE EDITOR */}
        <div className="editor-column overleaf-editor-column">
          <div className="column-toolbar overleaf-editor-toolbar">
            <div className="column-title">
              <strong>
                {activeDraftTab === 'latex'
                  ? 'main.tex (LaTeX Source)'
                  : activeDraftTab === 'cover'
                  ? 'cover_letter.txt'
                  : activeDraftTab === 'form_qa'
                  ? 'form_questionnaire.json'
                  : `outreach_${channel}.txt`}
              </strong>
            </div>

            <div className="toolbar-actions">
              {activeDraftTab === 'form_qa' ? (
                <div className="btn-group-row">
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
                      <span>Drag: <strong>⚡ JobEazy Autofill</strong></span>
                    </a>
                  )}
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
                    onClick={handleCopyAllAnswers}
                    title="Copy all questions and generated answers into formatted text"
                  >
                    <Copy className="btn-icon-xxs" />
                    <span>Copy All Q&A</span>
                  </button>
                </div>
              ) : (
                <button
                  className="action-btn-xs"
                  onClick={() =>
                    handleCopyDraft(
                      activeDraftTab === 'cover'
                        ? editedCoverDraft
                        : activeDraftTab === 'outreach'
                        ? editedOutreachDraft
                        : editedLatex,
                      activeDraftTab === 'cover'
                        ? 'Cover Letter'
                        : activeDraftTab === 'outreach'
                        ? 'Outreach Message'
                        : 'LaTeX Source'
                    )
                  }
                  title="Copy content"
                >
                  <Copy className="btn-icon-xxs" />
                  <span>Copy</span>
                </button>
              )}

              {activeDraftTab === 'latex' && (
                <>
                  <div className="compact-dropdown-wrap">
                    <Scissors className="btn-icon-xxs" />
                    <select
                      className="compact-select"
                      defaultValue=""
                      onChange={(e) => {
                        if (e.target.value) {
                          handleCompactToPages(Number(e.target.value));
                          e.target.value = '';
                        }
                      }}
                      title="Budget CV to 1 or 2 pages"
                    >
                      <option value="" disabled>Compact...</option>
                      <option value="1">1 Page</option>
                      <option value="2">2 Pages</option>
                    </select>
                  </div>
                  <button
                    className="action-btn-xs"
                    onClick={handleDownloadLatex}
                    title="Download raw LaTeX (.tex) file"
                  >
                    <Download className="btn-icon-xxs" />
                    <span>.tex</span>
                  </button>
                </>
              )}
            </div>
          </div>

          <div className="textarea-container">
            {activeDraftTab === 'cover' && (
              <textarea
                rows={20}
                className="code-textarea"
                value={editedCoverDraft}
                onChange={(e) => setEditedCoverDraft(e.target.value)}
                placeholder="Cover letter draft..."
              />
            )}

            {activeDraftTab === 'outreach' && (
              <div className="outreach-composer-view">
                <div className="email-subject-bar">
                  <span className="email-label">Subject:</span>
                  <input
                    type="text"
                    className="email-subject-input"
                    value={`Application: ${customRole || 'AI Engineer'} - ${profile?.full_name || 'Niloy Sannyal'}`}
                    readOnly
                  />
                  <button
                    className="action-btn-xs copy-subject-btn"
                    onClick={() => handleCopyDraft(`Application: ${customRole || 'AI Engineer'} - ${profile?.full_name || 'Niloy Sannyal'}`, 'Subject Line')}
                    title="Copy Subject"
                  >
                    <Copy className="btn-icon-xxs" />
                    <span>Copy</span>
                  </button>
                </div>

                {channel === 'email' && (
                  <div className="email-dispatch-action-bar">
                    <a
                      href={`mailto:${channelInspection?.recruiter_email || ''}?subject=${encodeURIComponent(
                        `Application: ${customRole || 'AI Engineer'} - ${profile?.full_name || 'Niloy Sannyal'}`
                      )}&body=${encodeURIComponent(editedOutreachDraft || editedCoverDraft || '')}`}
                      className="action-btn-xs action-btn-mailto"
                      title="Open default email client with recruiter and pitch pre-filled"
                    >
                      <Mail className="btn-icon-xxs" />
                      <span>Launch in Email Client</span>
                    </a>

                    <button
                      className="action-btn-xs action-btn-accent"
                      onClick={handleDownloadEml}
                      title="Download RFC 822 .eml draft file with tailored CV attached"
                    >
                      <Download className="btn-icon-xxs" />
                      <span>Download .eml Draft with CV</span>
                    </button>

                    <button
                      className={`action-btn-xs action-btn-gmail ${googleConnected ? 'connected' : ''}`}
                      onClick={googleConnected ? handleDraftInGmail : handleConnectGmail}
                      disabled={isDraftingGmail}
                      title={googleConnected ? "Create a 1-click draft in your Gmail account" : "Connect your Google account to enable 1-click Gmail drafting"}
                    >
                      <Sparkles className="btn-icon-xxs" />
                      <span>
                        {isDraftingGmail
                          ? 'Creating Draft...'
                          : googleConnected
                          ? 'Draft in Gmail (1-Click)'
                          : 'Connect Gmail'}
                      </span>
                    </button>

                    {gmailDraftLink && (
                      <a
                        href={gmailDraftLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="action-btn-xs action-btn-view-draft"
                        title="Open newly created draft directly in Gmail"
                      >
                        <ExternalLink className="btn-icon-xxs" />
                        <span>Open Draft in Gmail</span>
                      </a>
                    )}
                  </div>
                )}

                <textarea
                  rows={18}
                  className="code-textarea outreach-body-textarea"
                  value={editedOutreachDraft}
                  onChange={(e) => setEditedOutreachDraft(e.target.value)}
                  placeholder="Direct outreach email pitch..."
                />
              </div>
            )}

            {activeDraftTab === 'latex' && (
              <textarea
                rows={20}
                className="code-textarea font-mono overleaf-textarea"
                value={editedLatex}
                onChange={(e) => setEditedLatex(e.target.value)}
                onKeyDown={handleKeyDown}
                spellCheck={false}
                placeholder="\documentclass[a4paper,11pt]{article}..."
              />
            )}

            {activeDraftTab === 'form_qa' && (
              <StudioFormQAEditor
                formQuestions={formQuestions}
                formAnswers={formAnswers}
                bookmarkletJs={bookmarkletJs}
                handleCopyBookmarklet={handleCopyBookmarklet}
                handleGenerateFormAnswers={handleGenerateFormAnswers}
                isGeneratingAnswers={isGeneratingAnswers}
                handleCopyAllAnswers={handleCopyAllAnswers}
                handleDetectChannel={handleDetectChannel}
                isDetectingChannel={isDetectingChannel}
                copiedQuestionId={copiedQuestionId}
                handleCopyQuestionAnswer={handleCopyQuestionAnswer}
                handleFormAnswerChange={handleFormAnswerChange}
              />
            )}
          </div>
        </div>

        {/* RIGHT COLUMN: PREVIEW (FOR LATEX / COVER / FORM_QA) */}
        {activeDraftTab !== 'outreach' && (
          <div className="preview-column overleaf-preview-column">
            {activeDraftTab === 'form_qa' ? (
              <StudioFormQADispatchHub
                channelInspection={channelInspection}
                profile={profile}
              />
            ) : (
              <>
                {/* OVERLEAF PREVIEW TOOLBAR */}
                <div className="column-toolbar overleaf-toolbar">
                  <div className="overleaf-toolbar-left">
                    {activeDraftTab === 'latex' ? (
                      <button
                        className={`overleaf-compile-btn ${isCompiling ? 'loading' : ''}`}
                        onClick={handleCompile}
                        disabled={isCompiling}
                        title="Compile LaTeX source code (Ctrl + Enter)"
                      >
                        {isCompiling ? (
                          <RefreshCw className="btn-icon-xs icon-spin" />
                        ) : (
                          <Eye className="btn-icon-xs" />
                        )}
                        <span>{isCompiling ? 'Compiling...' : 'Recompile'}</span>
                        <kbd className="overleaf-kbd">Ctrl+↵</kbd>
                      </button>
                    ) : (
                      <div className="column-title">
                        <Eye className="icon-xxs" />
                        <strong>Formatted Document Preview</strong>
                      </div>
                    )}
                  </div>

                  <div className="overleaf-toolbar-right">
                    {/* Overleaf Zoom Controls */}
                    <div className="zoom-controls-group">
                      <button
                        className="zoom-btn"
                        onClick={() => setZoomLevel((z) => Math.max(70, z - 10))}
                        title="Zoom Out"
                      >
                        <ZoomOut className="icon-xxs" />
                      </button>
                      <span className="zoom-label">{zoomLevel}%</span>
                      <button
                        className="zoom-btn"
                        onClick={() => setZoomLevel((z) => Math.min(130, z + 10))}
                        title="Zoom In"
                      >
                        <ZoomIn className="icon-xxs" />
                      </button>
                    </div>

                    <button
                      className="action-btn-xs action-btn-pdf"
                      onClick={handleDownloadPdf}
                      title="Generate and download compiled PDF document"
                    >
                      <Download className="btn-icon-xxs" />
                      <span>Download PDF</span>
                    </button>

                    <button
                      className="action-btn-xs"
                      onClick={handlePrint}
                      title="Print or Save via browser dialog"
                    >
                      <Printer className="btn-icon-xxs" />
                      <span>Print</span>
                    </button>
                  </div>
                </div>

                {/* PREVIEW SHEET WRAPPER */}
                <div className="preview-sheet-wrapper overleaf-viewer-bg" ref={previewRef}>
                  {/* DYNAMIC LATEX COMPILED MULTI-PAGE DOCUMENT PREVIEW */}
                  {activeDraftTab === 'latex' ? (
                    <div
                      className="overleaf-multi-page-container"
                      style={{
                        transform: `scale(${zoomLevel / 100})`,
                        transformOrigin: 'top center',
                      }}
                    >
                      {paginatedPages.map((page, pIdx) => (
                        <div key={pIdx} className="overleaf-a4-page-card" id={`overleaf-page-${page.pageNumber}`}>
                          {/* Authentic Page Tag Badge */}
                          <div className="a4-page-top-badge">Page {page.pageNumber} of {paginatedPages.length}</div>

                          {/* Document Header (Rendered on Page 1) */}
                          {page.hasHeader && (
                            <div className="cv-header-container">
                              <div className="cv-header-top-row">
                                <div className="cv-header-left">
                                  <h1 className="cv-name">{(parsedDoc.header.name || 'NILOY SANNYAL').toUpperCase()}</h1>
                                  <div className="cv-header-links-row">
                                    {parsedDoc.header.leftLinks.map((lk, lIdx) => (
                                      <React.Fragment key={lIdx}>
                                        <a
                                          href={lk.url}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          className="cv-header-link"
                                          title={lk.url}
                                        >
                                          {lk.label}
                                        </a>
                                        {lIdx < parsedDoc.header.leftLinks.length - 1 && (
                                          <span className="cv-link-pipe">|</span>
                                        )}
                                      </React.Fragment>
                                    ))}
                                  </div>
                                </div>

                                <div className="cv-header-right">
                                  <div className="cv-location-line">Location: {parsedDoc.header.location || 'Dhaka, Bangladesh'}</div>
                                  <div className="cv-header-contact-row">
                                    {parsedDoc.header.rightLinks.map((rk, rIdx) => (
                                      <React.Fragment key={rIdx}>
                                        <span className="cv-contact-prefix">
                                          {rk.url.startsWith('mailto:') ? 'Email: ' : 'Mobile: '}
                                        </span>
                                        <a
                                          href={rk.url}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          className="cv-header-link"
                                          title={rk.url}
                                        >
                                          {rk.label}
                                        </a>
                                        {rIdx < parsedDoc.header.rightLinks.length - 1 && (
                                          <span className="cv-link-pipe">|</span>
                                        )}
                                      </React.Fragment>
                                    ))}
                                  </div>
                                </div>
                              </div>

                              <div className="cv-header-divider" />
                            </div>
                          )}

                          {/* Sections on this page */}
                          {page.sections.map((sec, secIdx) => (
                            <div key={secIdx} className="cv-section-container">
                              <div className="cv-section-title-wrap">
                                <h3 className="cv-section-heading">{(sec.title || '').replace(/\s*\((?:cont\.?|continued)\)/gi, '').trim()}</h3>
                                <div className="cv-section-rule" />
                              </div>

                              <div className="cv-section-items-body">
                                {sec.items.map((item, itemIdx) => {
                                  if (item.type === 'skills_line') {
                                    return (
                                      <div key={itemIdx} className="cv-skills-row">
                                        <strong
                                          className="skills-category-col"
                                          dangerouslySetInnerHTML={{
                                            __html: item.categoryHtml ? `${item.categoryHtml}:` : `${item.category}:`,
                                          }}
                                        />
                                        <span
                                          className="skills-content-col"
                                          dangerouslySetInnerHTML={{ __html: item.contentHtml }}
                                        />
                                      </div>
                                    );
                                  }
                                  if (item.type === 'heading') {
                                    return (
                                      <div key={itemIdx} className="cv-quad-heading-block">
                                        <div className="quad-row quad-top">
                                          <span
                                            className="quad-role-title"
                                            dangerouslySetInnerHTML={{ __html: item.roleHtml || item.role }}
                                          />
                                          <span
                                            className="quad-location-text"
                                            dangerouslySetInnerHTML={{ __html: item.locationOrDateHtml || item.locationOrDate }}
                                          />
                                        </div>
                                        <div className="quad-row quad-bottom">
                                          <span
                                            className="quad-company-text"
                                            dangerouslySetInnerHTML={{ __html: `<em>${item.companyOrDegreeHtml || item.companyOrDegree}</em>` }}
                                          />
                                          {(item.submetaHtml || item.submeta) && (
                                            <span
                                              className="quad-dates-text"
                                              dangerouslySetInnerHTML={{ __html: `<em>${item.submetaHtml || item.submeta}</em>` }}
                                            />
                                          )}
                                        </div>
                                      </div>
                                    );
                                  }
                                  if (item.type === 'trio_heading') {
                                    return (
                                      <div key={itemIdx} className="cv-trio-heading-block">
                                        <div
                                          className="trio-title-text"
                                          dangerouslySetInnerHTML={{ __html: item.contentHtml }}
                                        />
                                        {item.right && <span className="trio-right-text">{item.right}</span>}
                                      </div>
                                    );
                                  }
                                  if (item.type === 'bullet') {
                                    return (
                                      <div key={itemIdx} className="cv-bullet-item-row">
                                        <span className="cv-bullet-point">•</span>
                                        <div
                                          className="cv-bullet-text-wrap"
                                          dangerouslySetInnerHTML={{ __html: item.contentHtml }}
                                        />
                                      </div>
                                    );
                                  }
                                  return (
                                    <div
                                      key={itemIdx}
                                      className="cv-prose-text-wrap"
                                      dangerouslySetInnerHTML={{ __html: item.contentHtml }}
                                    />
                                  );
                                })}
                              </div>
                            </div>
                          ))}

                          {/* Authentic A4 Page Number Footer */}
                          <div className="a4-page-number-footer">
                            Page {page.pageNumber} of {paginatedPages.length}
                          </div>
                        </div>
                      ))}

                      {paginatedPages.length === 0 && (
                        <div className="empty-latex-notice">
                          <p>Click <strong>Recompile</strong> to compile your LaTeX code into the visual document preview.</p>
                        </div>
                      )}
                    </div>
                  ) : (
                    /* COVER LETTER PREVIEW */
                    <div
                      className="letter-paper-preview overleaf-paper"
                      style={{
                        transform: `scale(${zoomLevel / 100})`,
                        transformOrigin: 'top center',
                      }}
                    >
                      <div className="letter-header">
                        <h2>{decodeHtmlEntities(profile?.full_name || 'Niloy Sannyal')}</h2>
                        <p className="letter-subhead">
                          Dhaka, Bangladesh • niloysannyal@gmail.com • +8801783445245 • niloysannyal.me
                        </p>
                        <div className="letter-rule"></div>
                      </div>

                      <div className="letter-meta-block">
                        <p>
                          <strong>Date:</strong>{' '}
                          {new Date().toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                          })}
                        </p>
                        <p>
                          <strong>To:</strong> Hiring Team at {decodeHtmlEntities(customCompany || 'Target Company')}
                        </p>
                        <p>
                          <strong>Re:</strong> Application for {decodeHtmlEntities(customRole || 'AI Engineer')}
                        </p>
                      </div>

                      <div className="letter-body">
                        {decodeHtmlEntities(editedCoverDraft)
                          .split(/\n\s*\n/)
                          .map((paragraph, idx) => (
                            <p key={idx} className="letter-paragraph">
                              {paragraph.trim()}
                            </p>
                          ))}
                      </div>

                      <div className="letter-signature-block">
                        <p>Sincerely,</p>
                        <p className="signature-name">{decodeHtmlEntities(profile?.full_name || 'Niloy Sannyal')}</p>
                        <p className="signature-title">AI Engineer</p>
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
