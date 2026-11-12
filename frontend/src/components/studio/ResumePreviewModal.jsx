import React, { useState, useEffect } from 'react';
import {
  X,
  ZoomIn,
  ZoomOut,
  Download,
  FileText,
  FileCode,
  Maximize2,
  Minimize2,
} from 'lucide-react';
import { downloadPdfDocument, downloadLatexSource } from './studioExportUtils';

export default function ResumePreviewModal({
  isOpen,
  onClose,
  parsedDoc,
  paginatedPages = [],
  companyName = 'Company',
  roleTitle = 'Role',
  profile,
  latexSource = '',
  showToast,
}) {
  const [zoomLevel, setZoomLevel] = useState(85);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop resume-preview-modal-backdrop" onClick={onClose}>
      <div
        className="modal-container resume-preview-modal-dialog overleaf-viewer-bg"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label="Tailored Resume Preview"
      >
        {/* MODAL HEADER */}
        <div className="resume-preview-modal-header">
          <div className="preview-modal-title-box">
            <FileText size={18} className="text-emerald-400" />
            <div>
              <h3 className="preview-modal-title">
                Tailored CV Preview — {roleTitle} at {companyName}
              </h3>
              <span className="preview-modal-subtitle">
                Overleaf-grade A4 PDF • 100% ATS Parsable Text Layer
              </span>
            </div>
          </div>

          <div className="preview-modal-actions">
            {/* Zoom Controls */}
            <div className="cv-zoom-controls">
              <button
                type="button"
                className="zoom-btn"
                onClick={() => setZoomLevel((z) => Math.max(50, z - 10))}
                title="Zoom Out"
              >
                <ZoomOut size={13} />
              </button>
              <span className="zoom-value">{zoomLevel}%</span>
              <button
                type="button"
                className="zoom-btn"
                onClick={() => setZoomLevel((z) => Math.min(130, z + 10))}
                title="Zoom In"
              >
                <ZoomIn size={13} />
              </button>
            </div>

            {/* Quick Download PDF */}
            <button
              type="button"
              className="action-btn-primary"
              onClick={() => {
                downloadPdfDocument({
                  parsedDoc,
                  customCompany: companyName,
                  customRole: roleTitle,
                  profile,
                  showToast,
                });
              }}
              title="Download compiled PDF to local machine"
            >
              <Download size={14} />
              <span>Download PDF</span>
            </button>

            {/* Close Button */}
            <button
              type="button"
              className="modal-close-btn"
              onClick={onClose}
              title="Close Preview (Esc)"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* MODAL BODY: SCROLLABLE A4 PAGES */}
        <div className="resume-preview-modal-body">
          <div className="overleaf-pages-column" style={{ zoom: zoomLevel / 100, margin: '0 auto' }}>
            {paginatedPages.map((page, pIdx) => (
              <div key={pIdx} className="overleaf-a4-page-card" id={`modal-page-${page.pageNumber}`}>
                <div className="a4-page-top-badge">Page {page.pageNumber} of {paginatedPages.length}</div>

                {/* Document Header (Page 1) */}
                {page.hasHeader && (
                  <div className="cv-header-container">
                    <div className="cv-header-top-row">
                      <div className="cv-header-left">
                        <h1 className="cv-name">
                          {(parsedDoc.header?.name || profile?.full_name || 'CANDIDATE NAME').toUpperCase()}
                        </h1>
                        <div className="cv-header-links-row">
                          {(parsedDoc.header?.leftLinks || []).map((lk, lIdx) => (
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
                          Location: {parsedDoc.header?.location || [profile?.location_city, profile?.location_country].filter(Boolean).join(', ') || 'Remote / Worldwide'}
                        </div>
                        <div className="cv-header-contact-row">
                          {(parsedDoc.header?.rightLinks || []).map((rk, rIdx) => (
                            <React.Fragment key={rIdx}>
                              <span className="cv-contact-prefix">
                                {rk.url?.startsWith('mailto:') ? 'Email: ' : 'Mobile: '}
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
                {(page.sections || []).map((sec, secIdx) => {
                  const cleanTitle = (sec.title || '').replace(/\s*\((?:cont\.?|continued)\)/gi, '').trim();
                  const showTitle = Boolean(cleanTitle && !sec.isContinuation);
                  return (
                    <div key={secIdx} className="cv-section-container">
                      {showTitle && (
                        <div className="cv-section-title-wrap">
                          <h3 className="cv-section-heading">{cleanTitle}</h3>
                          <div className="cv-section-rule" />
                        </div>
                      )}

                      <div className="cv-section-items-body">
                        {(sec.items || []).map((item, itemIdx) => {
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
                  );
                })}

                <div className="a4-page-number-footer">Page {page.pageNumber} of {paginatedPages.length}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

