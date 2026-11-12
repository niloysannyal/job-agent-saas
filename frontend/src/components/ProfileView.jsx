import React, { useState, useMemo } from 'react';
import {
  User,
  Briefcase,
  GraduationCap,
  Code,
  FolderGit2,
  Compass,
  FileCode,
  FileText,
  Upload,
} from 'lucide-react';
import { parseLatexDocument, paginateParsedDocument, compileParsedLatexToPdf } from '../utils/latexCompiler';
import ProfileIdentityTab from './profile/ProfileIdentityTab';
import ProfileExperienceTab from './profile/ProfileExperienceTab';
import ProfileEducationTab from './profile/ProfileEducationTab';
import ProfileSkillsTab from './profile/ProfileSkillsTab';
import ProfileProjectsTab from './profile/ProfileProjectsTab';
import ProfileTargetsTab from './profile/ProfileTargetsTab';
import ProfileTemplatesTab from './profile/ProfileTemplatesTab';
import SavedResumesTab from './profile/SavedResumesTab';
import ProfileExperienceModal from './profile/ProfileExperienceModal';
import ProfileEducationModal from './profile/ProfileEducationModal';
import ProfileProjectModal from './profile/ProfileProjectModal';

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
  onNavigate,
}) {
  const [activeTab, setActiveTab] = useState('identity'); // identity | experience | education | skills | projects | targets | resumes

  // Local state for modals/forms
  const [newRole, setNewRole] = useState('');
  const [newLocationName, setNewLocationName] = useState('');
  const [newLocationType, setNewLocationType] = useState('remote');
  const [newRelocation, setNewRelocation] = useState(false);

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

  // LaTeX Preview & Side-by-Side Editor State
  const [previewLatex, setPreviewLatex] = useState(profile?.master_cv_latex || '');
  const [editedLatex, setEditedLatex] = useState(profile?.master_cv_latex || '');
  const [previewTemplateName, setPreviewTemplateName] = useState('01_MODERN_TECH');
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [previewMode, setPreviewMode] = useState('preview'); // 'preview' (default) | 'split'
  const [isCopied, setIsCopied] = useState(false);

  // Parsed LaTeX document for visual rendering
  const parsedDoc = useMemo(() => {
    const sourceCode = previewMode === 'split' ? (editedLatex || previewLatex) : (previewLatex || editedLatex);
    if (!sourceCode) return parseLatexDocument('');
    return parseLatexDocument(sourceCode);
  }, [previewLatex, editedLatex, previewMode]);

  // Paginate parsed document into discrete A4 sheets
  const paginatedPages = useMemo(() => {
    return paginateParsedDocument(parsedDoc, 770);
  }, [parsedDoc]);

  // Field change helper for profileForm
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
      if (templateId) {
        setPreviewTemplateName(templateId);
      }
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
    const candidateName = (profileForm?.full_name || profile?.full_name || 'Candidate').replace(/\s+/g, '_');
    link.download = `${candidateName}_${previewTemplateName || 'TAILORED_CV'}.tex`;
    link.click();
    URL.revokeObjectURL(url);
    showToast?.('Downloaded LaTeX source file.');
  };

  const handleDownloadPdf = () => {
    try {
      if (!parsedDoc) {
        showToast?.('No compiled document available to export.');
        return;
      }
      const candidateName = (profileForm?.full_name || profile?.full_name || 'Candidate').replace(/\s+/g, '_');
      const filename = `${candidateName}_${previewTemplateName || 'CV'}.pdf`;
      const doc = compileParsedLatexToPdf(parsedDoc, filename);
      doc.save(filename);
      showToast?.(`Downloaded ${filename}!`);
    } catch (err) {
      console.error('Failed to export PDF:', err);
      showToast?.('Failed to generate PDF. You can download .tex source instead.');
    }
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
          <User size={16} />
          <span>Identity</span>
        </button>
        <button
          className={`sub-tab-btn ${activeTab === 'experience' ? 'active' : ''}`}
          onClick={() => setActiveTab('experience')}
        >
          <Briefcase size={16} />
          <span>Experience</span>
          {profile?.work_experiences?.length > 0 && (
            <span className="tab-count-badge">{profile.work_experiences.length}</span>
          )}
        </button>
        <button
          className={`sub-tab-btn ${activeTab === 'education' ? 'active' : ''}`}
          onClick={() => setActiveTab('education')}
        >
          <GraduationCap size={16} />
          <span>Education</span>
          {profile?.educations?.length > 0 && (
            <span className="tab-count-badge">{profile.educations.length}</span>
          )}
        </button>
        <button
          className={`sub-tab-btn ${activeTab === 'skills' ? 'active' : ''}`}
          onClick={() => setActiveTab('skills')}
        >
          <Code size={16} />
          <span>Skills</span>
          {profile?.skills?.length > 0 && (
            <span className="tab-count-badge">{profile.skills.length}</span>
          )}
        </button>
        <button
          className={`sub-tab-btn ${activeTab === 'projects' ? 'active' : ''}`}
          onClick={() => setActiveTab('projects')}
        >
          <FolderGit2 size={16} />
          <span>Projects</span>
          {profile?.projects?.length > 0 && (
            <span className="tab-count-badge">{profile.projects.length}</span>
          )}
        </button>
        <button
          className={`sub-tab-btn ${activeTab === 'targets' ? 'active' : ''}`}
          onClick={() => setActiveTab('targets')}
        >
          <Compass size={16} />
          <span>Target Roles & Modes</span>
        </button>
        <button
          className={`sub-tab-btn ${activeTab === 'resumes' ? 'active' : ''}`}
          onClick={() => setActiveTab('resumes')}
        >
          <FileText size={16} />
          <span>My Resumes</span>
        </button>
      </div>

      {/* TAB 1: IDENTITY & CONTACT */}
      {activeTab === 'identity' && (
        <ProfileIdentityTab
          profileForm={profileForm}
          handleFieldChange={handleFieldChange}
          onSaveProfile={onSaveProfile}
          isSaving={isSaving}
        />
      )}

      {/* TAB 2: WORK EXPERIENCE */}
      {activeTab === 'experience' && (
        <ProfileExperienceTab
          profile={profile}
          handleOpenAddExp={handleOpenAddExp}
          handleOpenEditExp={handleOpenEditExp}
          handleDeleteExp={handleDeleteExp}
        />
      )}

      {/* TAB 3: EDUCATION */}
      {activeTab === 'education' && (
        <ProfileEducationTab
          profile={profile}
          handleOpenAddEdu={handleOpenAddEdu}
          handleOpenEditEdu={handleOpenEditEdu}
          handleDeleteEdu={handleDeleteEdu}
        />
      )}

      {/* TAB 4: SKILLS */}
      {activeTab === 'skills' && (
        <ProfileSkillsTab
          profile={profile}
          newSkillName={newSkillName}
          setNewSkillName={setNewSkillName}
          newSkillCategory={newSkillCategory}
          setNewSkillCategory={setNewSkillCategory}
          newSkillProficiency={newSkillProficiency}
          setNewSkillProficiency={setNewSkillProficiency}
          handleAddSkill={handleAddSkill}
          handleDeleteSkill={handleDeleteSkill}
        />
      )}

      {/* TAB 5: PROJECTS */}
      {activeTab === 'projects' && (
        <ProfileProjectsTab
          profile={profile}
          handleOpenAddProj={handleOpenAddProj}
          handleOpenEditProj={handleOpenEditProj}
          handleDeleteProj={handleDeleteProj}
        />
      )}

      {/* TAB 6: TARGET ROLES & LOCATIONS */}
      {activeTab === 'targets' && (
        <ProfileTargetsTab
          targetDesignations={targetDesignations}
          newRole={newRole}
          setNewRole={setNewRole}
          onAddDesignation={onAddDesignation}
          onDeleteDesignation={onDeleteDesignation}
          targetLocations={targetLocations}
          newLocationName={newLocationName}
          setNewLocationName={setNewLocationName}
          newLocationType={newLocationType}
          setNewLocationType={setNewLocationType}
          newRelocation={newRelocation}
          setNewRelocation={setNewRelocation}
          onAddLocation={onAddLocation}
          onDeleteLocation={onDeleteLocation}
        />
      )}

      {/* TAB 7: MY RESUMES (CV KEEPER & BUILDER LAUNCHER) */}
      {activeTab === 'resumes' && (
        <SavedResumesTab
          accountId={accountId}
          authHeaders={authHeaders}
          showToast={showToast}
          onNavigate={onNavigate}
          profileForm={profileForm}
        />
      )}

      {/* MODAL: ADD / EDIT WORK EXPERIENCE */}
      <ProfileExperienceModal
        isOpen={isExpModalOpen}
        onClose={() => setIsExpModalOpen(false)}
        editingExp={editingExp}
        expForm={expForm}
        setExpForm={setExpForm}
        handleSaveExp={handleSaveExp}
      />

      {/* MODAL: ADD / EDIT EDUCATION */}
      <ProfileEducationModal
        isOpen={isEduModalOpen}
        onClose={() => setIsEduModalOpen(false)}
        editingEdu={editingEdu}
        eduForm={eduForm}
        setEduForm={setEduForm}
        handleSaveEdu={handleSaveEdu}
      />

      {/* MODAL: ADD / EDIT PROJECT */}
      <ProfileProjectModal
        isOpen={isProjModalOpen}
        onClose={() => setIsProjModalOpen(false)}
        editingProj={editingProj}
        projForm={projForm}
        setProjForm={setProjForm}
        handleSaveProj={handleSaveProj}
      />
    </div>
  );
}
