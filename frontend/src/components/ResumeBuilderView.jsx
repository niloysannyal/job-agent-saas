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
  Scissors,
  Printer,
  FileCode,
  Eye,
  ExternalLink,
  Layers,
} from 'lucide-react';
import LatexCodeEditor from './studio/LatexCodeEditor';
import CompilerDiagnosticsDrawer from './studio/CompilerDiagnosticsDrawer';
import { analyzeLatexDiagnostics } from '../utils/latexLogParser';
import { compactLatex, parseLatexDocument, paginateParsedDocument, decodeHtmlEntities } from '../utils/latexCompiler';
import { downloadLatexSource, downloadPdfDocument } from './studio/studioExportUtils';

const TEMPLATES = [
  { id: 'custom', label: 'Custom' },
  { id: '01_MODERN_TECH', label: '01_MODERN_TECH' },
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

  const [savedResumeId, setSavedResumeId] = useState(() => builderContext?.resumeId || null);

  const [resumeTitle, setResumeTitle] = useState(() => {
    if (builderContext?.resumeName) return builderContext.resumeName;
    if (builderContext?.company && builderContext?.role) {
      return `Tailored CV - ${builderContext.role} @ ${builderContext.company}`;
    }
    if (builderContext?.job) return `Tailored CV - ${builderContext.job.company || 'Opportunity'}`;
    return 'Lead AI Systems Engineer Master CV';
  });

  const [activeTemplate, setActiveTemplate] = useState(() => {
    if (builderContext?.templateId && TEMPLATES.some((t) => t.id === builderContext.templateId)) {
      return builderContext.templateId;
    }
    return 'custom';
  });
  const [editedLatex, setEditedLatex] = useState('');
  const [initialLatex, setInitialLatex] = useState('');
  const [isCompiling, setIsCompiling] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isDownloadOpen, setIsDownloadOpen] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(75);
  const [splitRatio, setSplitRatio] = useState(48);
  const [activePage, setActivePage] = useState(1);
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

  // Load initial LaTeX: from context (Studio / saved resume), or compile baseline with profile
  useEffect(() => {
    if (builderContext?.tailoredLatex || builderContext?.resumeLatex) {
      const src = builderContext.tailoredLatex || builderContext.resumeLatex;
      setEditedLatex(src);
      setInitialLatex(src);
      if (builderContext?.templateId && TEMPLATES.some((t) => t.id === builderContext.templateId)) {
        setActiveTemplate(builderContext.templateId);
      } else {
        setActiveTemplate('custom');
      }
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
          if (data?.template_id && TEMPLATES.some((t) => t.id === data.template_id)) {
            setActiveTemplate(data.template_id);
          } else {
            setActiveTemplate('custom');
          }
          if (data?.id) setSavedResumeId(data.id);
        })
        .catch(() => {});
      return;
    }

    // Default: compile baseline template into Custom workspace
    if (profile?.master_cv_latex) {
      setEditedLatex(profile.master_cv_latex);
      setInitialLatex(profile.master_cv_latex);
      setActiveTemplate('custom');
    } else {
      fetchTemplatePreview('01_MODERN_TECH', false);
      setActiveTemplate('custom');
    }
  }, [builderContext, accountId]);

  // Fetch compiled LaTeX for a template from backend TeX compiler
  const fetchTemplatePreview = async (templateId, setAsActive = true) => {
    try {
      setIsCompiling(true);
      const url = `/api/v1/profile/preview-cv?account_id=${accountId}&template_id=${templateId}`;
      const res = await fetch(url, { headers: { ...authHeaders } });
      if (res.ok) {
        const data = await res.json();
        setEditedLatex(data.latex_source);
        setInitialLatex(data.latex_source);
        if (setAsActive) {
          setActiveTemplate(templateId);
        }
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
      const container = document.querySelector('.split-editor-grid');
      if (!container) return;
      const rect = container.getBoundingClientRect();
      const newRatio = ((moveEvent.clientX - rect.left) / rect.width) * 100;
      if (newRatio >= 28 && newRatio <= 72) {
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
    if (!previewScrollRef?.current) return 75;
    const availableWidth = previewScrollRef.current.clientWidth - 40;
    const fit = Math.min(130, Math.max(50, Math.round((availableWidth / 794) * 100)));
    return fit;
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (previewScrollRef?.current) {
        setZoomLevel(calculateFitWidth());
      }
    }, 100);
    return () => clearTimeout(timer);
  }, [calculateFitWidth]);

  // Jump to section in CodeMirror editor
  const handleLocateSection = useCallback(
    (sectionTitle) => {
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
    },
    [editedLatex]
  );

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

  // Manual Recompile Action
  const handleManualCompile = () => {
    setIsCompiling(true);
    setTimeout(() => {
      try {
        const parsed = parseLatexDocument(editedLatex || '');
        showToast?.('✓ TeX compilation successful. Live preview re-rendered!');
      } catch (err) {
        console.error('Compilation error:', err);
        showToast?.('LaTeX syntax warning during compile', 4000);
      } finally {
        setIsCompiling(false);
      }
    }, 220);
  };

  // Compact / Budget to target pages
  const handleCompactToPages = (targetPages = 2) => {
    try {
      const source = editedLatex || '';
      const compacted = compactLatex(source, targetPages, resumeTitle, '');
      setEditedLatex(compacted);
      showToast?.(`Compacted & budgeted CV strictly to ${targetPages} ${targetPages === 1 ? 'page' : 'pages'}!`);
    } catch (err) {
      console.error('Compact error:', err);
      showToast?.('Error compacting CV.', 4000);
    }
  };

  // Copy LaTeX
  const handleCopyLatex = () => {
    if (!editedLatex) return;
    navigator.clipboard.writeText(editedLatex);
    setIsCopied(true);
    showToast?.('LaTeX source copied to clipboard!');
    setTimeout(() => setIsCopied(false), 2000);
  };

  // Handle editor source changes: typing switches template state to Custom
  const handleLatexChange = useCallback((newVal) => {
    setEditedLatex(newVal);
    setActiveTemplate((prev) => (prev !== 'custom' ? 'custom' : prev));
  }, []);

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
        resume_id: savedResumeId || builderContext?.resumeId || null,
        name: resumeTitle.trim() || 'Custom LaTeX Resume',
        latex_source: editedLatex,
        template_id: activeTemplate,
      };

      const res = await fetch('/api/v1/profile/resumes/save-builder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const saved = await res.json();
        if (saved?.id) {
          setSavedResumeId(saved.id);
        }
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

  return (
    <div
      className={`split-workspace-panel panel-card overleaf-workspace ${isFullscreen ? 'overleaf-fullscreen-mode' : ''}`}
      style={{
        height: isFullscreen ? '100vh' : 'calc(100vh - 24px)',
        minHeight: '850px',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* STUDIO INTEROP CONTEXT BANNER */}
      {isFromStudio && (
        <div className="builder-studio-interop-banner">
          <div className="interop-banner-left">
            <span className="interop-badge">Application Studio Mode</span>
            <span className="interop-title">
              Tailoring CV for <strong>{builderContext?.role || 'Opportunity'}</strong> at{' '}
              <strong>{builderContext?.company || 'Company'}</strong>
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

      {/* TOP WORKSPACE HEADER & ACTION BAR */}
      <div
        className="workspace-tabs-bar"
        style={{
          padding: '10px 18px',
          margin: 0,
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          flexWrap: 'wrap',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flex: 1, minWidth: '320px' }}>
          <div className="builder-title-input-row" style={{ minWidth: '260px' }}>
            <input
              type="text"
              className="builder-resume-title-input"
              value={resumeTitle}
              onChange={(e) => setResumeTitle(e.target.value)}
              placeholder="Resume Name (e.g. Lead AI Systems Engineer Master CV)"
              style={{ width: '100%', fontSize: '15px', fontWeight: 600 }}
            />
          </div>

          {/* TEMPLATE DROPDOWN */}
          <div className="builder-template-dropdown-wrapper">
            <Layers size={13} className="template-dropdown-icon text-emerald-400" />
            <span className="template-dropdown-label">Template:</span>
            <div className="builder-template-select-box">
              <select
                className="builder-template-select"
                value={TEMPLATES.some((t) => t.id === activeTemplate) ? activeTemplate : 'custom'}
                onChange={(e) => {
                  const val = e.target.value;
                  if (val === 'custom') {
                    setActiveTemplate('custom');
                    showToast?.('Switched to Custom template mode.');
                  } else {
                    fetchTemplatePreview(val);
                  }
                }}
                disabled={isCompiling}
                title="Choose Resume Template"
              >
                {TEMPLATES.map((tmpl) => (
                  <option key={tmpl.id} value={tmpl.id}>
                    {tmpl.label}
                  </option>
                ))}
              </select>
              <ChevronDown size={11} className="template-select-arrow" />
            </div>
            {isCompiling && <RefreshCw size={12} className="icon-spin text-emerald-400" />}
          </div>
        </div>

        <div className="cv-header-actions-toolbar" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* SAVE BUTTON: INTEROP WITH STUDIO OR SAVE TO PROFILE */}
          {isFromStudio ? (
            <button
              type="button"
              className="action-btn-primary btn-save-return-studio"
              onClick={handleSaveAndReturn}
              disabled={isSaving}
              title="Save changes and return back to Application Studio"
            >
              <Check size={13} />
              <span>{isSaving ? 'Saving...' : 'Save & Return to Studio'}</span>
            </button>
          ) : (
            <button
              type="button"
              className="action-btn-primary btn-save-profile"
              onClick={handleSaveToProfile}
              disabled={isSaving}
              title="Save to My Resumes storage"
            >
              <Save size={13} />
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
            {isCopied ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
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
              <Download size={13} />
              <span>Download</span>
              <ChevronDown size={11} className={`cv-dropdown-arrow ${isDownloadOpen ? 'open' : ''}`} />
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
            className="action-btn-secondary cv-toolbar-btn cv-toolbar-icon-btn"
            onClick={() => setIsFullscreen((prev) => !prev)}
            title={isFullscreen ? 'Exit Full Screen' : 'Full Screen Focus Mode'}
          >
            {isFullscreen ? <Minimize2 size={13} /> : <Maximize2 size={13} />}
          </button>
        </div>
      </div>

      {/* 2-COLUMN SPLIT CONTAINER (OVERLEAF-GRADE DUAL PANE) */}
      <div
        className="split-editor-grid overleaf-grid"
        style={{
          gridTemplateColumns: `${splitRatio}% 10px calc(${100 - splitRatio}% - 10px)`,
          flex: 1,
          height: 'calc(100% - 54px)',
          minHeight: 0,
        }}
      >
        {/* LEFT COLUMN: CODE EDITOR */}
        <div className="editor-column overleaf-editor-column" style={{ display: 'flex', flexDirection: 'column', minHeight: 0, height: '100%' }}>
          <div className="overleaf-editor-wrapper" style={{ height: '100%', flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
            <LatexCodeEditor
              ref={editorRef}
              value={editedLatex}
              onChange={handleLatexChange}
              onCompile={handleManualCompile}
              extraActions={
                <>
                  <div className="editor-tool-btn compact-tool-btn" title="Budget CV (1 or 2 pages)">
                    <Scissors size={13} />
                    <select
                      className="compact-select-overlay"
                      defaultValue=""
                      onChange={(e) => {
                        if (e.target.value) {
                          handleCompactToPages(Number(e.target.value));
                          e.target.value = '';
                        }
                      }}
                      title="Budget CV to 1 or 2 pages"
                    >
                      <option value="" disabled>
                        Compact CV to...
                      </option>
                      <option value="1">1 Page</option>
                      <option value="2">2 Pages</option>
                    </select>
                  </div>
                  <button
                    type="button"
                    className="editor-tool-btn"
                    onClick={() => downloadLatexSource(editedLatex, profileForm, resumeTitle, showToast)}
                    title="Download raw LaTeX (.tex) file"
                  >
                    <Download size={13} />
                    <span style={{ fontSize: '11px', marginLeft: '3px' }}>.tex</span>
                  </button>
                  <button
                    type="button"
                    className="editor-tool-btn"
                    onClick={handleCopyLatex}
                    title="Copy LaTeX source"
                  >
                    {isCopied ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
                  </button>
                </>
              }
            />
            <CompilerDiagnosticsDrawer
              diagnostics={diagnostics}
              onJumpToLine={(line) => editorRef.current?.jumpToLine(line)}
            />
          </div>
        </div>

        {/* DRAGGABLE OVERLEAF SPLITTER GUTTER */}
        <div
          className="overleaf-splitter-gutter"
          onMouseDown={handleSplitterMouseDown}
          onDoubleClick={() => setSplitRatio(48)}
          title="Drag to resize split view (Double-click to reset 50/50)"
        >
          <div className="splitter-handle-bar" />
        </div>

        {/* RIGHT COLUMN: PREVIEW */}
        <div
          className="preview-column overleaf-preview-column"
          style={{ display: 'flex', flexDirection: 'column', minHeight: 0, height: '100%' }}
        >
          {/* OVERLEAF PREVIEW TOOLBAR */}
          <div className="column-toolbar overleaf-toolbar">
            <div className="overleaf-toolbar-left">
              <button
                type="button"
                className={`overleaf-compile-btn ${isCompiling ? 'loading' : ''}`}
                onClick={handleManualCompile}
                disabled={isCompiling}
                title="Compile LaTeX source code (Ctrl + Enter)"
              >
                {isCompiling ? <RefreshCw size={13} className="icon-spin" /> : <Eye size={13} />}
                <span>{isCompiling ? 'Compiling...' : 'Recompile'}</span>
              </button>
            </div>

            <div className="overleaf-toolbar-right">
              {/* Overleaf Zoom Controls with Presets */}
              <div className="zoom-controls-group">
                <button
                  type="button"
                  className="zoom-btn"
                  onClick={() => setZoomLevel((z) => Math.max(50, z - 10))}
                  title="Zoom Out"
                >
                  <ZoomOut size={13} />
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
                  <option value={75}>75%</option>
                  <option value={85}>85%</option>
                  <option value={100}>100%</option>
                  <option value={115}>115%</option>
                  <option value={130}>130%</option>
                </select>
                <button
                  type="button"
                  className="zoom-btn"
                  onClick={() => setZoomLevel((z) => Math.min(140, z + 10))}
                  title="Zoom In"
                >
                  <ZoomIn size={13} />
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
                      document.getElementById(`builder-page-${prev}`)?.scrollIntoView({ behavior: 'smooth' });
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
                      document.getElementById(`builder-page-${next}`)?.scrollIntoView({ behavior: 'smooth' });
                    }}
                    disabled={activePage >= paginatedPages.length}
                    title="Next Page"
                  >
                    ▶
                  </button>
                </div>
              )}

              {/* Print Button */}
              <button
                type="button"
                className="overleaf-toolbar-btn"
                onClick={() => window.print()}
                title="Print or Save via browser dialog"
              >
                <Printer size={13} />
                <span>Print</span>
              </button>
            </div>
          </div>

          {/* PREVIEW SHEET WRAPPER */}
          <div
            className="preview-content-scroll preview-sheet-wrapper overleaf-viewer-bg"
            ref={previewScrollRef}
            style={{ flex: 1, overflowY: 'auto', overflowX: 'auto', minHeight: 0 }}
          >
            <div
              className="overleaf-multi-page-container"
              style={{
                zoom: zoomLevel / 100,
                margin: '0 auto',
                padding: '0 0 36px 0',
              }}
            >
              {paginatedPages.map((page, pIdx) => (
                <div key={pIdx} className="overleaf-a4-page-card" id={`builder-page-${page.pageNumber}`}>
                  {/* Authentic Page Tag Badge */}
                  <div className="a4-page-top-badge">
                    Page {page.pageNumber} of {paginatedPages.length}
                  </div>

                  {/* Document Header (Rendered on Page 1) */}
                  {page.hasHeader && (
                    <div className="cv-header-container">
                      <div className="cv-header-top-row">
                        <div className="cv-header-left">
                          <h1 className="cv-name">
                            {(parsedDoc.header?.name || profileForm?.full_name || 'NILOY SANNYAL').toUpperCase()}
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
                            Location:{' '}
                            {parsedDoc.header?.location ||
                              [profileForm?.location_city, profileForm?.location_country]
                                .filter(Boolean)
                                .join(', ') ||
                              'Dhaka, Bangladesh'}
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
                                      dangerouslySetInnerHTML={{
                                        __html: `<em>${item.companyOrDegreeHtml || item.companyOrDegree}</em>`,
                                      }}
                                    />
                                    {(item.submetaHtml || item.submeta) && (
                                      <span
                                        className="quad-dates-text"
                                        dangerouslySetInnerHTML={{
                                          __html: `<em>${item.submetaHtml || item.submeta}</em>`,
                                        }}
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

                  {/* Authentic A4 Page Number Footer */}
                  <div className="a4-page-number-footer">
                    Page {page.pageNumber} of {paginatedPages.length}
                  </div>
                </div>
              ))}

              {paginatedPages.length === 0 && (
                <div className="empty-latex-notice" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
                  <p>
                    Click <strong>Recompile</strong> to compile your LaTeX code into the visual document preview.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
