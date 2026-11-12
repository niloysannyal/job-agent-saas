import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import {
  FileText,
  Save,
  ArrowLeft,
  RefreshCw,
  Download,
  Copy,
  Check,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Minimize2,
  ChevronDown,
  Sparkles,
  Layers,
  FileCode,
  Layout,
  Columns,
  Eye,
  ExternalLink,
} from 'lucide-react';
import LatexCodeEditor from './studio/LatexCodeEditor';
import CompilerDiagnosticsDrawer from './studio/CompilerDiagnosticsDrawer';
import { analyzeLatexDiagnostics } from '../utils/latexLogParser';
import { parseLatexDocument, paginateParsedDocument } from '../utils/latexCompiler';
import { downloadLatexSource, downloadPdfDocument } from './studio/studioExportUtils';

const TEMPLATES = [
  { id: '01_MODERN_TECH', label: '01_MODERN_TECH (Default)' },
  { id: '02_CLASSIC_CORPORATE', label: '02_CLASSIC_CORPORATE' },
  { id: '03_MINIMALIST_COMPACT', label: '03_MINIMALIST_COMPACT' },
];

export default function ResumeBuilderView({
  accountId,
  authHeaders = {},
  showToast,
  profile,
  profileForm,
  builderContext = null,
  onNavigate,
  onSaveAndReturn,
}) {
  const isFromStudio = Boolean(builderContext?.fromStudio || builderContext?.returnTo === 'studio');

  const [resumeTitle, setResumeTitle] = useState(() => {
    if (builderContext?.resumeName) return builderContext.resumeName;
    if (builderContext?.company && builderContext?.role) {
      return `Tailored CV - ${builderContext.role} @ ${builderContext.company}`;
    }
    if (builderContext?.job) return `Tailored CV - ${builderContext.job.company || 'Opportunity'}`;
    return 'Lead AI Systems Engineer Master CV';
  });

  const [activeTemplate, setActiveTemplate] = useState('01_MODERN_TECH');
  const [previewMode, setPreviewMode] = useState('split'); // 'preview' | 'split'
  const [editedLatex, setEditedLatex] = useState('');
  const [initialLatex, setInitialLatex] = useState('');
  const [isCompiling, setIsCompiling] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isDownloadOpen, setIsDownloadOpen] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(70);
  const [splitRatio, setSplitRatio] = useState(48);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const isDraggingSplitter = useRef(false);
  const downloadRef = useRef(null);
  const editorRef = useRef(null);
  const previewScrollRef = useRef(null);

  // Close download dropdown on click outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (downloadRef.current && !downloadRef.current.contains(event.target)) {
        setIsDownloadOpen(false);
      }
    }
    if (isDownloadOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDownloadOpen]);

  // Load initial LaTeX: from context (Studio / saved resume), or compile template with profile
  useEffect(() => {
    if (builderContext?.tailoredLatex || builderContext?.resumeLatex) {
      const src = builderContext.tailoredLatex || builderContext.resumeLatex;
      setEditedLatex(src);
      setInitialLatex(src);
      return;
    }

    if (builderContext?.resumeId) {
      fetch(`/api/v1/profile/resumes/${builderContext.resumeId}?account_id=${accountId}`, {
        headers: { ...authHeaders },
      })
        .then((r) => r.ok && r.json())
        .then((data) => {
          if (data?.name) setResumeTitle(data.name);
          if (data?.latex_source) {
            setEditedLatex(data.latex_source);
            setInitialLatex(data.latex_source);
          }
        })
        .catch(() => {});
      return;
    }

    // Default: compile from candidate profile
    fetchTemplatePreview(activeTemplate);
  }, [builderContext, accountId]);

  // Fetch compiled LaTeX for a template from backend TeX compiler
  const fetchTemplatePreview = async (templateId) => {
    try {
      setIsCompiling(true);
      const url = `/api/v1/profile/preview-cv?account_id=${accountId}&template_id=${templateId}`;
      const res = await fetch(url, { headers: { ...authHeaders } });
      if (res.ok) {
        const data = await res.json();
        setEditedLatex(data.latex_source);
        setInitialLatex(data.latex_source);
        setActiveTemplate(templateId);
        showToast?.(`Loaded ${templateId} with profile data.`);
      }
    } catch {
      showToast?.('Failed to compile template with profile.');
    } finally {
      setIsCompiling(false);
    }
  };

  // Draggable Splitter
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

  // Auto calculate fit zoom width
  const calculateFitWidth = useCallback(() => {
    if (!previewScrollRef.current) return 70;
    const availableWidth = previewScrollRef.current.clientWidth - 48;
    return Math.min(130, Math.max(50, Math.round((availableWidth / 794) * 100)));
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

  // Jump to section in CodeMirror editor
  const handleLocateSection = (sectionTitle) => {
    if (!sectionTitle || !editorRef.current) return;
    const source = editedLatex || '';
    const lines = source.split(/\r?\n/);
    const target = sectionTitle.toLowerCase().trim();
    const lineIdx = lines.findIndex(
      (l) => l.toLowerCase().includes(`\\section{${target}}`) || l.toLowerCase().includes(target)
    );
    if (lineIdx >= 0) {
      editorRef.current.jumpToLine(lineIdx + 1);
    }
  };

  // Parsed AST & Paginated Pages
  const parsedDoc = useMemo(() => {
    if (!editedLatex) return parseLatexDocument('');
    return parseLatexDocument(editedLatex);
  }, [editedLatex]);

  const paginatedPages = useMemo(() => {
    return paginateParsedDocument(parsedDoc, 770);
  }, [parsedDoc]);

  const diagnostics = useMemo(() => {
    return analyzeLatexDiagnostics({
      latexSource: editedLatex || '',
      targetPages: 2,
      actualPages: paginatedPages.length,
    });
  }, [editedLatex, paginatedPages.length]);

  // Copy LaTeX
  const handleCopyLatex = () => {
    if (!editedLatex) return;
    navigator.clipboard.writeText(editedLatex);
    setIsCopied(true);
    showToast?.('LaTeX source copied to clipboard!');
    setTimeout(() => setIsCopied(false), 2000);
  };

  // Save to Profile Keeper (user_resumes)
  const handleSaveToProfile = async () => {
    if (!editedLatex.trim()) {
      showToast?.('Cannot save empty resume.');
      return null;
    }
    try {
      setIsSaving(true);
      const payload = {
        account_id: accountId,
        resume_id: builderContext?.resumeId || null,
        name: resumeTitle.trim() || 'Custom LaTeX Resume',
        latex_source: editedLatex,
      };

      const res = await fetch('/api/v1/profile/resumes/save-builder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const saved = await res.json();
        showToast?.(`Saved "${saved.name}" to My Resumes!`);
        return saved;
      } else {
        const err = await res.json();
        showToast?.(err.detail || 'Failed to save resume.', 4000);
        return null;
      }
    } catch {
      showToast?.('Error saving resume to profile keeper.', 4000);
      return null;
    } finally {
      setIsSaving(false);
    }
  };

  // Save & Return to Application Studio
  const handleSaveAndReturn = async () => {
    const saved = await handleSaveToProfile();
    if (onSaveAndReturn) {
      onSaveAndReturn({
        latex: editedLatex,
        name: resumeTitle,
        resumeId: saved?.id,
      });
    }
    onNavigate?.('studio');
  };

  // Render Visual A4 Pages
  const renderVisualA4Pages = () => {
    return (
      <div className="overleaf-pages-column" style={{ zoom: zoomLevel / 100, margin: '0 auto' }}>
        {paginatedPages.map((page, pIdx) => (
          <div key={pIdx} className="overleaf-a4-page-card" id={`builder-page-${page.pageNumber}`}>
            <div className="a4-page-top-badge">Page {page.pageNumber} of {paginatedPages.length}</div>

            {/* Document Header (Page 1) */}
            {page.hasHeader && (
              <div className="cv-header-container">
                <div className="cv-header-top-row">
                  <div className="cv-header-left">
                    <h1 className="cv-name">
                      {(parsedDoc.header?.name || profileForm?.full_name || 'CANDIDATE NAME').toUpperCase()}
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
                      Location: {parsedDoc.header?.location || [profileForm?.location_city, profileForm?.location_country].filter(Boolean).join(', ') || 'Remote / Worldwide'}
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
    );
  };

  return (
    <div className={`panel-card cv-template-panel-card ${isFullscreen ? 'overleaf-fullscreen-mode' : ''}`}>
      {/* STUDIO INTEROP CONTEXT BANNER */}
      {isFromStudio && (
        <div className="builder-studio-interop-banner">
          <div className="interop-banner-left">
            <span className="interop-badge">Application Studio Mode</span>
            <span className="interop-title">
              Tailoring CV for <strong>{builderContext?.role || 'Opportunity'}</strong> at <strong>{builderContext?.company || 'Company'}</strong>
            </span>
          </div>
          <button
            type="button"
            className="action-btn-secondary interop-back-btn"
            onClick={() => onNavigate?.('studio')}
            title="Discard changes and return to Application Studio"
          >
            <ArrowLeft size={14} />
            <span>Discard &amp; Return to Studio</span>
          </button>
        </div>
      )}

      {/* TOP HEADER & ACTION BAR */}
      <div className="panel-header cv-panel-header">
        <div className="panel-header-title-box">
          <div className="builder-title-input-row">
            <input
              type="text"
              className="builder-resume-title-input"
              value={resumeTitle}
              onChange={(e) => setResumeTitle(e.target.value)}
              placeholder="Resume Name (e.g. Lead AI Systems Engineer Master CV)"
            />
          </div>
          <p className="subtext cv-panel-subtext">
            Overleaf-grade LaTeX Resume Builder with dual-format export and TeX Live compiler.
          </p>
        </div>

        <div className="cv-header-actions-toolbar">
          {/* VIEW MODE SEGMENTED CONTROL */}
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

          {/* SAVE BUTTON: INTEROP WITH STUDIO OR SAVE TO PROFILE */}
          {isFromStudio ? (
            <button
              type="button"
              className="action-btn-primary btn-save-return-studio"
              onClick={handleSaveAndReturn}
              disabled={isSaving}
              title="Save changes and return back to Application Studio"
            >
              <Check size={14} />
              <span>{isSaving ? 'Saving...' : 'Save & Return to Studio'}</span>
            </button>
          ) : (
            <button
              type="button"
              className="action-btn-primary"
              onClick={handleSaveToProfile}
              disabled={isSaving}
              title="Save to My Resumes storage"
            >
              <Save size={14} />
              <span>{isSaving ? 'Saving...' : 'Save to Profile'}</span>
            </button>
          )}

          {/* COPY LATEX BUTTON */}
          <button
            type="button"
            className="action-btn-secondary cv-toolbar-btn"
            onClick={handleCopyLatex}
            disabled={!editedLatex}
            title="Copy full LaTeX source to clipboard"
          >
            {isCopied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
            <span>{isCopied ? 'Copied!' : 'Copy LaTeX'}</span>
          </button>

          {/* DOWNLOAD DROPDOWN */}
          <div className="cv-download-dropdown-wrapper" ref={downloadRef}>
            <button
              type="button"
              className="action-btn-secondary cv-download-btn"
              onClick={() => setIsDownloadOpen((prev) => !prev)}
              disabled={!editedLatex}
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
                    downloadPdfDocument({
                      parsedDoc,
                      customCompany: resumeTitle,
                      profile: profileForm,
                      showToast,
                    });
                  }}
                >
                  <div className="cv-dropdown-icon-box pdf-badge">
                    <FileText size={15} />
                  </div>
                  <div className="cv-dropdown-text-box">
                    <span className="cv-dropdown-item-title">Download PDF</span>
                    <span className="cv-dropdown-item-desc">Pixel-perfect compiled PDF (.pdf)</span>
                  </div>
                </button>

                <button
                  type="button"
                  className="cv-dropdown-item"
                  onClick={() => {
                    setIsDownloadOpen(false);
                    downloadLatexSource(editedLatex, profileForm, resumeTitle, showToast);
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

          {/* FULLSCREEN TOGGLE */}
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

      {/* TEMPLATE SWITCHER PILLS */}
      <div className="template-pills-row cv-template-pills-row">
        <span className="pills-label">Active Template:</span>
        {TEMPLATES.map((tmpl) => {
          const isSelected = activeTemplate === tmpl.id;
          return (
            <button
              key={tmpl.id}
              type="button"
              className={`pill-btn cv-template-pill ${isSelected ? 'active' : ''}`}
              onClick={() => fetchTemplatePreview(tmpl.id)}
              disabled={isCompiling}
            >
              {isSelected && <Check size={13} className="cv-pill-check-icon text-emerald-400" />}
              <span>{tmpl.label}</span>
            </button>
          );
        })}
      </div>

      {/* MODE 1: FULL PAGE AUTHENTIC A4 PREVIEW */}
      {previewMode === 'preview' && (
        <div className="cv-full-preview-container overleaf-viewer-bg" ref={previewScrollRef}>
          <div className="cv-full-preview-toolbar">
            <div className="engine-status-badge">
              <span className="status-dot-emerald" />
              <span>TeX Live Engine: Clean</span>
            </div>

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
          </div>

          <div className="cv-full-preview-scroll-wrapper">
            {renderVisualA4Pages()}
          </div>
        </div>
      )}

      {/* MODE 2: SPLIT OVERLEAF EDITOR & LIVE A4 PREVIEW */}
      {previewMode === 'split' && (
        <div className="cv-preview-split-layout">
          {/* LEFT: CodeMirror 6 Overleaf Editor */}
          <div className="cv-editor-col" style={{ width: `${splitRatio}%` }}>
            <LatexCodeEditor
              ref={editorRef}
              latexCode={editedLatex}
              onChange={(val) => setEditedLatex(val)}
              onReset={() => {
                setEditedLatex(initialLatex);
                showToast?.('Reset edits to initial source.');
              }}
              onSave={isFromStudio ? handleSaveAndReturn : handleSaveToProfile}
              diagnostics={diagnostics}
            />
          </div>

          {/* DRAGGABLE SPLITTER */}
          <div
            className="cv-split-resizer"
            onMouseDown={handleSplitterMouseDown}
            title="Drag to resize editor and preview panes"
          >
            <div className="resizer-handle-line" />
          </div>

          {/* RIGHT: Live Visual A4 Preview */}
          <div
            className="cv-preview-scroll-pane overleaf-viewer-bg"
            ref={previewScrollRef}
            style={{ width: `calc(${100 - splitRatio}% - 10px)` }}
          >
            <div className="cv-split-preview-header">
              <div className="engine-status-badge">
                <span className="status-dot-emerald" />
                <span>Real-Time Engine</span>
              </div>

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
            </div>

            <div className="cv-split-preview-body">
              {renderVisualA4Pages()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
