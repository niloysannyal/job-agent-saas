import React, { useState } from 'react';
import {
  Upload,
  FileText,
  CheckCircle,
  Briefcase,
  GraduationCap,
  Sparkles,
  ArrowRight,
  ArrowLeft,
  X,
  Code,
  Layout,
  Layers,
} from 'lucide-react';

export default function OnboardingModal({
  isOpen,
  onClose,
  accountId,
  authHeaders = {},
  onComplete,
  showToast,
}) {
  const [step, setStep] = useState(1); // 1: Upload, 2: Review, 3: Template
  const [file, setFile] = useState(null);
  const [isParsing, setIsParsing] = useState(false);
  const [parsedData, setParsedData] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState('01_MODERN_TECH');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Editable review form state
  const [formData, setFormData] = useState({
    full_name: '',
    headline: '',
    phone: '',
    summary: '',
    location_city: '',
    location_country: '',
    target_designations: [],
    work_experiences: [],
    educations: [],
    skills: [],
    projects: [],
    certifications: [],
  });

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleParseCv = async () => {
    if (!file) {
      showToast?.('Please choose a PDF or DOCX resume to upload.');
      return;
    }
    try {
      setIsParsing(true);
      const data = new FormData();
      data.append('file', file);

      const res = await fetch(`/api/v1/profile/parse-cv?account_id=${accountId}`, {
        method: 'POST',
        headers: {
          ...authHeaders,
        },
        body: data,
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Failed to parse CV.' }));
        throw new Error(err.detail || 'Failed to parse CV.');
      }

      const json = await res.json();
      const extracted = json.data;
      setParsedData(extracted);
      setFormData({
        full_name: extracted.full_name || '',
        headline: extracted.headline || '',
        phone: extracted.phone || '',
        summary: extracted.summary || '',
        location_city: extracted.location_city || '',
        location_country: extracted.location_country || '',
        target_designations: extracted.target_designations || [],
        work_experiences: extracted.work_experiences || [],
        educations: extracted.educations || [],
        skills: extracted.skills || [],
        projects: extracted.projects || [],
        certifications: extracted.certifications || [],
      });

      showToast?.('CV parsed successfully! Review your structured career data.');
      setStep(2);
    } catch (err) {
      showToast?.(err.message || 'Error parsing CV file.');
    } finally {
      setIsParsing(false);
    }
  };

  const handleSaveAndFinish = async () => {
    try {
      setIsSubmitting(true);
      // 1. Apply parsed data
      const applyRes = await fetch(`/api/v1/profile/apply-parsed-cv?account_id=${accountId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify(formData),
      });

      if (!applyRes.ok) {
        throw new Error('Failed to save profile career details.');
      }

      showToast?.('Career profile and CV template initialized successfully!');
      if (onComplete) onComplete();
      onClose();
    } catch (err) {
      showToast?.(err.message || 'Error finalizing onboarding.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-content onboarding-modal-container">
        {/* Header */}
        <div className="modal-header">
          <div className="header-badge-title">
            <span className="brand-pill">⚡ 60-Second Onboarding</span>
            <h2>Set Up Your Career Profile</h2>
          </div>
          <button className="btn-icon-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {/* Stepper Progress */}
        <div className="onboarding-stepper">
          <div className={`step-node ${step >= 1 ? 'active' : ''}`}>
            <span className="node-num">1</span>
            <span className="node-label">Upload CV</span>
          </div>
          <div className="step-line" />
          <div className={`step-node ${step >= 2 ? 'active' : ''}`}>
            <span className="node-num">2</span>
            <span className="node-label">Review Career Data</span>
          </div>
          <div className="step-line" />
          <div className={`step-node ${step >= 3 ? 'active' : ''}`}>
            <span className="node-num">3</span>
            <span className="node-label">Select Template</span>
          </div>
        </div>

        {/* Modal Body */}
        <div className="onboarding-body">
          {/* STEP 1: UPLOAD */}
          {step === 1 && (
            <div className="onboarding-step-content step-upload">
              <p className="step-desc">
                Upload your existing resume (PDF, DOCX, or TXT). Our AI parses your work history, education,
                skills, and projects into structured data without any manual data entry.
              </p>

              <div className="dropzone-box">
                <Upload className="dropzone-icon" size={44} />
                <h3>Drag & Drop your resume file here</h3>
                <p>Supports PDF, Word (.docx), or plain text format</p>

                <input
                  type="file"
                  id="cv-file-input"
                  className="hidden-file-input"
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileChange}
                />
                <label htmlFor="cv-file-input" className="btn-select-file">
                  {file ? file.name : 'Browse Files'}
                </label>
              </div>

              {file && (
                <div className="selected-file-banner">
                  <FileText className="file-icon" size={20} />
                  <span className="file-name">{file.name} ({(file.size / 1024).toFixed(1)} KB)</span>
                  <CheckCircle className="check-icon" size={18} />
                </div>
              )}

              <div className="step-actions right-align">
                <button
                  className="action-btn-primary"
                  onClick={handleParseCv}
                  disabled={!file || isParsing}
                >
                  <Sparkles size={16} />
                  <span>{isParsing ? 'Analyzing with AI...' : 'Parse & Pre-Fill Profile'}</span>
                </button>
              </div>
            </div>
          )}

          {/* STEP 2: REVIEW */}
          {step === 2 && (
            <div className="onboarding-step-content step-review">
              <p className="step-desc">
                Review your extracted career identity. Everything is fully editable anytime.
              </p>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Full Name</label>
                  <input
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Professional Headline</label>
                  <input
                    type="text"
                    value={formData.headline}
                    onChange={(e) => setFormData({ ...formData, headline: e.target.value })}
                    placeholder="e.g. Senior Backend Engineer"
                  />
                </div>
              </div>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Phone / WhatsApp</label>
                  <input
                    type="text"
                    value={formData.phone || ''}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    placeholder="+1 555-0199"
                  />
                </div>
                <div className="form-group">
                  <label>Location (City, Country)</label>
                  <input
                    type="text"
                    value={[formData.location_city, formData.location_country].filter(Boolean).join(', ')}
                    onChange={(e) => {
                      const parts = e.target.value.split(',');
                      setFormData({
                        ...formData,
                        location_city: parts[0]?.trim() || '',
                        location_country: parts[1]?.trim() || '',
                      });
                    }}
                    placeholder="London, United Kingdom"
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Executive Career Summary</label>
                <textarea
                  rows={3}
                  value={formData.summary}
                  onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
                />
              </div>

              {/* Extracted Stats Badges */}
              <div className="extracted-stats-row">
                <div className="stat-pill">
                  <Briefcase size={16} />
                  <span>{formData.work_experiences.length} Work Experiences</span>
                </div>
                <div className="stat-pill">
                  <GraduationCap size={16} />
                  <span>{formData.educations.length} Degrees</span>
                </div>
                <div className="stat-pill">
                  <Code size={16} />
                  <span>{formData.skills.length} Extracted Skills</span>
                </div>
              </div>

              <div className="step-actions split-align">
                <button className="action-btn-secondary" onClick={() => setStep(1)}>
                  <ArrowLeft size={16} /> Back
                </button>
                <button className="action-btn-primary" onClick={() => setStep(3)}>
                  Next: Choose CV Template <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}

          {/* STEP 3: TEMPLATE SELECTOR */}
          {step === 3 && (
            <div className="onboarding-step-content step-templates">
              <p className="step-desc">
                Choose an admin-curated LaTeX template. Candidates never need to write raw LaTeX code;
                the system dynamically compiles your data into pixel-perfect PDF applications.
              </p>

              <div className="template-cards-grid">
                {/* Template 1 */}
                <div
                  className={`template-select-card ${selectedTemplate === '01_MODERN_TECH' ? 'selected' : ''}`}
                  onClick={() => setSelectedTemplate('01_MODERN_TECH')}
                >
                  <div className="template-icon-wrap">
                    <Code size={24} />
                  </div>
                  <h4>Modern Tech (Source Sans)</h4>
                  <p>Clean, crisp typography with compact headings. Tailored for engineering, software, and tech roles.</p>
                  <span className="template-badge">Default Recommended</span>
                </div>

                {/* Template 2 */}
                <div
                  className={`template-select-card ${selectedTemplate === '02_CLASSIC_CORPORATE' ? 'selected' : ''}`}
                  onClick={() => setSelectedTemplate('02_CLASSIC_CORPORATE')}
                >
                  <div className="template-icon-wrap">
                    <Layout size={24} />
                  </div>
                  <h4>Classic Corporate (Times)</h4>
                  <p>Traditional serif styling with standard margins. Ideal for management, finance, ops, and corporate.</p>
                  <span className="template-badge">Corporate Standard</span>
                </div>

                {/* Template 3 */}
                <div
                  className={`template-select-card ${selectedTemplate === '03_MINIMALIST_COMPACT' ? 'selected' : ''}`}
                  onClick={() => setSelectedTemplate('03_MINIMALIST_COMPACT')}
                >
                  <div className="template-icon-wrap">
                    <Layers size={24} />
                  </div>
                  <h4>Minimalist Compact (Helvetica)</h4>
                  <p>High-density, 1-page layout maximizing bullet space. Perfect for senior leaders with extensive history.</p>
                  <span className="template-badge">High Density</span>
                </div>
              </div>

              <div className="step-actions split-align">
                <button className="action-btn-secondary" onClick={() => setStep(2)}>
                  <ArrowLeft size={16} /> Back
                </button>
                <button
                  className="action-btn-primary"
                  onClick={handleSaveAndFinish}
                  disabled={isSubmitting}
                >
                  <CheckCircle size={16} />
                  <span>{isSubmitting ? 'Saving Profile...' : 'Complete & Launch Career Radar'}</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

