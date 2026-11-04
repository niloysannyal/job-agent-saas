import React, { useState, useMemo } from 'react';
import {
  User,
  Briefcase,
  GraduationCap,
  Code,
  FolderGit2,
  Compass,
  FileCode,
  Save,
  Plus,
  Trash2,
  Edit2,
  Upload,
  Sparkles,
  Download,
  Copy,
  Check,
  CheckCircle,
  Eye,
  X,
  ExternalLink,
  GitBranch,
  Code2,
  Columns,
  Layout,
  MapPin,
  Wifi,
  Building2,
  Globe,
} from 'lucide-react';
import { parseLatexDocument, paginateParsedDocument } from '../utils/latexCompiler';

const WORKPLACE_LABELS = {
  remote: 'Remote',
  hybrid: 'Hybrid',
  onsite: 'On-site',
  any: 'Any Mode',
};

export default function ProfileView({
  profile,
  profileForm,
  setProfileForm,
  onSaveProfile,
  isSaving,
  targetDesignations = [],
  onAddDesignation,
  onDeleteDesignation,
  targetLocations = [],
  onAddLocation,
  onDeleteLocation,
  compensation = {},
  onSaveCompensation,
  languages = [],
  onAddLanguage,
  onDeleteLanguage,
  showToast,
  accountId,
  authHeaders = {},
  onOpenOnboarding,
  onRefreshProfile,
}) {
  const [activeTab, setActiveTab] = useState('identity'); // identity | experience | education | skills | projects | targets | template

  // Local state for modals/forms
  const [newRole, setNewRole] = useState('');
  const [newLocationName, setNewLocationName] = useState('');
  const [newLocationType, setNewLocationType] = useState('remote');
  const [newRelocation, setNewRelocation] = useState(false);
  const [newLangName, setNewLangName] = useState('');
  const [newLangProficiency, setNewLangProficiency] = useState('fluent');

  // Compensation state
  const [compMin, setCompMin] = useState(compensation.min_salary != null ? String(compensation.min_salary) : '');
  const [compMax, setCompMax] = useState(compensation.max_salary != null ? String(compensation.max_salary) : '');
  const [compCurrency, setCompCurrency] = useState(compensation.currency || 'USD');
  const [compPeriod, setCompPeriod] = useState(compensation.period || 'yearly');

  // Work experience modal / edit state
  const [isExpModalOpen, setIsExpModalOpen] = useState(false);
  const [editingExp, setEditingExp] = useState(null);
  const [expForm, setExpForm] = useState({
    company: '',
    title: '',
    location: '',
    location_type: 'onsite',
    start_date: '',
    end_date: '',
    is_current: false,
    description: '',
    highlights: '',
  });

  // Education modal / state
  const [isEduModalOpen, setIsEduModalOpen] = useState(false);
  const [editingEdu, setEditingEdu] = useState(null);
  const [eduForm, setEduForm] = useState({
    institution: '',
    degree: '',
    field_of_study: '',
    location: '',
    start_date: '',
    end_date: '',
    grade: '',
  });

  // Skills state
  const [newSkillName, setNewSkillName] = useState('');
  const [newSkillCategory, setNewSkillCategory] = useState('Languages');
  const [newSkillProficiency, setNewSkillProficiency] = useState('Advanced');

  // Projects modal / state
  const [isProjModalOpen, setIsProjModalOpen] = useState(false);
  const [editingProj, setEditingProj] = useState(null);
  const [projForm, setProjForm] = useState({
    title: '',
    role: '',
    url: '',
    github_url: '',
    technologies: '',
    start_date: '',
    end_date: '',
    is_current: false,
    description: '',
    highlights: '',
  });

  // Preview CV state
  const [previewLatex, setPreviewLatex] = useState(null);
  const [editedLatex, setEditedLatex] = useState('');
  const [previewTemplateName, setPreviewTemplateName] = useState('');
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [previewMode, setPreviewMode] = useState('preview'); // 'preview' (default) | 'split'
  const [isCopied, setIsCopied] = useState(false);

  // Compute parsed document and discrete A4 sheets for compiled preview
  const parsedDoc = useMemo(() => {
    const codeToParse = previewMode === 'split' ? (editedLatex || previewLatex) : previewLatex;
    return parseLatexDocument(codeToParse || '');
  }, [previewLatex, editedLatex, previewMode]);

  const paginatedPages = useMemo(() => {
    return paginateParsedDocument(parsedDoc, 770);
  }, [parsedDoc]);

  // Field change for identity form
  const handleFieldChange = (e) => {
    const { name, value } = e.target;
    setProfileForm((prev) => ({ ...prev, [name]: value }));
  };

  // --- Work Experience Handlers ---
  const handleOpenAddExp = () => {
    setEditingExp(null);
    setExpForm({
      company: '',
      title: '',
      location: '',
      location_type: 'onsite',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
      highlights: '',
    });
    setIsExpModalOpen(true);
  };

  const handleOpenEditExp = (exp) => {
    setEditingExp(exp);
    let bullets = exp.highlights;
    if (typeof bullets === 'string' && bullets.startsWith('[')) {
      try {
        const arr = JSON.parse(bullets);
        bullets = arr.join('\n');
      } catch {}
    }
    setExpForm({
      company: exp.company || '',
      title: exp.title || '',
      location: exp.location || '',
      location_type: exp.location_type || 'onsite',
      start_date: exp.start_date || '',
      end_date: exp.end_date || '',
      is_current: exp.is_current || false,
      description: exp.description || '',
      highlights: bullets || '',
    });
    setIsExpModalOpen(true);
  };

  const handleSaveExp = async (e) => {
    e.preventDefault();
    try {
      const url = editingExp
        ? `/api/v1/profile/experiences/${editingExp.id}?account_id=${accountId}`
        : `/api/v1/profile/experiences?account_id=${accountId}`;
      const method = editingExp ? 'PATCH' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify(expForm),
      });

      if (!res.ok) throw new Error('Failed to save experience.');
      showToast?.(editingExp ? 'Work experience updated.' : 'Work experience added.');
      setIsExpModalOpen(false);
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error saving experience.');
    }
  };

  const handleDeleteExp = async (id) => {
    if (!confirm('Are you sure you want to remove this work experience?')) return;
    try {
      const res = await fetch(`/api/v1/profile/experiences/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (!res.ok) throw new Error('Failed to delete experience.');
      showToast?.('Work experience removed.');
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error deleting experience.');
    }
  };

  // --- Education Handlers ---
  const handleOpenAddEdu = () => {
    setEditingEdu(null);
    setEduForm({
      institution: '',
      degree: '',
      field_of_study: '',
      location: '',
      start_date: '',
      end_date: '',
      grade: '',
    });
    setIsEduModalOpen(true);
  };

  const handleOpenEditEdu = (edu) => {
    setEditingEdu(edu);
    setEduForm({
      institution: edu.institution || '',
      degree: edu.degree || '',
      field_of_study: edu.field_of_study || '',
      location: edu.location || '',
      start_date: edu.start_date || '',
      end_date: edu.end_date || '',
      grade: edu.grade || '',
    });
    setIsEduModalOpen(true);
  };

  const handleSaveEdu = async (e) => {
    e.preventDefault();
    try {
      const url = editingEdu
        ? `/api/v1/profile/educations/${editingEdu.id}?account_id=${accountId}`
        : `/api/v1/profile/educations?account_id=${accountId}`;
      const method = editingEdu ? 'PATCH' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify(eduForm),
      });

      if (!res.ok) throw new Error('Failed to save education.');
      showToast?.(editingEdu ? 'Education updated.' : 'Education added.');
      setIsEduModalOpen(false);
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error saving education.');
    }
  };

  const handleDeleteEdu = async (id) => {
    if (!confirm('Remove this education entry?')) return;
    try {
      const res = await fetch(`/api/v1/profile/educations/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (!res.ok) throw new Error('Failed to delete education.');
      showToast?.('Education removed.');
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error deleting education.');
    }
  };

  // --- Skill Handlers ---
  const handleAddSkill = async (e) => {
    e.preventDefault();
    if (!newSkillName.trim()) return;
    try {
      const res = await fetch(`/api/v1/profile/skills?account_id=${accountId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify({
          name: newSkillName.trim(),
          category: newSkillCategory,
          proficiency: newSkillProficiency,
        }),
      });
      if (!res.ok) throw new Error('Failed to add skill.');
      showToast?.(`Skill added: ${newSkillName}`);
      setNewSkillName('');
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error adding skill.');
    }
  };

  const handleDeleteSkill = async (id) => {
    try {
      const res = await fetch(`/api/v1/profile/skills/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (!res.ok) throw new Error('Failed to remove skill.');
      showToast?.('Skill removed.');
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error deleting skill.');
    }
  };

  // --- Projects Handlers ---
  const handleOpenAddProj = () => {
    setEditingProj(null);
    setProjForm({
      title: '',
      role: '',
      url: '',
      github_url: '',
      technologies: '',
      start_date: '',
      end_date: '',
      is_current: false,
      description: '',
      highlights: '',
    });
    setIsProjModalOpen(true);
  };

  const handleOpenEditProj = (proj) => {
    setEditingProj(proj);
    let bullets = proj.highlights;
    if (typeof bullets === 'string' && bullets.startsWith('[')) {
      try {
        const arr = JSON.parse(bullets);
        bullets = arr.join('\n');
      } catch {}
    }
    setProjForm({
      title: proj.title || '',
      role: proj.role || '',
      url: proj.url || '',
      github_url: proj.github_url || '',
      technologies: proj.technologies || '',
      start_date: proj.start_date || '',
      end_date: proj.end_date || '',
      is_current: proj.end_date === 'Present' || false,
      description: proj.description || '',
      highlights: bullets || '',
    });
    setIsProjModalOpen(true);
  };

  const handleSaveProj = async (e) => {
    e.preventDefault();
    try {
      const url = editingProj
        ? `/api/v1/profile/projects/${editingProj.id}?account_id=${accountId}`
        : `/api/v1/profile/projects?account_id=${accountId}`;
      const method = editingProj ? 'PATCH' : 'POST';

      const payload = {
        title: projForm.title,
        role: projForm.role || null,
        url: projForm.url || null,
        github_url: projForm.github_url || null,
        technologies: projForm.technologies || null,
        start_date: projForm.start_date || null,
        end_date: projForm.is_current ? 'Present' : (projForm.end_date || null),
        description: projForm.description || null,
        highlights: projForm.highlights || null,
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error('Failed to save project.');
      showToast?.(editingProj ? 'Project updated.' : 'Project added.');
      setIsProjModalOpen(false);
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error saving project.');
    }
  };

  const handleDeleteProj = async (id) => {
    if (!confirm('Are you sure you want to remove this project?')) return;
    try {
      const res = await fetch(`/api/v1/profile/projects/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (!res.ok) throw new Error('Failed to delete project.');
      showToast?.('Project removed.');
      if (onRefreshProfile) await onRefreshProfile();
    } catch (err) {
      showToast?.(err.message || 'Error deleting project.');
    }
  };

  // --- Preview & Compile LaTeX ---
  const handleFetchPreview = async (templateId = null) => {
    try {
      setIsLoadingPreview(true);
      const url = templateId
        ? `/api/v1/profile/preview-cv?account_id=${accountId}&template_id=${templateId}`
        : `/api/v1/profile/preview-cv?account_id=${accountId}`;
      const res = await fetch(url, { headers: { ...authHeaders } });
      if (!res.ok) throw new Error('Failed to generate CV preview.');
      const data = await res.json();
      setPreviewLatex(data.latex_source);
      setEditedLatex(data.latex_source);
      setPreviewTemplateName(data.template_name);
      showToast?.('CV compiled successfully with active template!');
    } catch (err) {
      showToast?.(err.message || 'Error compiling CV preview.');
    } finally {
      setIsLoadingPreview(false);
    }
  };

  const handleCopyLatex = async () => {
    const codeToCopy = previewMode === 'split' ? (editedLatex || previewLatex) : previewLatex;
    if (!codeToCopy) return;
    try {
      await navigator.clipboard.writeText(codeToCopy);
      setIsCopied(true);
      showToast?.('LaTeX code copied to clipboard!');
      setTimeout(() => setIsCopied(false), 2500);
    } catch {
      showToast?.('Failed to copy to clipboard.');
    }
  };

  const handleDownloadLatex = () => {
    const codeToDownload = previewMode === 'split' ? (editedLatex || previewLatex) : previewLatex;
    if (!codeToDownload) return;
    const blob = new Blob([codeToDownload], { type: 'text/x-tex;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${previewTemplateName || 'TAILORED_CV'}.tex`;
    link.click();
    URL.revokeObjectURL(url);
    showToast?.('Downloaded LaTeX source file.');
  };

  // Helper to render authentic A4 compiled CV page cards
  const renderA4Pages = () => {
    if (isLoadingPreview) {
      return (
        <div className="loading-preview-state">
          <Sparkles size={36} className="spin-icon text-emerald-400" />
          <p style={{ marginTop: '12px', color: 'var(--text-secondary)' }}>
            Compiling profile entities into pixel-perfect CV document...
          </p>
        </div>
      );
    }

    if (!previewLatex && !editedLatex) {
      return (
        <div className="empty-panel-state">
          <FileCode size={36} className="dim-icon" />
          <h4>No Compiled Preview Available</h4>
          <p>Click "Re-compile Preview" above to generate your compiled CV page.</p>
        </div>
      );
    }

    return (
      <div className="overleaf-multi-page-container">
        {paginatedPages.map((page, pIdx) => (
          <div key={pIdx} className="overleaf-a4-page-card" id={`profile-cv-page-${page.pageNumber}`}>
            {/* Page number badge */}
            <div className="a4-page-top-badge">Page {page.pageNumber} of {paginatedPages.length}</div>

            {/* Document Header (Page 1) */}
            {page.hasHeader && (
              <div className="cv-header-container">
                <div className="cv-header-top-row">
                  <div className="cv-header-left">
                    <h1 className="cv-name">{(parsedDoc.header.name || profileForm.full_name || 'CANDIDATE').toUpperCase()}</h1>
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
    <div className="section-container profile-view">
      {/* Top Banner with One-Click Onboarding / CV Parser */}
      <div className="profile-top-banner panel-card">
        <div className="banner-text">
          <div className="badge-row">
            <span className="brand-pill">⚡ Universal Career Profile</span>
            <span className="tag-pill-dim">All Tech & Private Roles</span>
          </div>
          <h2>Professional Identity & CV Control Center</h2>
          <p>
            Manage your structured career history, verify facts, and select admin-curated LaTeX templates
            without ever needing to write or debug raw LaTeX code.
          </p>
        </div>
        <div className="banner-actions">
          <button className="action-btn-primary" onClick={onOpenOnboarding}>
            <Upload size={16} />
            <span>Upload CV to Auto-Fill</span>
          </button>
        </div>
      </div>

      {/* Sub-Navigation Tabs */}
      <div className="sub-nav-tabs">
        <button
          className={`sub-tab-btn ${activeTab === 'identity' ? 'active' : ''}`}
          onClick={() => setActiveTab('identity')}
        >
          <User className="tab-icon" />
          <span>Identity & Contact</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'experience' ? 'active' : ''}`}
          onClick={() => setActiveTab('experience')}
        >
          <Briefcase className="tab-icon" />
          <span>Experience ({profile?.work_experiences?.length || 0})</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'education' ? 'active' : ''}`}
          onClick={() => setActiveTab('education')}
        >
          <GraduationCap className="tab-icon" />
          <span>Education ({profile?.educations?.length || 0})</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'skills' ? 'active' : ''}`}
          onClick={() => setActiveTab('skills')}
        >
          <Code className="tab-icon" />
          <span>Skills ({profile?.skills?.length || 0})</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'projects' ? 'active' : ''}`}
          onClick={() => setActiveTab('projects')}
        >
          <FolderGit2 className="tab-icon" />
          <span>Projects ({profile?.projects?.length || 0})</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'targets' ? 'active' : ''}`}
          onClick={() => setActiveTab('targets')}
        >
          <Compass className="tab-icon" />
          <span>Target Roles & Modes</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'template' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('template');
            if (!previewLatex) handleFetchPreview();
          }}
        >
          <FileCode className="tab-icon" />
          <span>CV Template & Preview</span>
        </button>
      </div>

      {/* TAB 1: IDENTITY & CONTACT */}
      {activeTab === 'identity' && (
        <form onSubmit={onSaveProfile} className="profile-form panel-card">
          <div className="panel-header">
            <h3>Candidate Identity & Executive Contact</h3>
            <button type="submit" disabled={isSaving} className="action-btn-primary">
              <Save className="btn-icon" />
              <span>{isSaving ? 'Saving...' : 'Save Identity'}</span>
            </button>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Full Name *</label>
              <input
                type="text"
                name="full_name"
                value={profileForm.full_name || ''}
                onChange={handleFieldChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Professional Headline *</label>
              <input
                type="text"
                name="headline"
                value={profileForm.headline || ''}
                onChange={handleFieldChange}
                placeholder="e.g. Senior Backend Engineer | Distributed Systems"
              />
            </div>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Current Role / Title</label>
              <input
                type="text"
                name="current_role"
                value={profileForm.current_role || ''}
                onChange={handleFieldChange}
              />
            </div>
            <div className="form-group">
              <label>Current Organization / Company</label>
              <input
                type="text"
                name="current_company"
                value={profileForm.current_company || ''}
                onChange={handleFieldChange}
              />
            </div>
          </div>

          <div className="form-grid-3">
            <div className="form-group">
              <label>Phone / WhatsApp</label>
              <input
                type="text"
                name="phone"
                value={profileForm.phone || ''}
                onChange={handleFieldChange}
                placeholder="+1 555-0199"
              />
            </div>
            <div className="form-group">
              <label>City</label>
              <input
                type="text"
                name="location_city"
                value={profileForm.location_city || ''}
                onChange={handleFieldChange}
              />
            </div>
            <div className="form-group">
              <label>Country</label>
              <input
                type="text"
                name="location_country"
                value={profileForm.location_country || ''}
                onChange={handleFieldChange}
              />
            </div>
          </div>

          <div className="form-grid-3">
            <div className="form-group">
              <label>LinkedIn URL</label>
              <input
                type="text"
                name="linkedin_url"
                value={profileForm.linkedin_url || ''}
                onChange={handleFieldChange}
              />
            </div>
            <div className="form-group">
              <label>GitHub URL</label>
              <input
                type="text"
                name="github_url"
                value={profileForm.github_url || ''}
                onChange={handleFieldChange}
              />
            </div>
            <div className="form-group">
              <label>Portfolio / Personal Website</label>
              <input
                type="text"
                name="portfolio_url"
                value={profileForm.portfolio_url || ''}
                onChange={handleFieldChange}
                placeholder="https://yourportfolio.com"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Executive Career Summary</label>
            <textarea
              name="summary"
              rows={4}
              value={profileForm.summary || ''}
              onChange={handleFieldChange}
              placeholder="Concise 2-4 sentence executive narrative of your experience, ownership, and engineering impact..."
            />
          </div>
        </form>
      )}

      {/* TAB 2: WORK EXPERIENCE */}
      {activeTab === 'experience' && (
        <div className="panel-card">
          <div className="panel-header">
            <div>
              <h3>Work Experience History</h3>
              <p className="subtext">Chronological career milestones used as ground truth for CV tailoring.</p>
            </div>
            <button className="action-btn-primary" onClick={handleOpenAddExp}>
              <Plus size={16} /> Add Position
            </button>
          </div>

          <div className="experience-list">
            {(!profile?.work_experiences || profile.work_experiences.length === 0) ? (
              <div className="empty-panel-state">
                <Briefcase size={36} className="dim-icon" />
                <h4>No work experiences recorded yet</h4>
                <p>Click "Add Position" above or upload your CV to auto-fill your career history.</p>
              </div>
            ) : (
              profile.work_experiences.map((exp) => (
                <div key={exp.id} className="career-card">
                  <div className="career-card-header">
                    <div>
                      <div className="role-company-line">
                        <h4 className="card-title">{exp.title}</h4>
                        <span className="card-at">at</span>
                        <h4 className="card-company">{exp.company}</h4>
                        {exp.is_current && <span className="badge-active">Current</span>}
                      </div>
                      <div className="card-meta">
                        <span>{exp.start_date} -- {exp.is_current ? 'Present' : exp.end_date}</span>
                        {exp.location && <span> &bull; {exp.location} ({exp.location_type})</span>}
                      </div>
                    </div>
                    <div className="card-actions">
                      <button className="btn-icon-subtle" title="Edit Position" onClick={() => handleOpenEditExp(exp)}>
                        <Edit2 size={15} />
                      </button>
                      <button className="btn-icon-danger" title="Remove Position" onClick={() => handleDeleteExp(exp.id)}>
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </div>

                  {exp.description && <p className="card-desc">{exp.description}</p>}

                  {exp.highlights && (
                    <ul className="card-highlights">
                      {(typeof exp.highlights === 'string' && exp.highlights.startsWith('[')
                        ? JSON.parse(exp.highlights)
                        : exp.highlights.split('\n')
                      ).map((bullet, idx) => (
                        <li key={idx}>{bullet}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* TAB 3: EDUCATION */}
      {activeTab === 'education' && (
        <div className="panel-card">
          <div className="panel-header">
            <div>
              <h3>Education & Credentials</h3>
              <p className="subtext">Academic degrees, institutions, locations, and honors.</p>
            </div>
            <button className="action-btn-primary" onClick={handleOpenAddEdu}>
              <Plus size={16} /> Add Education
            </button>
          </div>

          <div className="education-list">
            {(!profile?.educations || profile.educations.length === 0) ? (
              <div className="empty-panel-state">
                <GraduationCap size={36} className="dim-icon" />
                <h4>No education entries recorded</h4>
                <p>Click "Add Education" to add degrees or coursework.</p>
              </div>
            ) : (
              profile.educations.map((edu) => (
                <div key={edu.id} className="career-card">
                  <div className="career-card-header">
                    <div>
                      <h4 className="card-title">{edu.degree} {edu.field_of_study && `in ${edu.field_of_study}`}</h4>
                      <h5 className="card-company">{edu.institution}</h5>
                      <div className="card-meta">
                        <span>{edu.start_date} -- {edu.end_date}</span>
                        {edu.location && <span> &bull; {edu.location}</span>}
                        {edu.grade && <span> &bull; Grade: {edu.grade}</span>}
                      </div>
                    </div>
                    <div className="card-actions">
                      <button className="btn-icon-subtle" title="Edit Education" onClick={() => handleOpenEditEdu(edu)}>
                        <Edit2 size={15} />
                      </button>
                      <button className="btn-icon-danger" title="Remove Education" onClick={() => handleDeleteEdu(edu.id)}>
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* TAB 4: SKILLS */}
      {activeTab === 'skills' && (
        <div className="panel-card">
          <div className="panel-header">
            <div>
              <h3>Skills & Competencies</h3>
              <p className="subtext">Categorized technical and professional skills matched during job searches.</p>
            </div>
          </div>

          {/* Add skill form with aligned height and tokens */}
          <form onSubmit={handleAddSkill} className="add-subrecord-form">
            <input
              type="text"
              placeholder="e.g. Python, Docker, Financial Modeling..."
              value={newSkillName}
              onChange={(e) => setNewSkillName(e.target.value)}
              required
            />
            <select
              value={newSkillCategory}
              onChange={(e) => setNewSkillCategory(e.target.value)}
            >
              <option value="Languages">Languages</option>
              <option value="Frameworks">Frameworks & Libraries</option>
              <option value="Cloud & DevOps">Cloud & DevOps</option>
              <option value="Databases">Databases & Storage</option>
              <option value="Tools">Tools & Systems</option>
              <option value="Management">Management & Leadership</option>
              <option value="Soft Skills">Soft Skills & Communication</option>
            </select>
            <select
              value={newSkillProficiency}
              onChange={(e) => setNewSkillProficiency(e.target.value)}
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
              <option value="Expert">Expert</option>
            </select>
            <button type="submit" className="action-btn-primary">
              <Plus size={16} /> Add Skill
            </button>
          </form>

          {/* Grouped Skills */}
          <div className="skills-categories-grid">
            {['Languages', 'Frameworks', 'Cloud & DevOps', 'Databases', 'Tools', 'Management', 'Soft Skills'].map((cat) => {
              const catSkills = (profile?.skills || []).filter((s) => s.category === cat);
              if (catSkills.length === 0) return null;
              return (
                <div key={cat} className="skill-category-box">
                  <h4 className="category-title">{cat}</h4>
                  <div className="skill-chips-row">
                    {catSkills.map((s) => (
                      <span key={s.id} className="skill-chip">
                        <span className="skill-chip-name">{s.name}</span>
                        <span className="skill-chip-level">{s.proficiency}</span>
                        <button
                          type="button"
                          className="chip-remove"
                          title="Remove skill"
                          onClick={() => handleDeleteSkill(s.id)}
                        >
                          <X size={12} />
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 5: PROJECTS */}
      {activeTab === 'projects' && (
        <div className="panel-card">
          <div className="panel-header">
            <div>
              <h3>Featured Projects & Deliverables</h3>
              <p className="subtext">Portfolio projects, open-source repositories, and key engineering systems.</p>
            </div>
            <button className="action-btn-primary" onClick={handleOpenAddProj}>
              <Plus size={16} /> Add Project
            </button>
          </div>

          <div className="projects-list">
            {(!profile?.projects || profile.projects.length === 0) ? (
              <div className="empty-panel-state">
                <FolderGit2 size={36} className="dim-icon" />
                <h4>No projects recorded yet</h4>
                <p>Click "Add Project" above to highlight open-source repositories, client deliverables, or portfolio systems.</p>
              </div>
            ) : (
              profile.projects.map((proj) => (
                <div key={proj.id} className="career-card">
                  <div className="career-card-header">
                    <div>
                      <div className="role-company-line">
                        <h4 className="card-title">{proj.title}</h4>
                        {proj.role && (
                          <>
                            <span className="card-at">as</span>
                            <h4 className="card-company">{proj.role}</h4>
                          </>
                        )}
                        {proj.end_date === 'Present' && <span className="badge-active">Ongoing</span>}
                      </div>

                      <div className="card-meta">
                        <span>{proj.start_date || 'Project'} -- {proj.end_date || 'Completed'}</span>
                      </div>

                      {/* Project Links (Live Demo + GitHub) */}
                      <div className="project-links-row">
                        {proj.url && (
                          <a
                            href={proj.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="project-link-badge"
                            title="Open live project"
                          >
                            <ExternalLink size={12} />
                            <span>Live Demo</span>
                          </a>
                        )}
                        {proj.github_url && (
                          <a
                            href={proj.github_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="project-link-badge"
                            title="Open GitHub repository"
                          >
                            <GitBranch size={12} />
                            <span>GitHub Repo</span>
                          </a>
                        )}
                      </div>

                      {/* Tech stack badges */}
                      {proj.technologies && (
                        <div className="tech-stack-row">
                          {proj.technologies.split(',').map((tech, tIdx) => (
                            <span key={tIdx} className="tech-stack-badge">
                              {tech.trim()}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    <div className="card-actions">
                      <button className="btn-icon-subtle" title="Edit Project" onClick={() => handleOpenEditProj(proj)}>
                        <Edit2 size={15} />
                      </button>
                      <button className="btn-icon-danger" title="Remove Project" onClick={() => handleDeleteProj(proj.id)}>
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </div>

                  {proj.description && <p className="card-desc">{proj.description}</p>}

                  {proj.highlights && (
                    <ul className="card-highlights">
                      {(typeof proj.highlights === 'string' && proj.highlights.startsWith('[')
                        ? JSON.parse(proj.highlights)
                        : proj.highlights.split('\n')
                      ).map((bullet, idx) => (
                        <li key={idx}>{bullet}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* TAB 6: TARGET ROLES & LOCATIONS */}
      {activeTab === 'targets' && (
        <div className="targets-section-grid">
          {/* Target Roles */}
          <div className="panel-card">
            <div className="panel-header">
              <h3>Target Job Roles</h3>
            </div>
            <p className="subtext">Ranked order of target roles. Higher priority roles receive higher search weighting.</p>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (newRole.trim()) {
                  onAddDesignation(newRole.trim(), targetDesignations.length);
                  setNewRole('');
                }
              }}
              className="add-subrecord-form"
            >
              <input
                type="text"
                placeholder="e.g. Senior Backend Engineer"
                value={newRole}
                onChange={(e) => setNewRole(e.target.value)}
              />
              <button type="submit" className="action-btn-primary">
                <Plus size={16} /> Add Role
              </button>
            </form>

            <div className="subrecord-list">
              {targetDesignations.length === 0 ? (
                <div className="subrecord-empty-state">
                  <span>No target roles added yet. Add your preferred job titles above.</span>
                </div>
              ) : (
                targetDesignations.map((desig, idx) => (
                  <div key={desig.id || idx} className="subrecord-item">
                    <div className="subrecord-left">
                      <span className="rank-badge">#{idx + 1}</span>
                      <span className="item-title">{desig.title}</span>
                    </div>
                    <button
                      className="btn-icon-danger"
                      title="Remove Role"
                      onClick={() => onDeleteDesignation(desig.id)}
                    >
                      <Trash2 size={15} />
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Workplace Modes & Locations */}
          <div className="panel-card">
            <div className="panel-header">
              <h3>Target Locations & Work Modes</h3>
            </div>
            <p className="subtext">Define locations and whether you prefer Remote, Hybrid, or On-site.</p>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (newLocationName.trim()) {
                  onAddLocation(newLocationName.trim(), newLocationType, newRelocation);
                  setNewLocationName('');
                }
              }}
              className="add-subrecord-form"
            >
              <input
                type="text"
                placeholder="e.g. London, United Kingdom or Remote"
                value={newLocationName}
                onChange={(e) => setNewLocationName(e.target.value)}
              />
              <select
                value={newLocationType}
                onChange={(e) => setNewLocationType(e.target.value)}
              >
                <option value="remote">Remote</option>
                <option value="hybrid">Hybrid</option>
                <option value="onsite">On-site</option>
                <option value="any">Any Mode</option>
              </select>
              <button type="submit" className="action-btn-primary">
                <Plus size={16} /> Add Location
              </button>
            </form>

            <div className="subrecord-list">
              {targetLocations.length === 0 ? (
                <div className="subrecord-empty-state">
                  <span>No target locations added yet. Add your target cities or remote preferences above.</span>
                </div>
              ) : (
                targetLocations.map((loc) => (
                  <div key={loc.id} className="subrecord-item">
                    <div className="subrecord-left">
                      <MapPin size={15} className="subrecord-pin-icon" />
                      <span className="item-title">{loc.location_name}</span>
                    </div>
                    <div className="subrecord-actions">
                      <span className={`workplace-badge badge-${loc.location_type}`}>
                        {loc.location_type === 'remote' ? (
                          <Wifi size={11} />
                        ) : loc.location_type === 'hybrid' ? (
                          <Building2 size={11} />
                        ) : loc.location_type === 'onsite' ? (
                          <MapPin size={11} />
                        ) : (
                          <Globe size={11} />
                        )}
                        <span>{WORKPLACE_LABELS[loc.location_type] || loc.location_type}</span>
                      </span>
                      <button
                        className="btn-icon-danger"
                        title="Remove Location"
                        onClick={() => onDeleteLocation(loc.id)}
                      >
                        <Trash2 size={15} />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* TAB 7: CV TEMPLATE & PREVIEW */}
      {activeTab === 'template' && (
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
              onClick={() => handleFetchPreview()}
            >
              01_MODERN_TECH (Default)
            </button>
            <button
              className={`pill-btn ${previewTemplateName === '02_CLASSIC_CORPORATE' ? 'active' : ''}`}
              onClick={() => handleFetchPreview()}
            >
              02_CLASSIC_CORPORATE
            </button>
            <button
              className={`pill-btn ${previewTemplateName === '03_MINIMALIST_COMPACT' ? 'active' : ''}`}
              onClick={() => handleFetchPreview()}
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
      )}

      {/* MODAL: ADD / EDIT WORK EXPERIENCE */}
      {isExpModalOpen && (
        <div className="modal-backdrop">
          <div className="modal-content modal-medium">
            <div className="modal-header">
              <h3>{editingExp ? 'Edit Work Experience' : 'Add Work Experience'}</h3>
              <button className="btn-icon-close" onClick={() => setIsExpModalOpen(false)}>
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSaveExp} className="modal-form">
              <div className="form-grid-2">
                <div className="form-group">
                  <label>Job Title *</label>
                  <input
                    type="text"
                    value={expForm.title}
                    onChange={(e) => setExpForm({ ...expForm, title: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Company / Organization *</label>
                  <input
                    type="text"
                    value={expForm.company}
                    onChange={(e) => setExpForm({ ...expForm, company: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Location</label>
                  <input
                    type="text"
                    value={expForm.location}
                    onChange={(e) => setExpForm({ ...expForm, location: e.target.value })}
                    placeholder="e.g. London, UK"
                  />
                </div>
                <div className="form-group">
                  <label>Workplace Mode</label>
                  <select
                    value={expForm.location_type}
                    onChange={(e) => setExpForm({ ...expForm, location_type: e.target.value })}
                  >
                    <option value="onsite">On-site</option>
                    <option value="remote">Remote</option>
                    <option value="hybrid">Hybrid</option>
                  </select>
                </div>
              </div>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Start Date *</label>
                  <input
                    type="text"
                    value={expForm.start_date}
                    onChange={(e) => setExpForm({ ...expForm, start_date: e.target.value })}
                    placeholder="e.g. 2022-01 or Jan 2022"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>End Date</label>
                  <input
                    type="text"
                    value={expForm.end_date}
                    onChange={(e) => setExpForm({ ...expForm, end_date: e.target.value })}
                    placeholder="e.g. 2024-05 (leave blank if current)"
                    disabled={expForm.is_current}
                  />
                  <label className="checkbox-inline">
                    <input
                      type="checkbox"
                      checked={expForm.is_current}
                      onChange={(e) => setExpForm({ ...expForm, is_current: e.target.checked })}
                    />
                    I currently work here
                  </label>
                </div>
              </div>

              <div className="form-group">
                <label>Key Accomplishments & Bullet Points (one per line)</label>
                <textarea
                  rows={4}
                  value={expForm.highlights}
                  onChange={(e) => setExpForm({ ...expForm, highlights: e.target.value })}
                  placeholder="&bull; Architected distributed caching layer saving $50k/mo&#10;&bull; Led a squad of 4 engineers delivering payments API"
                />
              </div>

              <div className="modal-actions">
                <button type="button" className="action-btn-secondary" onClick={() => setIsExpModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="action-btn-primary">
                  Save Position
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: ADD / EDIT EDUCATION */}
      {isEduModalOpen && (
        <div className="modal-backdrop">
          <div className="modal-content modal-medium">
            <div className="modal-header">
              <h3>{editingEdu ? 'Edit Education Background' : 'Add Education Background'}</h3>
              <button className="btn-icon-close" onClick={() => setIsEduModalOpen(false)}>
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSaveEdu} className="modal-form">
              <div className="form-grid-2">
                <div className="form-group">
                  <label>Institution / University *</label>
                  <input
                    type="text"
                    value={eduForm.institution}
                    onChange={(e) => setEduForm({ ...eduForm, institution: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Degree *</label>
                  <input
                    type="text"
                    value={eduForm.degree}
                    onChange={(e) => setEduForm({ ...eduForm, degree: e.target.value })}
                    placeholder="e.g. B.Sc., M.Sc., High School"
                    required
                  />
                </div>
              </div>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Field of Study</label>
                  <input
                    type="text"
                    value={eduForm.field_of_study}
                    onChange={(e) => setEduForm({ ...eduForm, field_of_study: e.target.value })}
                    placeholder="e.g. Computer Science"
                  />
                </div>
                <div className="form-group">
                  <label>Campus / City Location</label>
                  <input
                    type="text"
                    value={eduForm.location}
                    onChange={(e) => setEduForm({ ...eduForm, location: e.target.value })}
                    placeholder="e.g. Stanford, CA or Cambridge, UK"
                  />
                </div>
              </div>

              <div className="form-grid-3">
                <div className="form-group">
                  <label>Start Year</label>
                  <input
                    type="text"
                    value={eduForm.start_date}
                    onChange={(e) => setEduForm({ ...eduForm, start_date: e.target.value })}
                    placeholder="2018"
                  />
                </div>
                <div className="form-group">
                  <label>End Year</label>
                  <input
                    type="text"
                    value={eduForm.end_date}
                    onChange={(e) => setEduForm({ ...eduForm, end_date: e.target.value })}
                    placeholder="2022"
                  />
                </div>
                <div className="form-group">
                  <label>Grade / GPA / Honors</label>
                  <input
                    type="text"
                    value={eduForm.grade}
                    onChange={(e) => setEduForm({ ...eduForm, grade: e.target.value })}
                    placeholder="e.g. 3.9 / 4.0 or First Class"
                  />
                </div>
              </div>

              <div className="modal-actions">
                <button type="button" className="action-btn-secondary" onClick={() => setIsEduModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="action-btn-primary">
                  Save Education
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL: ADD / EDIT PROJECT */}
      {isProjModalOpen && (
        <div className="modal-backdrop">
          <div className="modal-content modal-medium">
            <div className="modal-header">
              <h3>{editingProj ? 'Edit Project' : 'Add Project'}</h3>
              <button className="btn-icon-close" onClick={() => setIsProjModalOpen(false)}>
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSaveProj} className="modal-form">
              <div className="form-grid-2">
                <div className="form-group">
                  <label>Project Name *</label>
                  <input
                    type="text"
                    value={projForm.title}
                    onChange={(e) => setProjForm({ ...projForm, title: e.target.value })}
                    placeholder="e.g. Full Send Sports AI"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Role / Ownership</label>
                  <input
                    type="text"
                    value={projForm.role}
                    onChange={(e) => setProjForm({ ...projForm, role: e.target.value })}
                    placeholder="e.g. Creator & Lead Architect"
                  />
                </div>
              </div>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Live Link / Demo URL</label>
                  <input
                    type="url"
                    value={projForm.url}
                    onChange={(e) => setProjForm({ ...projForm, url: e.target.value })}
                    placeholder="https://example.com/demo"
                  />
                </div>
                <div className="form-group">
                  <label>GitHub Repository URL</label>
                  <input
                    type="url"
                    value={projForm.github_url}
                    onChange={(e) => setProjForm({ ...projForm, github_url: e.target.value })}
                    placeholder="https://github.com/user/project"
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Tech Stack (comma-separated)</label>
                <input
                  type="text"
                  value={projForm.technologies}
                  onChange={(e) => setProjForm({ ...projForm, technologies: e.target.value })}
                  placeholder="e.g. Python, FastAPI, React 19, PostgreSQL, Docker, AWS"
                />
              </div>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Start Date</label>
                  <input
                    type="text"
                    value={projForm.start_date}
                    onChange={(e) => setProjForm({ ...projForm, start_date: e.target.value })}
                    placeholder="e.g. 2024-01 or Jan 2024"
                  />
                </div>
                <div className="form-group">
                  <label>End Date</label>
                  <input
                    type="text"
                    value={projForm.end_date}
                    onChange={(e) => setProjForm({ ...projForm, end_date: e.target.value })}
                    placeholder="e.g. 2024-06"
                    disabled={projForm.is_current}
                  />
                  <label className="checkbox-inline">
                    <input
                      type="checkbox"
                      checked={projForm.is_current}
                      onChange={(e) => setProjForm({ ...projForm, is_current: e.target.checked })}
                    />
                    Ongoing project
                  </label>
                </div>
              </div>

              <div className="form-group">
                <label>Project Description</label>
                <textarea
                  rows={2}
                  value={projForm.description}
                  onChange={(e) => setProjForm({ ...projForm, description: e.target.value })}
                  placeholder="Summary of the project's purpose, architecture, and engineering scale..."
                />
              </div>

              <div className="form-group">
                <label>Key Highlights & Accomplishments (one bullet per line)</label>
                <textarea
                  rows={3}
                  value={projForm.highlights}
                  onChange={(e) => setProjForm({ ...projForm, highlights: e.target.value })}
                  placeholder="&bull; Trained ensemble XGBoost pipeline on 10k+ records with sub-100ms latency&#10;&bull; Deployed on AWS with high-availability autoscaling"
                />
              </div>

              <div className="modal-actions">
                <button type="button" className="action-btn-secondary" onClick={() => setIsProjModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="action-btn-primary">
                  Save Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
