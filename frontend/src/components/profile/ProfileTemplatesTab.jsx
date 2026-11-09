import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import {
  Check,
  Copy,
  Layout,
  Columns,
  RefreshCw,
  Download,
  ChevronDown,
  FileText,
  FileCode,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Minimize2,
  Eye,
} from 'lucide-react';
import LatexCodeEditor from '../studio/LatexCodeEditor';
import CompilerDiagnosticsDrawer from '../studio/CompilerDiagnosticsDrawer';
import { analyzeLatexDiagnostics } from '../../utils/latexLogParser';

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
  handleDownloadPdf,
  parsedDoc,
  paginatedPages = [],
  profileForm,
}) {
  const [isDownloadOpen, setIsDownloadOpen] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(70);
  const [activePage, setActivePage] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [splitRatio, setSplitRatio] = useState(48);
  const isDraggingSplitter = useRef(false);
  const downloadRef = useRef(null);
  const editorRef = useRef(null);
  const previewScrollRef = useRef(null);

  const handleSplitterMouseDown = useCallback((e) => {
    e.preventDefault();
    isDraggingSplitter.current = true;
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';

    const handleMouseMove = (moveEvent) => {
      if (!isDraggingSplitter.current) return;
      const container = document.querySelector('.cv-preview-split-layout');
      if (!container) return;
      const rect = container.getBoundingClientRect();
      const newRatio = ((moveEvent.clientX - rect.left) / rect.width) * 100;
      if (newRatio >= 25 && newRatio <= 75) {
        setSplitRatio(Math.round(newRatio));
      }
    };

    const handleMouseUp = () => {
      isDraggingSplitter.current = false;
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  }, []);

  // Auto calculate fit width based on container width
  const calculateFitWidth = useCallback(() => {
    if (!previewScrollRef.current) return 70;
    const availableWidth = previewScrollRef.current.clientWidth - 48;
    const fit = Math.min(130, Math.max(50, Math.round((availableWidth / 794) * 100)));
    return fit;
  }, []);

  useEffect(() => {
    if (previewMode === 'split') {
      const timer = setTimeout(() => {
        setZoomLevel(calculateFitWidth());
      }, 50);
      return () => clearTimeout(timer);
    } else {
      setZoomLevel(100);
    }
  }, [previewMode, calculateFitWidth]);

  const diagnostics = useMemo(() => {
    return analyzeLatexDiagnostics({
      latexSource: editedLatex || previewLatex || '',
      targetPages: 2,
      actualPages: paginatedPages.length,
    });
  }, [editedLatex, previewLatex, paginatedPages.length]);

  // Click to locate section in editor
  const handleLocateSection = (sectionTitle) => {
    if (!sectionTitle || !editorRef.current) return;
    const source = editedLatex || previewLatex || '';
    const lines = source.split(/\r?\n/);
    const searchTarget = sectionTitle.toLowerCase().trim();
    const lineIdx = lines.findIndex((l) =>
      l.toLowerCase().includes(`\\section{${searchTarget}}`) ||
      l.toLowerCase().includes(searchTarget)
    );
    if (lineIdx >= 0) {
      editorRef.current.jumpToLine(lineIdx + 1);
    }
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (downloadRef.current && !downloadRef.current.contains(event.target)) {
        setIsDownloadOpen(false);
      }
    };
    if (isDownloadOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDownloadOpen]);

  const isTemplateActive = (tmplId) => {
    if (!previewTemplateName) return tmplId === '01_MODERN_TECH';
    return (
      previewTemplateName === tmplId ||
      previewTemplateName.toLowerCase() === tmplId.toLowerCase() ||
      previewTemplateName.includes(tmplId)
    );
  };
  const renderA4Pages = () => {
    return (
      <div
        className="overleaf-multi-page-container"
        style={{
          zoom: zoomLevel / 100,
          margin: '0 auto',
        }}
      >
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
            {page.sections.map((sec, secIdx) => {
              const cleanTitle = (sec.title || '').replace(/\s*\((?:cont\.?|continued)\)/gi, '').trim();
              const showTitle = Boolean(cleanTitle && !sec.isContinuation);
              return (
                <div key={secIdx} className="cv-section-container">
                  {showTitle && (
                    <div
                      className="cv-section-title-wrap cv-locateable-section"
                      onDoubleClick={() => handleLocateSection(cleanTitle)}
                      title="Double-click to locate section in LaTeX editor"
                    >
                      <h3 className="cv-section-heading">{cleanTitle}</h3>
                      <div className="cv-section-rule" />
                    </div>
                  )}

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
            );
          })}

            {/* A4 Page Number Footer */}
            <div className="a4-page-number-footer">Page {page.pageNumber} of {paginatedPages.length}</div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className={`panel-card cv-template-panel-card ${isFullscreen ? 'overleaf-fullscreen-mode' : ''}`}>
      <div className="panel-header cv-panel-header">
        <div className="panel-header-title-box">
          <h3 className="cv-panel-title">CV Template &amp; Preview</h3>
          <p className="subtext cv-panel-subtext">
            Compiled Overleaf LaTeX preview with dual-format export.
          </p>
        </div>

        <div className="cv-header-actions-toolbar">
          {/* View Mode Segmented Control */}
          <div className="cv-segmented-group" role="tablist" aria-label="Preview Mode">
            <button
              type="button"
              className={`cv-segmented-btn ${previewMode === 'preview' ? 'active' : ''}`}
              onClick={() => setPreviewMode('preview')}
              title="Full Page A4 Preview"
            >
              <Layout size={14} />
              <span>Full Preview</span>
            </button>
            <button
              type="button"
              className={`cv-segmented-btn ${previewMode === 'split' ? 'active' : ''}`}
              onClick={() => setPreviewMode('split')}
              title="Edit LaTeX & View Side-by-Side"
            >
              <Columns size={14} />
              <span>Split View</span>
            </button>
          </div>

          <div className="cv-toolbar-divider" />

          {/* Copy LaTeX button */}
          <button
            type="button"
            className="action-btn-secondary cv-toolbar-btn"
            onClick={handleCopyLatex}
            disabled={!previewLatex && !editedLatex}
            title="Copy full LaTeX source to clipboard"
          >
            {isCopied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
            <span>{isCopied ? 'Copied!' : 'Copy LaTeX'}</span>
          </button>

          {/* Download Dropdown */}
          <div className="cv-download-dropdown-wrapper" ref={downloadRef}>
            <button
              type="button"
              className="action-btn-primary cv-download-btn"
              onClick={() => setIsDownloadOpen((prev) => !prev)}
              disabled={!previewLatex && !editedLatex}
              aria-haspopup="true"
              aria-expanded={isDownloadOpen}
              title="Download CV as PDF or LaTeX"
            >
              <Download size={14} />
              <span>Download</span>
              <ChevronDown size={13} className={`cv-dropdown-arrow ${isDownloadOpen ? 'open' : ''}`} />
            </button>

            {isDownloadOpen && (
              <div className="cv-download-dropdown-menu">
                <button
                  type="button"
                  className="cv-dropdown-item"
                  onClick={() => {
                    setIsDownloadOpen(false);
                    handleDownloadPdf?.();
                  }}
                >
                  <div className="cv-dropdown-icon-box pdf-badge">
                    <FileText size={15} />
                  </div>
                  <div className="cv-dropdown-text-box">
                    <span className="cv-dropdown-item-title">Download PDF</span>
                    <span className="cv-dropdown-item-desc">Pixel-perfect Overleaf PDF (.pdf)</span>
                  </div>
                </button>

                <button
                  type="button"
                  className="cv-dropdown-item"
                  onClick={() => {
                    setIsDownloadOpen(false);
                    handleDownloadLatex?.();
                  }}
                >
                  <div className="cv-dropdown-icon-box tex-badge">
                    <FileCode size={15} />
                  </div>
                  <div className="cv-dropdown-text-box">
                    <span className="cv-dropdown-item-title">Download LaTeX</span>
                    <span className="cv-dropdown-item-desc">Raw Overleaf TeX file (.tex)</span>
                  </div>
                </button>
              </div>
            )}
          </div>

          {/* Fullscreen Toggle */}
          <button
            type="button"
            className="action-btn-secondary cv-toolbar-btn"
            onClick={() => setIsFullscreen((prev) => !prev)}
            title={isFullscreen ? 'Exit Full Screen' : 'Full Screen Focus Mode'}
          >
            {isFullscreen ? <Minimize2 size={14} /> : <Maximize2 size={14} />}
          </button>
        </div>
      </div>

      {/* Template Switcher Buttons */}
      <div className="template-pills-row cv-template-pills-row">
        <span className="pills-label">Active Template:</span>
        {[
          { id: '01_MODERN_TECH', label: '01_MODERN_TECH (Default)' },
          { id: '02_CLASSIC_CORPORATE', label: '02_CLASSIC_CORPORATE' },
          { id: '03_MINIMALIST_COMPACT', label: '03_MINIMALIST_COMPACT' },
        ].map((tmpl) => {
          const isSelected = isTemplateActive(tmpl.id);
          return (
            <button
              key={tmpl.id}
              type="button"
              className={`pill-btn cv-template-pill ${isSelected ? 'active' : ''}`}
              onClick={() => handleFetchPreview(tmpl.id)}
            >
              {isSelected && <Check size={13} className="cv-pill-check-icon text-emerald-400" />}
              <span>{tmpl.label}</span>
            </button>
          );
        })}
      </div>

      {/* DEFAULT MODE: Authentic Full-Page A4 Document Preview */}
      {previewMode === 'preview' && (
        <div className="cv-full-preview-container overleaf-viewer-bg" ref={previewScrollRef}>
          {renderA4Pages()}
        </div>
      )}

      {/* SPLIT MODE: Side-by-Side Editor (Left) + Live Preview (Right) */}
      {previewMode === 'split' && (
        <div
          className="cv-preview-split-layout"
          style={{ gridTemplateColumns: `${splitRatio}% 10px calc(${100 - splitRatio}% - 10px)` }}
        >
          {/* Left Column: Overleaf-Grade Code Editor */}
          <div className="cv-editor-col">
            <LatexCodeEditor
              ref={editorRef}
              value={editedLatex}
              onChange={setEditedLatex}
              onCompile={() => handleFetchPreview()}
              extraActions={
                <>
                  <button
                    type="button"
                    className="editor-tool-btn"
                    onClick={() => setEditedLatex(previewLatex || '')}
                    title="Reset edits to server compiled source"
                  >
                    Reset
                  </button>
                  <button
                    type="button"
                    className="editor-tool-btn"
                    onClick={handleCopyLatex}
                    title="Copy LaTeX source"
                  >
                    {isCopied ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
                  </button>
                  <button
                    type="button"
                    className="editor-tool-btn"
                    onClick={() => setIsFullscreen((prev) => !prev)}
                    title={isFullscreen ? 'Exit Full Screen' : 'Full Screen Focus Mode'}
                  >
                    {isFullscreen ? <Minimize2 size={13} /> : <Maximize2 size={13} />}
                  </button>
                </>
              }
            />
            <CompilerDiagnosticsDrawer
              diagnostics={diagnostics}
              onJumpToLine={(line) => editorRef.current?.jumpToLine(line)}
            />
          </div>

          {/* Draggable Gutter Resizer */}
          <div
            className="overleaf-splitter-gutter"
            onMouseDown={handleSplitterMouseDown}
            onDoubleClick={() => setSplitRatio(50)}
            title="Drag to resize split view (Double-click to reset 50/50)"
          >
            <div className="splitter-handle-bar" />
          </div>

          {/* Right Column: Live Compiled A4 Preview */}
          <div className="cv-preview-col overleaf-preview-column">
            {/* Integrated Overleaf Preview Toolbar */}
            <div className="column-toolbar overleaf-toolbar">
              <div className="overleaf-toolbar-left">
                <button
                  type="button"
                  className={`overleaf-compile-btn ${isLoadingPreview ? 'loading' : ''}`}
                  onClick={() => handleFetchPreview()}
                  disabled={isLoadingPreview}
                  title="Re-compile LaTeX from profile data (Ctrl+Enter)"
                >
                  <RefreshCw size={13} className={isLoadingPreview ? 'icon-spin' : ''} />
                  <span>{isLoadingPreview ? 'Compiling...' : 'Recompile'}</span>
                  <kbd className="overleaf-kbd">Ctrl+↵</kbd>
                </button>
              </div>

              <div className="overleaf-toolbar-right">
                {/* Zoom Controls */}
                <div className="zoom-controls-group">
                  <button
                    type="button"
                    className="zoom-btn"
                    onClick={() => setZoomLevel((z) => Math.max(50, z - 10))}
                    title="Zoom Out"
                  >
                    <ZoomOut size={12} />
                  </button>
                  <select
                    className="zoom-dropdown-select"
                    value={zoomLevel}
                    onChange={(e) => {
                      if (e.target.value === 'fit') {
                        setZoomLevel(calculateFitWidth());
                      } else {
                        setZoomLevel(Number(e.target.value));
                      }
                    }}
                    title="Zoom Preset"
                  >
                    <option value="fit">Fit Width</option>
                    <option value={50}>50%</option>
                    <option value={60}>60%</option>
                    <option value={70}>70%</option>
                    <option value={80}>80%</option>
                    <option value={100}>100%</option>
                    <option value={120}>120%</option>
                  </select>
                  <button
                    type="button"
                    className="zoom-btn"
                    onClick={() => setZoomLevel((z) => Math.min(140, z + 10))}
                    title="Zoom In"
                  >
                    <ZoomIn size={12} />
                  </button>
                </div>

                {/* Page Stepper Navigation */}
                {paginatedPages.length > 1 && (
                  <div className="page-stepper-group">
                    <button
                      type="button"
                      className="page-step-btn"
                      onClick={() => {
                        const prev = Math.max(1, activePage - 1);
                        setActivePage(prev);
                        document.getElementById(`profile-page-${prev}`)?.scrollIntoView({ behavior: 'smooth' });
                      }}
                      disabled={activePage <= 1}
                      title="Previous Page"
                    >
                      ◀
                    </button>
                    <span className="page-step-indicator">
                      Page {activePage} / {paginatedPages.length}
                    </span>
                    <button
                      type="button"
                      className="page-step-btn"
                      onClick={() => {
                        const next = Math.min(paginatedPages.length, activePage + 1);
                        setActivePage(next);
                        document.getElementById(`profile-page-${next}`)?.scrollIntoView({ behavior: 'smooth' });
                      }}
                      disabled={activePage >= paginatedPages.length}
                      title="Next Page"
                    >
                      ▶
                    </button>
                  </div>
                )}

                <button
                  type="button"
                  className="action-btn-xs"
                  onClick={() => setIsFullscreen((prev) => !prev)}
                  title={isFullscreen ? 'Exit Full Screen' : 'Full Screen Focus Mode'}
                >
                  {isFullscreen ? <Minimize2 size={12} /> : <Maximize2 size={12} />}
                </button>
              </div>
            </div>

            <div className="preview-sheet-wrapper overleaf-viewer-bg" ref={previewScrollRef}>
              {renderA4Pages()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

