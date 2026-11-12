import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  FileText,
  Upload,
  Plus,
  Eye,
  Edit2,
  Trash2,
  Star,
  Download,
  Check,
  X,
  FileCode,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Minimize2,
  AlertCircle,
  Clock,
  Sparkles,
} from 'lucide-react';
import { parseLatexDocument, paginateParsedDocument } from '../../utils/latexCompiler';

export default function SavedResumesTab({
  accountId,
  authHeaders = {},
  showToast,
  onNavigate,
  profileForm,
}) {
  const [resumes, setResumes] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Upload modal state
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadName, setUploadName] = useState('');
  const [uploadIsDefault, setUploadIsDefault] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  // Preview modal state
  const [previewResume, setPreviewResume] = useState(null);
  const [previewData, setPreviewData] = useState(null);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);
  const [previewZoom, setPreviewZoom] = useState(85);

  // Rename inline state
  const [editingId, setEditingId] = useState(null);
  const [editingName, setEditingName] = useState('');

  // Fetch list of resumes
  const fetchResumes = useCallback(async () => {
    if (!accountId) return;
    try {
      setIsLoading(true);
      const res = await fetch(`/api/v1/profile/resumes?account_id=${accountId}`, {
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const data = await res.json();
        setResumes(data.resumes || []);
      }
    } catch (e) {
      console.warn('Failed to fetch resumes:', e);
    } finally {
      setIsLoading(false);
    }
  }, [accountId, authHeaders]);

  useEffect(() => {
    fetchResumes();
  }, [fetchResumes]);

  // Upload Handler
  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!uploadFile) {
      showToast?.('Please select a PDF resume file to upload.');
      return;
    }
    try {
      setIsUploading(true);
      const formData = new FormData();
      formData.append('file', uploadFile);
      if (uploadName.trim()) {
        formData.append('name', uploadName.trim());
      }
      formData.append('is_default', String(uploadIsDefault));
      formData.append('account_id', accountId);

      const res = await fetch('/api/v1/profile/resumes/upload', {
        method: 'POST',
        headers: { ...authHeaders },
        body: formData,
      });

      if (res.ok) {
        showToast?.('Resume uploaded and verified successfully!');
        setIsUploadOpen(false);
        setUploadFile(null);
        setUploadName('');
        setUploadIsDefault(false);
        fetchResumes();
      } else {
        const err = await res.json();
        showToast?.(err.detail || 'Failed to upload resume.', 4000);
      }
    } catch (err) {
      showToast?.('Network error during upload.', 4000);
    } finally {
      setIsUploading(false);
    }
  };

  // Set as Default
  const handleSetDefault = async (resumeId) => {
    try {
      const res = await fetch(`/api/v1/profile/resumes/${resumeId}/default?account_id=${accountId}`, {
        method: 'PUT',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast?.('Default resume updated. Match scoring will now prioritize this resume.');
        fetchResumes();
      } else {
        showToast?.('Failed to update default resume.');
      }
    } catch {
      showToast?.('Network error updating default resume.');
    }
  };

  // Delete Resume
  const handleDelete = async (resumeId, name) => {
    if (!confirm(`Are you sure you want to delete "${name}"?`)) return;
    try {
      const res = await fetch(`/api/v1/profile/resumes/${resumeId}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast?.('Resume removed from storage.');
        fetchResumes();
      } else {
        showToast?.('Failed to delete resume.');
      }
    } catch {
      showToast?.('Network error deleting resume.');
    }
  };

  // Open Preview Modal
  const handleOpenPreview = async (resume) => {
    setPreviewResume(resume);
    setPreviewData(null);
    setIsLoadingDetails(true);
    try {
      const res = await fetch(`/api/v1/profile/resumes/${resume.id}?account_id=${accountId}`, {
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const fullData = await res.json();
        setPreviewData(fullData);
      }
    } catch {
      showToast?.('Failed to load full resume preview.');
    } finally {
      setIsLoadingDetails(false);
    }
  };

  // Format file size
  const formatBytes = (bytes) => {
    if (!bytes || bytes === 0) return '0 KB';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  // Parse LaTeX for discrete A4 preview if builder source
  const parsedDoc = useMemo(() => {
    if (!previewData?.latex_source) return parseLatexDocument('');
    return parseLatexDocument(previewData.latex_source);
  }, [previewData?.latex_source]);

  const paginatedPages = useMemo(() => {
    return paginateParsedDocument(parsedDoc, 770);
  }, [parsedDoc]);

  return (
    <div className="saved-resumes-container">
      {/* HEADER SECTION */}
      <div className="saved-resumes-header">
        <div className="saved-resumes-title-group">
          <div className="saved-resumes-icon-badge">
            <FileText size={22} className="text-emerald-400" />
          </div>
          <div>
            <h2 className="saved-resumes-title">CV & Resume Keeper</h2>
            <p className="saved-resumes-subtitle">
              Manage your verified resumes (up to 5). Your default resume guides autonomous vector matching and outreach generation.
            </p>
          </div>
        </div>

        <div className="saved-resumes-actions-group">
          <div className="resumes-quota-pill">
            <span className="quota-number">{resumes.length} / 5</span>
            <span className="quota-label">Resumes Saved</span>
          </div>

          <button
            type="button"
            className="btn-upload-resume"
            onClick={() => setIsUploadOpen(true)}
            disabled={resumes.length >= 5}
            title={resumes.length >= 5 ? 'Maximum limit of 5 resumes reached' : 'Upload readymade PDF resume'}
          >
            <Upload size={15} />
            <span>Upload Resume</span>
          </button>

          <button
            type="button"
            className="btn-build-resume"
            onClick={() => onNavigate?.('builder')}
            title="Open Resume Builder to edit or create LaTeX resumes"
          >
            <Plus size={15} />
            <span>Build Resume</span>
          </button>
        </div>
      </div>

      {/* RESUMES LIST / EMPTY STATE */}
      {isLoading ? (
        <div className="resumes-loading-state">
          <div className="loading-spinner" />
          <span>Loading your saved resumes...</span>
        </div>
      ) : resumes.length === 0 ? (
        <div className="resumes-empty-card">
          <div className="empty-icon-circle">
            <FileText size={32} className="text-slate-400" />
          </div>
          <h3>No Resumes Saved Yet</h3>
          <p>
            Upload a readymade PDF resume or craft a tailored resume using our LaTeX Resume Builder.
            Your default resume automatically powers AI job match scoring.
          </p>
          <div className="empty-action-buttons">
            <button
              type="button"
              className="btn-upload-resume"
              onClick={() => setIsUploadOpen(true)}
            >
              <Upload size={15} />
              <span>Upload PDF Resume</span>
            </button>
            <button
              type="button"
              className="btn-build-resume"
              onClick={() => onNavigate?.('builder')}
            >
              <FileCode size={15} />
              <span>Build with LaTeX</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="saved-resumes-grid">
          {resumes.map((resume) => {
            const isDef = Boolean(resume.is_default);
            return (
              <div
                key={resume.id}
                className={`resume-card ${isDef ? 'default-active' : ''}`}
              >
                {/* DEFAULT BADGE OR PROMOTION */}
                <div className="resume-card-top-bar">
                  {isDef ? (
                    <span className="badge-default-active">
                      <Star size={12} className="fill-emerald-400 text-emerald-400" />
                      <span>Default Resume</span>
                    </span>
                  ) : (
                    <button
                      type="button"
                      className="btn-make-default"
                      onClick={() => handleSetDefault(resume.id)}
                      title="Set as Default for AI Match Scoring and Outreach"
                    >
                      <Star size={12} />
                      <span>Set as Default</span>
                    </button>
                  )}

                  <span className={`badge-source-type ${resume.source_type}`}>
                    {resume.source_type === 'builder' ? 'LaTeX Builder' : 'Uploaded PDF'}
                  </span>
                </div>

                {/* CARD BODY */}
                <div className="resume-card-body">
                  <div className="resume-card-title-row">
                    <FileText size={20} className="resume-type-icon" />
                    <div className="resume-names">
                      <h3 className="resume-display-name" title={resume.name}>
                        {resume.name}
                      </h3>
                      <span className="resume-filename" title={resume.filename}>
                        {resume.filename}
                      </span>
                    </div>
                  </div>

                  {/* METADATA CHIPS */}
                  <div className="resume-metadata-chips">
                    <span className="meta-chip">
                      {resume.page_count} {resume.page_count === 1 ? 'Page' : 'Pages'}
                    </span>
                    <span className="meta-chip">{formatBytes(resume.file_size_bytes)}</span>
                    <span className="meta-chip">
                      <Clock size={11} />
                      {new Date(resume.created_at).toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                      })}
                    </span>
                  </div>
                </div>

                {/* CARD ACTIONS */}
                <div className="resume-card-actions">
                  <button
                    type="button"
                    className="action-btn preview-btn"
                    onClick={() => handleOpenPreview(resume)}
                    title="Preview multi-page resume"
                  >
                    <Eye size={14} />
                    <span>Preview</span>
                  </button>

                  {resume.has_latex && (
                    <button
                      type="button"
                      className="action-btn edit-btn"
                      onClick={() => onNavigate?.('builder', { resumeId: resume.id })}
                      title="Edit source in LaTeX Resume Builder"
                    >
                      <Edit2 size={14} />
                      <span>Edit</span>
                    </button>
                  )}

                  <a
                    href={`/api/v1/profile/resumes/${resume.id}/download?account_id=${accountId}`}
                    download={resume.filename}
                    className="action-btn download-btn"
                    title="Download PDF"
                  >
                    <Download size={14} />
                  </a>

                  <button
                    type="button"
                    className="action-btn delete-btn"
                    onClick={() => handleDelete(resume.id, resume.name)}
                    title="Delete resume"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* UPLOAD MODAL */}
      {isUploadOpen && (
        <div className="modal-backdrop" onClick={() => !isUploading && setIsUploadOpen(false)}>
          <div className="modal-container upload-resume-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-title-group">
                <Upload size={18} className="text-emerald-400" />
                <h3>Upload Readymade Resume</h3>
              </div>
              <button
                type="button"
                className="modal-close-btn"
                onClick={() => setIsUploadOpen(false)}
                disabled={isUploading}
              >
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleUploadSubmit} className="upload-modal-form">
              <div className="form-group">
                <label>PDF Document</label>
                <div className="file-drop-area">
                  <input
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) {
                        setUploadFile(f);
                        if (!uploadName) {
                          const base = f.name.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ');
                          setUploadName(base.charAt(0).toUpperCase() + base.slice(1));
                        }
                      }
                    }}
                    required
                  />
                  <div className="file-drop-text">
                    {uploadFile ? (
                      <span className="file-selected-name">
                        <Check size={16} className="text-emerald-400" />
                        {uploadFile.name} ({Math.round(uploadFile.size / 1024)} KB)
                      </span>
                    ) : (
                      <span>Drop your PDF here or click to browse (Max 10MB)</span>
                    )}
                  </div>
                </div>
              </div>

              <div className="form-group">
                <label>Resume Label / Name</label>
                <input
                  type="text"
                  className="text-input"
                  placeholder="e.g. Lead AI Engineer Master CV"
                  value={uploadName}
                  onChange={(e) => setUploadName(e.target.value)}
                />
                <span className="input-hint">A clear name helps you distinguish between role variations.</span>
              </div>

              <div className="checkbox-row">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={uploadIsDefault}
                    onChange={(e) => setUploadIsDefault(e.target.checked)}
                  />
                  <span>Set as Default Resume (prioritized for match scoring & outreach)</span>
                </label>
              </div>

              <div className="modal-footer-actions">
                <button
                  type="button"
                  className="btn-cancel"
                  onClick={() => setIsUploadOpen(false)}
                  disabled={isUploading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-confirm-upload"
                  disabled={isUploading || !uploadFile}
                >
                  {isUploading ? 'Verifying & Uploading...' : 'Upload & Save'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* FULL-FIDELITY PREVIEW MODAL */}
      {previewResume && (
        <div className="modal-backdrop" onClick={() => setPreviewResume(null)}>
          <div className="modal-container preview-resume-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header preview-header">
              <div className="preview-header-info">
                <h3>{previewResume.name}</h3>
                <span className="preview-filename">{previewResume.filename}</span>
                {previewResume.is_default && (
                  <span className="badge-default-active">★ Default</span>
                )}
              </div>

              <div className="preview-toolbar-actions">
                <div className="zoom-controls-group">
                  <button
                    type="button"
                    className="zoom-btn"
                    onClick={() => setPreviewZoom((z) => Math.max(50, z - 10))}
                    title="Zoom Out"
                  >
                    <ZoomOut size={14} />
                  </button>
                  <span className="zoom-indicator">{previewZoom}%</span>
                  <button
                    type="button"
                    className="zoom-btn"
                    onClick={() => setPreviewZoom((z) => Math.min(130, z + 10))}
                    title="Zoom In"
                  >
                    <ZoomIn size={14} />
                  </button>
                </div>

                <a
                  href={`/api/v1/profile/resumes/${previewResume.id}/download?account_id=${accountId}`}
                  download={previewResume.filename}
                  className="btn-download-preview"
                >
                  <Download size={14} />
                  <span>Download PDF</span>
                </a>

                {previewResume.has_latex && (
                  <button
                    type="button"
                    className="btn-edit-in-builder"
                    onClick={() => {
                      const rId = previewResume.id;
                      setPreviewResume(null);
                      onNavigate?.('builder', { resumeId: rId });
                    }}
                  >
                    <Edit2 size={14} />
                    <span>Open in Builder</span>
                  </button>
                )}

                <button
                  type="button"
                  className="modal-close-btn"
                  onClick={() => setPreviewResume(null)}
                >
                  <X size={18} />
                </button>
              </div>
            </div>

            <div className="preview-modal-body">
              {isLoadingDetails ? (
                <div className="preview-loading">
                  <div className="loading-spinner" />
                  <span>Rendering resume preview...</span>
                </div>
              ) : previewData?.latex_source ? (
                // Authentic Overleaf-grade multi-page discrete A4 renderer
                <div className="cv-full-preview-container overleaf-viewer-bg">
                  <div
                    className="overleaf-multi-page-container"
                    style={{ zoom: previewZoom / 100, margin: '0 auto' }}
                  >
                    {paginatedPages.map((page, pIdx) => (
                      <div key={pIdx} className="overleaf-a4-page-card">
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
              ) : previewData?.pdf_data ? (
                // PDF Viewer using Base64 data
                <div className="pdf-embed-wrapper">
                  <iframe
                    src={`data:application/pdf;base64,${previewData.pdf_data}#toolbar=0&navpanes=0`}
                    title={previewResume.name}
                    className="pdf-preview-iframe"
                  />
                </div>
              ) : (
                <div className="preview-fallback-text">
                  <p>{previewData?.extracted_text || 'No preview content available.'}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
