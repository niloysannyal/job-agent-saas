import React, { useState } from 'react';
import {
  User,
  Compass,
  DollarSign,
  Globe,
  FileCode,
  Save,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  FileText,
  Copy,
  Download,
} from 'lucide-react';

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
  masterCvLatex = '',
  onSaveMasterCv,
  showToast,
}) {
  const [activeTab, setActiveTab] = useState('personal'); // personal | narrative | roles | locations | comp | latex

  // Local inputs for adding sub-records
  const [newRole, setNewRole] = useState('');
  const [newLocationName, setNewLocationName] = useState('');
  const [newLocationType, setNewLocationType] = useState('remote');
  const [newRelocation, setNewRelocation] = useState(false);
  const [compMin, setCompMin] = useState(compensation.min_salary != null ? String(compensation.min_salary) : '');
  const [compMax, setCompMax] = useState(compensation.max_salary != null ? String(compensation.max_salary) : '');
  const [compCurrency, setCompCurrency] = useState(compensation.currency || 'USD');
  const [compPeriod, setCompPeriod] = useState(compensation.period || 'yearly');
  const [compNegotiable, setCompNegotiable] = useState(compensation.is_negotiable ?? true);
  const [newLangName, setNewLangName] = useState('');
  const [newLangProficiency, setNewLangProficiency] = useState('fluent');
  const [latexSource, setLatexSource] = useState(masterCvLatex || profile?.master_cv_latex || '');

  const handleFieldChange = (e) => {
    const { name, value } = e.target;
    setProfileForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleCopyLatex = () => {
    navigator.clipboard.writeText(latexSource);
    showToast('Master CV LaTeX source copied to clipboard!');
  };

  const handleDownloadLatex = () => {
    const blob = new Blob([latexSource], { type: 'text/x-tex;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = '01_MASTER_CV.tex';
    link.click();
    URL.revokeObjectURL(url);
    showToast('Downloaded 01_MASTER_CV.tex');
  };

  return (
    <div className="section-container profile-view">
      {/* Sub-navigation Tabs */}
      <div className="sub-nav-tabs">
        <button
          className={`sub-tab-btn ${activeTab === 'personal' ? 'active' : ''}`}
          onClick={() => setActiveTab('personal')}
        >
          <User className="tab-icon" />
          <span>Personal Info</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'narrative' ? 'active' : ''}`}
          onClick={() => setActiveTab('narrative')}
        >
          <Compass className="tab-icon" />
          <span>Narrative & Grounding</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'roles' ? 'active' : ''}`}
          onClick={() => setActiveTab('roles')}
        >
          <span>Target Roles ({targetDesignations.length})</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'locations' ? 'active' : ''}`}
          onClick={() => setActiveTab('locations')}
        >
          <Globe className="tab-icon" />
          <span>Locations & Languages</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'comp' ? 'active' : ''}`}
          onClick={() => setActiveTab('comp')}
        >
          <DollarSign className="tab-icon" />
          <span>Compensation</span>
        </button>

        <button
          className={`sub-tab-btn ${activeTab === 'latex' ? 'active' : ''}`}
          onClick={() => setActiveTab('latex')}
        >
          <FileCode className="tab-icon" />
          <span>Master CV LaTeX</span>
        </button>
      </div>

      {/* TAB 1: PERSONAL INFO */}
      {activeTab === 'personal' && (
        <form onSubmit={onSaveProfile} className="profile-form panel-card">
          <div className="panel-header">
            <h3>Candidate Identity & Background</h3>
            <button type="submit" disabled={isSaving} className="action-btn-primary">
              <Save className="btn-icon" />
              <span>{isSaving ? 'Saving...' : 'Save Changes'}</span>
            </button>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                name="full_name"
                value={profileForm.full_name || ''}
                onChange={handleFieldChange}
                required
              />
            </div>

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

            <div className="form-group">
              <label>Education Degree & University</label>
              <input
                type="text"
                name="education"
                value={profileForm.education || ''}
                onChange={handleFieldChange}
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

            <div className="form-group">
              <label>LinkedIn URL</label>
              <input
                type="url"
                name="linkedin_url"
                value={profileForm.linkedin_url || ''}
                onChange={handleFieldChange}
                placeholder="https://linkedin.com/in/..."
              />
            </div>

            <div className="form-group">
              <label>GitHub URL</label>
              <input
                type="url"
                name="github_url"
                value={profileForm.github_url || ''}
                onChange={handleFieldChange}
                placeholder="https://github.com/..."
              />
            </div>
          </div>
        </form>
      )}

      {/* TAB 2: NARRATIVE & GROUNDING */}
      {activeTab === 'narrative' && (
        <form onSubmit={onSaveProfile} className="profile-form panel-card">
          <div className="panel-header">
            <div>
              <h3>Narrative Grounding & Fact Boundaries</h3>
              <p className="panel-subtext">
                Enforced by the CV Tailoring engine to prevent model hallucinations and maintain your authentic voice.
              </p>
            </div>
            <button type="submit" disabled={isSaving} className="action-btn-primary">
              <Save className="btn-icon" />
              <span>{isSaving ? 'Saving...' : 'Save Narrative'}</span>
            </button>
          </div>

          <div className="form-stack">
            <div className="form-group">
              <label>Professional One-Liner</label>
              <input
                type="text"
                name="one_liner"
                value={profileForm.one_liner || ''}
                onChange={handleFieldChange}
                placeholder="AI/ML Engineer building and deploying scalable AI-powered systems..."
              />
            </div>

            <div className="form-group">
              <label>Primary Technical Identity</label>
              <textarea
                rows={2}
                name="primary_identity"
                value={profileForm.primary_identity || ''}
                onChange={handleFieldChange}
              />
            </div>

            <div className="form-group">
              <label>Core Career Narrative</label>
              <textarea
                rows={3}
                name="core_narrative"
                value={profileForm.core_narrative || ''}
                onChange={handleFieldChange}
              />
            </div>

            <div className="form-group">
              <label>Engineering Principle</label>
              <textarea
                rows={2}
                name="engineering_principle"
                value={profileForm.engineering_principle || ''}
                onChange={handleFieldChange}
              />
            </div>

            <div className="form-group">
              <label>Working Style</label>
              <textarea
                rows={2}
                name="working_style"
                value={profileForm.working_style || ''}
                onChange={handleFieldChange}
              />
            </div>

            <div className="form-group">
              <label>Flagship Leadership Example</label>
              <textarea
                rows={3}
                name="leadership_example"
                value={profileForm.leadership_example || ''}
                onChange={handleFieldChange}
              />
            </div>

            <div className="form-grid-2">
              <div className="form-group">
                <label>Tone & Style Preferences</label>
                <textarea
                  rows={3}
                  name="tone_preferences"
                  value={profileForm.tone_preferences || ''}
                  onChange={handleFieldChange}
                  placeholder="Direct, technically precise, concise..."
                />
              </div>

              <div className="form-group">
                <label>Avoid Phrases & Buzzwords</label>
                <textarea
                  rows={3}
                  name="avoid_phrases"
                  value={profileForm.avoid_phrases || ''}
                  onChange={handleFieldChange}
                  placeholder="passionate AI enthusiast, keyword stuffing..."
                />
              </div>
            </div>

            <div className="form-group">
              <label>Dealbreakers (Roles to Automatically Filter)</label>
              <input
                type="text"
                name="dealbreakers"
                value={profileForm.dealbreakers || ''}
                onChange={handleFieldChange}
                placeholder="generic/low-substance roles that don't involve real production systems..."
              />
            </div>
          </div>
        </form>
      )}

      {/* TAB 3: TARGET ROLES */}
      {activeTab === 'roles' && (
        <div className="panel-card roles-panel">
          <div className="panel-header">
            <div>
              <h3>Target Designations & Scoring Priorities</h3>
              <p className="panel-subtext">
                Ranked order of target roles. Higher priority roles receive higher semantic match weighting.
              </p>
            </div>
          </div>

          {/* Add Designation Form */}
          <div className="add-item-bar">
            <input
              type="text"
              placeholder="e.g. Robotics / Embodied AI"
              value={newRole}
              onChange={(e) => setNewRole(e.target.value)}
              className="add-item-input"
            />
            <button
              className="action-btn-primary"
              disabled={!newRole.trim()}
              onClick={() => {
                onAddDesignation(newRole.trim(), targetDesignations.length);
                setNewRole('');
              }}
            >
              <Plus className="btn-icon" />
              <span>Add Designation</span>
            </button>
          </div>

          <div className="designation-list">
            {targetDesignations.map((item, idx) => (
              <div key={item.id || idx} className="designation-row">
                <div className="designation-info">
                  <span className="priority-badge">#{idx + 1}</span>
                  <span className="designation-title">{item.title}</span>
                </div>
                <div className="designation-actions">
                  <button
                    className="delete-icon-btn"
                    onClick={() => onDeleteDesignation(item.id)}
                    title="Remove designation"
                  >
                    <Trash2 className="icon-xs" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: LOCATIONS & LANGUAGES */}
      {activeTab === 'locations' && (
        <div className="locations-languages-grid">
          {/* Target Locations */}
          <div className="panel-card">
            <div className="panel-header">
              <h3>Target Locations & Work Modes</h3>
            </div>

            <div className="add-item-bar">
              <input
                type="text"
                placeholder="e.g. EU (any), Berlin, London"
                value={newLocationName}
                onChange={(e) => setNewLocationName(e.target.value)}
                className="add-item-input"
              />
              <select
                value={newLocationType}
                onChange={(e) => setNewLocationType(e.target.value)}
                className="add-item-select"
              >
                <option value="remote">Remote</option>
                <option value="any">Any / Hybrid</option>
                <option value="onsite">On-site</option>
              </select>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={newRelocation}
                  onChange={(e) => setNewRelocation(e.target.checked)}
                />
                <span>Relocate</span>
              </label>
              <button
                className="action-btn-primary"
                disabled={!newLocationName.trim()}
                onClick={() => {
                  onAddLocation(newLocationName.trim(), newLocationType, newRelocation);
                  setNewLocationName('');
                }}
              >
                <Plus className="btn-icon" />
                <span>Add</span>
              </button>
            </div>

            <div className="item-cards-list">
              {targetLocations.map((loc) => (
                <div key={loc.id} className="item-card-row">
                  <div>
                    <strong>{loc.location_name}</strong>
                    <span className="item-badge">{loc.location_type}</span>
                    {loc.relocation_willing && <span className="item-badge-accent">Relocation OK</span>}
                  </div>
                  <button
                    className="delete-icon-btn"
                    onClick={() => onDeleteLocation(loc.id)}
                  >
                    <Trash2 className="icon-xs" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Spoken Languages */}
          <div className="panel-card">
            <div className="panel-header">
              <h3>Spoken Languages (Language Gate)</h3>
            </div>

            <div className="add-item-bar">
              <input
                type="text"
                placeholder="e.g. English, Bengali, German"
                value={newLangName}
                onChange={(e) => setNewLangName(e.target.value)}
                className="add-item-input"
              />
              <select
                value={newLangProficiency}
                onChange={(e) => setNewLangProficiency(e.target.value)}
                className="add-item-select"
              >
                <option value="native">Native</option>
                <option value="fluent">Fluent</option>
                <option value="professional">Professional</option>
                <option value="intermediate">Intermediate</option>
              </select>
              <button
                className="action-btn-primary"
                disabled={!newLangName.trim()}
                onClick={() => {
                  onAddLanguage(newLangName.trim(), newLangProficiency);
                  setNewLangName('');
                }}
              >
                <Plus className="btn-icon" />
                <span>Add</span>
              </button>
            </div>

            <div className="item-cards-list">
              {languages.map((lang) => (
                <div key={lang.id} className="item-card-row">
                  <div>
                    <strong>{lang.language}</strong>
                    <span className="item-badge">{lang.proficiency}</span>
                  </div>
                  <button
                    className="delete-icon-btn"
                    onClick={() => onDeleteLanguage(lang.id)}
                  >
                    <Trash2 className="icon-xs" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: COMPENSATION */}
      {activeTab === 'comp' && (
        <div className="panel-card comp-panel">
          <div className="panel-header">
            <div>
              <h3>Compensation & Salary Expectations</h3>
              <p className="panel-subtext">
                Used for filtering opportunities and answering application salary screening questions.
              </p>
            </div>
            <button
              className="action-btn-primary"
              onClick={() =>
                onSaveCompensation({
                  min_salary: compMin ? parseFloat(compMin) : null,
                  max_salary: compMax ? parseFloat(compMax) : null,
                  currency: compCurrency,
                  period: compPeriod,
                  is_negotiable: compNegotiable,
                })
              }
            >
              <Save className="btn-icon" />
              <span>Save Compensation</span>
            </button>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Target Minimum Salary</label>
              <input
                type="number"
                value={compMin}
                onChange={(e) => setCompMin(e.target.value)}
                placeholder="e.g. 80000"
              />
            </div>

            <div className="form-group">
              <label>Target Maximum Salary</label>
              <input
                type="number"
                value={compMax}
                onChange={(e) => setCompMax(e.target.value)}
                placeholder="e.g. 130000"
              />
            </div>

            <div className="form-group">
              <label>Currency</label>
              <select
                value={compCurrency}
                onChange={(e) => setCompCurrency(e.target.value)}
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="BDT">BDT (৳)</option>
              </select>
            </div>

            <div className="form-group">
              <label>Period</label>
              <select
                value={compPeriod}
                onChange={(e) => setCompPeriod(e.target.value)}
              >
                <option value="yearly">Yearly</option>
                <option value="monthly">Monthly</option>
                <option value="hourly">Hourly</option>
              </select>
            </div>
          </div>

          <div className="checkbox-block">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={compNegotiable}
                onChange={(e) => setCompNegotiable(e.target.checked)}
              />
              <span>Compensation is negotiable based on equity, ownership, and remote benefits.</span>
            </label>
          </div>
        </div>
      )}

      {/* TAB 6: MASTER CV LATEX */}
      {activeTab === 'latex' && (
        <div className="panel-card latex-panel">
          <div className="panel-header">
            <div>
              <h3>Admin Master LaTeX Template (01_MASTER_CV.tex)</h3>
              <p className="panel-subtext">
                The sole ground-truth source of facts for the CV tailoring pipeline.
              </p>
            </div>
            <div className="panel-btn-group">
              <button className="action-btn-secondary" onClick={handleCopyLatex}>
                <Copy className="btn-icon" />
                <span>Copy Source</span>
              </button>
              <button className="action-btn-secondary" onClick={handleDownloadLatex}>
                <Download className="btn-icon" />
                <span>Download .tex</span>
              </button>
              <button
                className="action-btn-primary"
                onClick={() => onSaveMasterCv(latexSource)}
              >
                <Save className="btn-icon" />
                <span>Save Template</span>
              </button>
            </div>
          </div>

          <div className="latex-editor-wrapper">
            <textarea
              className="latex-textarea"
              rows={24}
              value={latexSource}
              onChange={(e) => setLatexSource(e.target.value)}
              spellCheck={false}
            />
          </div>
        </div>
      )}
    </div>
  );
}

