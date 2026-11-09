import React from 'react';
import {
  FileEdit,
  Sparkles,
  Building2,
  MapPin,
  ExternalLink,
  RefreshCw,
  Compass,
  FileText,
  Mail,
  MessageSquare,
  CheckSquare,
} from 'lucide-react';

export default function StudioJobContext({
  channel,
  setChannel,
  activeJobId,
  handleJobSelectChange,
  jobs = [],
  customCompany,
  setCustomCompany,
  customRole,
  setCustomRole,
  currentJobObj,
  salaryDisplay,
  customPostingText,
  setCustomPostingText,
  isEvaluatingFit,
  handleManualAnalyze,
  isDetectingChannel,
  handleDetectChannel,
  isTailoring,
  handleExecuteTailor,
  channelInspection,
  formQuestions = [],
  profile,
  editedOutreachDraft,
  editedCoverDraft,
  setActiveDraftTab,
  fitResult,
}) {
  return (
    <>
      {/* Studio Header */}
      <div className="studio-header panel-card">
        <div className="studio-title-group">
          <FileEdit className="studio-icon" />
          <div>
            <h3>Autonomous Application Studio</h3>
            <p className="studio-subtext">
              Senior Recruiter CV Tailoring, Overleaf-style Interactive LaTeX Compiler, Live A4 PDF Preview & Strict Human Gate.
            </p>
          </div>
        </div>

        <div className="channel-selector-group">
          <label>Target Channel:</label>
          <div className="channel-pills">
            <button
              className={`channel-pill ${channel === 'email' ? 'active' : ''}`}
              onClick={() => setChannel('email')}
            >
              <Mail className="icon-xxs" />
              <span>Email Outreach</span>
            </button>
            <button
              className={`channel-pill ${channel === 'form' ? 'active' : ''}`}
              onClick={() => setChannel('form')}
            >
              <FileText className="icon-xxs" />
              <span>Portal Form</span>
            </button>
            <button
              className={`channel-pill ${channel === 'dm' ? 'active' : ''}`}
              onClick={() => setChannel('dm')}
            >
              <MessageSquare className="icon-xxs" />
              <span>Direct DM</span>
            </button>
          </div>
        </div>
      </div>

      {/* Target Opportunity Selector */}
      <div className="opportunity-selector-panel panel-card">
        <div className="selector-top-row">
          <div className="form-group flex-1">
            <label>Select Opportunity from Ingested Radar:</label>
            <select
              value={activeJobId}
              onChange={handleJobSelectChange}
              className="job-select-input"
            >
              <option value="">-- Choose from Ingested Jobs ({jobs.length}) --</option>
              {jobs.map((j) => (
                <option key={j.id} value={j.id}>
                  {j.title || j.role} @ {j.company} ({j.match_score != null ? Math.round(j.match_score <= 1.0 ? j.match_score * 100 : j.match_score) : '--'}% fit)
                </option>
              ))}
            </select>
          </div>

          <div className="selector-or-divider">OR</div>

          <div className="form-group flex-1">
            <label>Target Company & Role Title:</label>
            <div className="inline-inputs">
              <input
                type="text"
                placeholder="Company Name"
                value={customCompany}
                onChange={(e) => setCustomCompany(e.target.value)}
              />
              <input
                type="text"
                placeholder="Role Title"
                value={customRole}
                onChange={(e) => setCustomRole(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Selected Job Quick Info Bar */}
        {currentJobObj && (
          <div className="studio-job-info-bar">
            <div className="info-meta">
              <Building2 className="icon-xs" />
              <span>{currentJobObj.company}</span>
              <span className="bullet-sep">•</span>
              <MapPin className="icon-xs" />
              <span>{currentJobObj.location || 'Remote'}</span>
              {salaryDisplay && (
                <>
                  <span className="bullet-sep">•</span>
                  <span className="salary-pill-studio">{salaryDisplay.text}</span>
                </>
              )}
            </div>
            {currentJobObj.apply_link && (
              <a
                href={currentJobObj.apply_link}
                target="_blank"
                rel="noreferrer"
                className="external-link-btn"
              >
                <span>View Job Page</span>
                <ExternalLink className="btn-icon-xs" />
              </a>
            )}
          </div>
        )}

        <div className="posting-text-wrapper">
          <label>Job Posting Text / Requirements:</label>
          <textarea
            rows={3}
            placeholder="Paste job posting requirements, key skills, and responsibilities here..."
            value={customPostingText}
            onChange={(e) => setCustomPostingText(e.target.value)}
          />
          <div className="posting-actions-bar">
            <button
              className="action-btn-secondary"
              disabled={isEvaluatingFit || !customPostingText.trim()}
              onClick={handleManualAnalyze}
            >
              {isEvaluatingFit ? <RefreshCw className="btn-icon icon-spin" /> : <Sparkles className="btn-icon" />}
              <span>Run Fit Analysis</span>
            </button>

            <button
              className="action-btn-secondary"
              disabled={isDetectingChannel || (!activeJobId && !customPostingText.trim())}
              onClick={() => handleDetectChannel()}
              title="Autonomous Detective discovers whether target job applies via Google Form, Email, ATS, or DM"
            >
              {isDetectingChannel ? <RefreshCw className="btn-icon icon-spin" /> : <Compass className="btn-icon" />}
              <span>Detect Channel & Forms</span>
            </button>

            <button
              className="action-btn-primary"
              disabled={isTailoring || (!activeJobId && !customPostingText.trim())}
              onClick={handleExecuteTailor}
              title="Tailors CV with 20-year Senior Recruiter intelligence"
            >
              {isTailoring ? (
                <>
                  <RefreshCw className="btn-icon icon-spin" />
                  <span>Senior Recruiter Tailoring...</span>
                </>
              ) : (
                <>
                  <Sparkles className="btn-icon" />
                  <span>Tailor with Senior Recruiter AI</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* AUTONOMOUS APPLY CHANNEL & DISPATCH RADAR */}
      {channelInspection && (
        <div className="channel-intelligence-banner panel-card">
          <div className="channel-banner-left">
            <div className="channel-icon-pill">
              {channelInspection.channel_type === 'google_form' || channelInspection.channel_type === 'typeform' ? (
                <FileText className="channel-type-icon text-emerald" />
              ) : channelInspection.channel_type === 'direct_email' ? (
                <Mail className="channel-type-icon text-cyan" />
              ) : channelInspection.channel_type === 'direct_message' ? (
                <MessageSquare className="channel-type-icon text-indigo" />
              ) : (
                <Building2 className="channel-type-icon text-amber" />
              )}
              <span className="channel-type-label">
                {channelInspection.platform_name || channelInspection.channel_type.toUpperCase()}
              </span>
            </div>

            <div className="channel-banner-info">
              <h4>{channelInspection.action_summary}</h4>
              <div className="channel-banner-meta">
                {channelInspection.recruiter_email && (
                  <span className="meta-tag email">
                    <Mail className="meta-icon" />
                    <strong>Recruiter:</strong> {channelInspection.recruiter_email}
                  </span>
                )}
                {channelInspection.target_handle && (
                  <span className="meta-tag handle">
                    <MessageSquare className="meta-icon" />
                    <strong>Contact:</strong> {channelInspection.target_handle}
                  </span>
                )}
                <span className="meta-tag confidence">
                  <strong>Confidence:</strong> {Math.round(channelInspection.detection_confidence * 100)}%
                </span>
                <span className="meta-tag questions-count">
                  <CheckSquare className="meta-icon" />
                  <strong>{formQuestions.length} Questions Ready</strong>
                </span>
              </div>
            </div>
          </div>

          <div className="channel-banner-actions">
            {channelInspection.apply_url && (
              <a
                href={channelInspection.apply_url}
                target="_blank"
                rel="noreferrer"
                className="action-btn-sm action-btn-accent"
              >
                <span>Open {channelInspection.platform_name}</span>
                <ExternalLink className="btn-icon-xs" />
              </a>
            )}

            {channelInspection.recruiter_email && (
              <a
                href={`mailto:${channelInspection.recruiter_email}?subject=${encodeURIComponent(
                  `Application: ${customRole || 'AI Engineer'} - ${profile?.full_name || 'Niloy Sannyal'}`
                )}&body=${encodeURIComponent(editedOutreachDraft || editedCoverDraft || '')}`}
                className="action-btn-sm action-btn-mailto"
                title="Launch mail client pre-filled with recruiter contact and tailored cover note"
              >
                <Mail className="btn-icon-xs" />
                <span>Launch Mail Draft</span>
              </a>
            )}

            <button
              className="action-btn-sm action-btn-qa"
              onClick={() => setActiveDraftTab('form_qa')}
            >
              <CheckSquare className="btn-icon-xs" />
              <span>Review Form Q&A ({formQuestions.length})</span>
            </button>
          </div>
        </div>
      )}

      {/* FIT ANALYSIS & DIMENSIONS CARD */}
      {fitResult && (
        <div className="fit-analysis-panel panel-card">
          <div className="panel-header">
            <div className="panel-title-group">
              <Sparkles className="panel-icon" />
              <h3>Semantic Fit & Dimension Diagnostics</h3>
            </div>
            <div className="overall-score-pill">
              <span className="pill-number">{fitResult.overall_score}%</span>
              <span className="pill-recommendation">{fitResult.recommendation}</span>
            </div>
          </div>

          <div className="dimensions-grid">
            {/* Technical Skills */}
            <div className="dimension-card">
              <div className="dim-header">
                <strong>Technical Competencies</strong>
                <span className={`dim-badge ${fitResult.technical_skills.verdict === 'STRONG_MATCH' ? 'badge-pass' : 'badge-flag'}`}>
                  {fitResult.technical_skills.verdict}
                </span>
              </div>
              <p className="dim-notes">{fitResult.technical_skills.notes}</p>
              <div className="skills-tags-cloud">
                {fitResult.technical_skills.matched_items.map((skill) => (
                  <span key={skill} className="skill-tag matched">
                    ✓ {skill}
                  </span>
                ))}
                {fitResult.technical_skills.missing_items.map((gap) => (
                  <span key={gap} className="skill-tag gap">
                    ! {gap}
                  </span>
                ))}
              </div>
            </div>

            {/* Location & Logistics */}
            <div className="dimension-card">
              <div className="dim-header">
                <strong>Location & Logistics</strong>
                <span className={`dim-badge ${fitResult.location_logistics.verdict === 'PASS' ? 'badge-pass' : 'badge-fail'}`}>
                  {fitResult.location_logistics.verdict}
                </span>
              </div>
              <p className="dim-notes">{fitResult.location_logistics.notes}</p>
              <div className="skills-tags-cloud">
                {fitResult.location_logistics.matched_items.map((m) => (
                  <span key={m} className="skill-tag matched">
                    ✓ {m}
                  </span>
                ))}
              </div>
            </div>

            {/* Language Gate */}
            <div className="dimension-card">
              <div className="dim-header">
                <strong>Language Gate</strong>
                <span className={`dim-badge ${fitResult.language_gate.verdict === 'PASS' ? 'badge-pass' : 'badge-fail'}`}>
                  {fitResult.language_gate.verdict}
                </span>
              </div>
              <p className="dim-notes">{fitResult.language_gate.notes}</p>
              <div className="skills-tags-cloud">
                {fitResult.language_gate.matched_items.map((l) => (
                  <span key={l} className="skill-tag matched">
                    ✓ {l}
                  </span>
                ))}
              </div>
            </div>

            {/* Dealbreaker Check */}
            <div className="dimension-card">
              <div className="dim-header">
                <strong>Dealbreaker Guard</strong>
                <span className={`dim-badge ${fitResult.dealbreaker_check.verdict === 'PASS' ? 'badge-pass' : 'badge-fail'}`}>
                  {fitResult.dealbreaker_check.verdict}
                </span>
              </div>
              <p className="dim-notes">{fitResult.dealbreaker_check.notes}</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

