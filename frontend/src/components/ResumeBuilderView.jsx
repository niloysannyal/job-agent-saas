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
  ExternalLink,
} from 'lucide-react';
import LatexCodeEditor from './studio/LatexCodeEditor';
import CompilerDiagnosticsDrawer from './studio/CompilerDiagnosticsDrawer';
import { analyzeLatexDiagnostics } from '../utils/latexLogParser';
import { parseLatexDocument, paginateParsedDocument } from '../utils/latexCompiler';
import { downloadLatexSource, downloadPdfDocument } from './studio/studioExportUtils';

const TEMPLATES = [
  { id: '01_MODERN_TECH', label: 'Modern Tech (Standard)' },
  { id: '02_MINIMAL_CLASSIC', label: 'Minimal Classic (ATS Core)' },
  { id: '03_EXECUTIVE', label: 'Executive Leadership' },
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
  const [resumeTitle, setResumeTitle] = useState(() => {
    if (builderContext?.resumeName) return builderContext.resumeName;
    if (builderContext?.job) return `Tailored Resume - ${builderContext.job.company || 'Job'}`;
    return 'Lead AI Engineer Master CV';
  });

  const [activeTemplate, setActiveTemplate] = useState('01_MODERN_TECH');
  const [editedLatex, setEditedLatex] = useState('');
  const [initialLatex, setInitialLatex] = useState('');
  const [isCompiling, setIsCompiling] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isDownloadOpen, setIsDownloadOpen] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(75);
  const [splitRatio, setSplitRatio] = useState(48);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const isDraggingSplitter = useRef(false);
  const downloadRef = useRef(null);
  const editorRef = useRef(null);
  const previewScrollRef = useRef(null);

  // Close download dropdown on outside click
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

  // Load initial LaTeX: from context (e.g. from Studio or existing resume), or fetch compiled preview
  useEffect(() => {
    if (builderContext?.resumeLatex) {
      setEditedLatex(builderContext.resumeLatex);
      setInitialLatex(builderContext.resumeLatex);
      return;
    }

    if (builderContext?.resumeId) {
      // Load existing saved resume by ID
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

    // Default: compile from user profile
    fetchTemplatePreview(activeTemplate);
  }, [builderContext, accountId]);

  // Fetch compiled LaTeX for a template
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

  // Draggable Splitter Handlers
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

  // Parse document for visual rendering
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

  // Save to Profile / Saved Resumes
  const handleSaveToProfile = async () => {
    if (!editedLatex.trim()) {
      showToast?.('Cannot save empty resume.');
      return;
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
      showToast?.('Error saving resume to storage.', 4000);
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

  const isReturnToStudio = builderContext?.returnTo === 'studio';

  return (
    <div className={`section-container resume-builder-view ${isFullscreen ? 'builder-fullscreen' : ''}`}>
      {/* TOP HEADER & ACTION BAR */}
      <div className="builder-header-bar">
        <div className="builder-header-left">
          {isReturnToStudio ? (
            <button
              type="button"
              className="btn-back-to-studio"
              onClick={() => onNavigate?.('studio')}
              title="Discard unsaved changes and return to Application Studio"
            >
              <ArrowLeft size={16} />
              <span>Back to Studio</span>
            </button>
          ) : (
            <div className="builder-icon-tag">
              <FileCode size={20} className="text-emerald-400" />
            </div>
          )}

          <div className="builder-title-input-wrap">
            <input
              type="text"
              className="builder-resume-title-input"
              value={resumeTitle}
              onChange={(e) => setResumeTitle(e.target.value)}
              placeholder="Resume Name (e.g. Lead AI Systems Engineer)"
            />
            <span className="builder-subtitle-tag">
              {isReturnToStudio ? 'Tailoring for Application Studio' : 'LaTeX Resume Builder & Compiler'}
            </span>
          </div>
        </div>

        {/* TEMPLATE PICKER PILLS */}
        <div className="builder-template-pills">
          {TEMPLATES.map((tmpl) => {
            const isSelected = activeTemplate === tmpl.id;
            return (
              <button
                key={tmpl.id}
                type="button"
                className={`builder-template-pill ${isSelected ? 'active' : ''}`}
                onClick={() => fetchTemplatePreview(tmpl.id)}
                disabled={isCompiling}
              >
                {isSelected && <Check size={12} className="text-emerald-400" />}
                <span>{tmpl.label}</span>
              </button>
            );
          })}
        </div>

        {/* PRIMARY ACTIONS */}
        <div className="builder-header-actions">
          {isReturnToStudio ? (
            <button
              type="button"
              className="btn-save-return-studio"
              onClick={handleSaveAndReturn}
              disabled={isSaving}
            >
              <Check size={16} />
              <span>{isSaving ? 'Compiling & Saving...' : 'Save & Return to Studio'}</span>
            </button>
          ) : (
            <button
              type="button"
              className="btn-save-resume"
              onClick={handleSaveToProfile}
              disabled={isSaving}
            >
              <Save size={15} />
              <span>{isSaving ? 'Saving...' : 'Save to Profile'}</span>
            </button>
          )}

          {/* DOWNLOAD DROPDOWN */}
          <div className="download-dropdown-container" ref={downloadRef}>
            <button
              type="button"
              className="btn-download-menu"
              onClick={() => setIsDownloadOpen((prev) => !prev)}
            >
              <Download size={14} />
              <span>Export</span>
              <ChevronDown size={13} />
            </button>

            {isDownloadOpen && (
              <div className="export-dropdown-menu">
                <button
                  type="button"
                  className="dropdown-item"
                  onClick={() => {
                    downloadPdfDocument({
                      parsedDoc,
                      customCompany: resumeTitle,
                      profile: profileForm,
                      showToast,
                    });
                    setIsDownloadOpen(false);
                  }}
                >
                  <FileText size={14} className="text-emerald-400" />
                  <span>Download PDF</span>
                </button>
                <button
                  type="button"
                  className="dropdown-item"
                  onClick={() => {
                    downloadLatexSource(editedLatex, profileForm, resumeTitle, showToast);
                    setIsDownloadOpen(false);
                  }}
                >
                  <FileCode size={14} className="text-blue-400" />
                  <span>Download LaTeX (.tex)</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* OVERLEAF-STYLE SPLIT SCREEN WORKSPACE */}
      <div
        className="cv-preview-split-layout builder-split-workspace"
        style={{ gridTemplateColumns: `${splitRatio}% 10px calc(${100 - splitRatio}% - 10px)` }}
      >
        {/* LEFT COLUMN: CODE EDITOR */}
        <div className="cv-editor-col">
          <LatexCodeEditor
            ref={editorRef}
            value={editedLatex}
            onChange={setEditedLatex}
            onCompile={() => showToast?.('LaTeX updated and re-rendered in real-time!')}
            extraActions={
              <>
                <button
                  type="button"
                  className="editor-tool-btn"
                  onClick={() => setEditedLatex(initialLatex)}
                  title="Reset edits to initial source"
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

        {/* SPLITTER GUTTER */}
        <div
          className="overleaf-splitter-gutter"
          onMouseDown={handleSplitterMouseDown}
          onDoubleClick={() => setSplitRatio(50)}
          title="Drag to resize split view (Double-click to reset 50/50)"
        >
          <div className="splitter-handle-bar" />
        </div>

        {/* RIGHT COLUMN: LIVE COMPILED A4 PREVIEW */}
        <div className="cv-preview-col overleaf-preview-column" ref={previewScrollRef}>
          {/* TOOLBAR */}
          <div className="column-toolbar overleaf-toolbar">
            <div className="overleaf-toolbar-left">
              <span className="overleaf-status-tag">
                <Check size={13} className="text-emerald-400" />
                <span>Real-Time Engine</span>
              </span>
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
                <span className="zoom-indicator">{zoomLevel}%</span>
                <button
                  type="button"
                  className="zoom-btn"
                  onClick={() => setZoomLevel((z) => Math.min(130, z + 10))}
                  title="Zoom In"
                >
                  <ZoomIn size={12} />
                </button>
              </div>
            </div>
          </div>

          {/* DISCRETE A4 PAGES VIEWER */}
          <div className="cv-full-preview-container overleaf-viewer-bg">
            <div
              className="overleaf-multi-page-container"
              style={{ zoom: zoomLevel / 100, margin: '0 auto' }}
            >
              {paginatedPages.map((page, pIdx) => (
                <div key={pIdx} className="overleaf-a4-page-card" id={`builder-page-${page.pageNumber}`}>
                  <div className="a4-page-top-badge">
                    Page {page.pageNumber} of {paginatedPages.length}
                  </div>

                  {page.hasHeader && (
                    <div className="cv-header-container">
                      <div className="cv-header-top-row">
                        <div className="cv-header-left">
                          <h1 className="cv-name">
                            {(parsedDoc.header.name || profileForm?.full_name || 'CANDIDATE NAME').toUpperCase()}
                          </h1>
                          <div className="cv-header-links-row">
                            {parsedDoc.header.leftLinks.map((lk, lIdx) => (
                              <React.Fragment key={lIdx}>
                                <a href={lk.url} target="_blank" rel="noopener noreferrer" className="cv-header-link">
                                  {lk.label}
                                </a>
                                {lIdx < parsedDoc.header.leftLinks.length - 1 && <span className="cv-link-pipe">|</span>}
                              </React.Fragment>
                            ))}
                          </div>
                        </div>

                        <div className="cv-header-right">
                          <div className="cv-location-line">
                            Location: {parsedDoc.header.location || [profileForm?.location_city, profileForm?.location_country].filter(Boolean).join(', ') || 'Remote'}
                          </div>
                        </div>
                      </div>
                      <div className="cv-header-divider" />
                    </div>
                  )}

                  {page.sections.map((sec, sIdx) => {
                    const cleanTitle = (sec.title || '').replace(/\s*\((?:cont\.?|continued)\)/gi, '').trim();
                    const showTitle = Boolean(cleanTitle && !sec.isContinuation);
                    return (
                      <div key={sIdx} className="cv-section-container">
                        {showTitle && (
                          <div className="cv-section-title-row">
                            <h2 className="cv-section-title">{cleanTitle.toUpperCase()}</h2>
                            <div className="cv-section-rule" />
                          </div>
                        )}
                        {sec.entries.map((entry, eIdx) => (
                          <div key={eIdx} className="cv-entry-block">
                            <div className="cv-entry-row-1">
                              <span className="cv-entry-bold">{entry.company}</span>
                              <span className="cv-entry-italic">{entry.location}</span>
                            </div>
                            <div className="cv-entry-row-2">
                              <span className="cv-entry-italic">{entry.title}</span>
                              <span className="cv-entry-date">{entry.dates}</span>
                            </div>
                            {entry.bullets.map((b, bIdx) => (
                              <div key={bIdx} className="cv-bullet-item">
                                <span className="cv-bullet-dot">•</span>
                                <span className="cv-bullet-text">{b}</span>
                              </div>
                            ))}
                          </div>
                        ))}
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
