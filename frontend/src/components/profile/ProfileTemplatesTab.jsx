import React from 'react';
import {
  Check,
  Copy,
  Layout,
  Columns,
  Sparkles,
  Download,
  Code2,
} from 'lucide-react';

export default function ProfileTemplatesTab({
  previewTemplateName,
  handleFetchPreview,
  isLoadingPreview,
  previewLatex,
  editedLatex,
  setEditedLatex,
  isCopied,
  handleCopyLatex,
  previewMode,
  setPreviewMode,
  handleDownloadLatex,
  parsedDoc,
  paginatedPages = [],
  profileForm,
}) {
  const renderA4Pages = () => {
    return (
      <div className="overleaf-multi-page-container">
        {paginatedPages.map((page, pIdx) => (
          <div key={pIdx} className="overleaf-a4-page-card" id={`profile-page-${page.pageNumber}`}>
            <div className="a4-page-top-badge">Page {page.pageNumber} of {paginatedPages.length}</div>

            {/* Document Header (Page 1) */}
            {page.hasHeader && (
              <div className="cv-header-container">
                <div className="cv-header-top-row">
                  <div className="cv-header-left">
                    <h1 className="cv-name">
                      {(parsedDoc.header.name || profileForm.full_name || 'CANDIDATE NAME').toUpperCase()}
                    </h1>
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
                    <div className="cv-location-line">
                      Location: {parsedDoc.header.location || [profileForm.location_city, profileForm.location_country].filter(Boolean).join(', ') || 'Remote / Worldwide'}
                    </div>
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
                  <h3 className="cv-section-heading">{sec.title}</h3>
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
                            <span className="quad-role-title">{item.role}</span>
                            <span className="quad-location-text">{item.locationOrDate}</span>
                          </div>
                          <div className="quad-row quad-bottom">
                            <span className="quad-company-text"><em>{item.companyOrDegree}</em></span>
                            {item.submeta && (
                              <span className="quad-dates-text"><em>{item.submeta}</em></span>
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

            {/* A4 Page Number Footer */}
            <div className="a4-page-number-footer">Page {page.pageNumber} of {paginatedPages.length}</div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div>
          <h3>Admin-Curated CV Template & Live Preview</h3>
          <p className="subtext">
            Your profile data compiles into pixel-perfect Overleaf LaTeX instantly with live side-by-side editing.
          </p>
        </div>
        <div className="header-actions">
          {/* Copy LaTeX button */}
          <button
            className="action-btn-secondary"
            onClick={handleCopyLatex}
            disabled={!previewLatex && !editedLatex}
            title="Copy full LaTeX source to clipboard"
          >
            {isCopied ? <Check size={16} className="text-emerald-400" /> : <Copy size={16} />}
            <span>{isCopied ? 'Copied!' : 'Copy LaTeX'}</span>
          </button>

          {/* Toggle Split Side-by-Side Mode */}
          <button
            className={previewMode === 'split' ? 'action-btn-primary' : 'action-btn-secondary'}
            onClick={() => setPreviewMode((prev) => (prev === 'split' ? 'preview' : 'split'))}
            title={previewMode === 'split' ? 'Switch to Full Page Preview' : 'Edit LaTeX & View Side-by-Side'}
          >
            {previewMode === 'split' ? <Layout size={16} /> : <Columns size={16} />}
            <span>{previewMode === 'split' ? 'Full Preview' : 'Edit LaTeX & Split View'}</span>
          </button>

          <button
            className="action-btn-secondary"
            onClick={() => handleFetchPreview()}
            disabled={isLoadingPreview}
          >
            <Sparkles size={16} /> Re-compile
          </button>

          <button
            className="action-btn-primary"
            onClick={handleDownloadLatex}
            disabled={!previewLatex && !editedLatex}
          >
            <Download size={16} /> Download .tex
          </button>
        </div>
      </div>

      {/* Template Switcher Buttons */}
      <div className="template-pills-row">
        <span className="pills-label">Active Template:</span>
        <button
          className={`pill-btn ${previewTemplateName === '01_MODERN_TECH' ? 'active' : ''}`}
          onClick={() => handleFetchPreview('01_MODERN_TECH')}
        >
          01_MODERN_TECH (Default)
        </button>
        <button
          className={`pill-btn ${previewTemplateName === '02_CLASSIC_CORPORATE' ? 'active' : ''}`}
          onClick={() => handleFetchPreview('02_CLASSIC_CORPORATE')}
        >
          02_CLASSIC_CORPORATE
        </button>
        <button
          className={`pill-btn ${previewTemplateName === '03_MINIMALIST_COMPACT' ? 'active' : ''}`}
          onClick={() => handleFetchPreview('03_MINIMALIST_COMPACT')}
        >
          03_MINIMALIST_COMPACT
        </button>
      </div>

      {/* DEFAULT MODE: Authentic Full-Page A4 Document Preview */}
      {previewMode === 'preview' && (
        <div className="cv-full-preview-container">
          {renderA4Pages()}
        </div>
      )}

      {/* SPLIT MODE: Side-by-Side Editor (Left) + Live Preview (Right) */}
      {previewMode === 'split' && (
        <div className="cv-preview-split-layout">
          {/* Left Column: Code Editor */}
          <div className="cv-editor-col">
            <div className="split-editor-toolbar">
              <div className="split-editor-title">
                <Code2 size={14} className="text-emerald-400" />
                <span>LaTeX Source Editor</span>
              </div>
              <div className="card-actions">
                <button
                  type="button"
                  className="btn-liveness-check"
                  onClick={() => setEditedLatex(previewLatex || '')}
                  title="Reset edits to server compiled source"
                >
                  Reset
                </button>
                <button
                  type="button"
                  className="btn-liveness-check"
                  onClick={handleCopyLatex}
                  title="Copy code"
                >
                  <Copy size={11} /> Copy
                </button>
              </div>
            </div>
            <textarea
              className="split-code-textarea"
              value={editedLatex}
              onChange={(e) => setEditedLatex(e.target.value)}
              placeholder="% Enter or edit your LaTeX document source here..."
              spellCheck="false"
            />
          </div>

          {/* Right Column: Live Compiled A4 Preview */}
          <div className="cv-preview-col">
            {renderA4Pages()}
          </div>
        </div>
      )}
    </div>
  );
}

