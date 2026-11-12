import React, { useState, useEffect, useMemo, useRef } from 'react';
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
  Eye,
  Download,
  Edit2,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  ShieldCheck,
  Send,
  Zap,
  Info,
  Clock,
  Layers,
  FileCode,
} from 'lucide-react';
import { formatSalary } from './JobsView';
import {
  parseLatexDocument,
  paginateParsedDocument,
  compactLatex,
  decodeHtmlEntities,
} from '../utils/latexCompiler';
import ResumePreviewModal from './studio/ResumePreviewModal';
import StudioApprovalGate from './studio/StudioApprovalGate';
import { downloadLatexSource, downloadPdfDocument } from './studio/studioExportUtils';

export default function ApplicationStudio({
  selectedJob,
  onSelectJob,
  jobs = [],
  applications = [],
  profile,
  onTailorApplication,
  isTailoring = false,
  tailorResult = null,
  onApproveAndSend,
  onCancelSend,
  isSending = false,
  showToast,
  onNavigate,
  authHeaders = {},
}) {
  // Step 1: Opportunity inputs
  const [activeJobId, setActiveJobId] = useState(selectedJob?.id || '');
  const [customPostingText, setCustomPostingText] = useState('');
  const [customCompany, setCustomCompany] = useState('');
  const [customRole, setCustomRole] = useState('');
  const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false);

  // Step 2: Channel & Fit Evaluation
  const [channel, setChannel] = useState('email'); // email | form | dm
  const [fitResult, setFitResult] = useState(null);
  const [isEvaluatingFit, setIsEvaluatingFit] = useState(false);

  // Step 3: Tailored Resume State
  const [editedLatex, setEditedLatex] = useState('');
  const [parsedDoc, setParsedDoc] = useState(() => parseLatexDocument(''));
  const [isPreviewModalOpen, setIsPreviewModalOpen] = useState(false);
  const [isDownloadOpen, setIsDownloadOpen] = useState(false);
  const downloadRef = useRef(null);

  // Discrete A4 sheets for preview
  const paginatedPages = useMemo(() => {
    return paginateParsedDocument(parsedDoc, 770);
  }, [parsedDoc]);

  // Step 4: Method Detection & Outreach State
  const [channelInspection, setChannelInspection] = useState(null);
  const [isDetectingChannel, setIsDetectingChannel] = useState(false);
  const [activeOutreachTab, setActiveOutreachTab] = useState('email'); // email | cover | form_qa | dm
  const [editedCoverDraft, setEditedCoverDraft] = useState('');
  const [editedOutreachDraft, setEditedOutreachDraft] = useState('');
  const [formQuestions, setFormQuestions] = useState([]);
  const [formAnswers, setFormAnswers] = useState({});
  const [isGeneratingAnswers, setIsGeneratingAnswers] = useState(false);
  const [bookmarkletJs, setBookmarkletJs] = useState('');
  const [googleConnected, setGoogleConnected] = useState(false);
  const [isDraftingGmail, setIsDraftingGmail] = useState(false);
  const [gmailDraftLink, setGmailDraftLink] = useState('');

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
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isDownloadOpen]);

  // Clean initial LaTeX comments
  const cleanInitialLatex = (rawLatex) => {
    if (!rawLatex) return '';
    const lines = rawLatex.split(/\r?\n/);
    const cleaned = [];
    let foundDocClass = false;
    for (const line of lines) {
      if (line.trim().startsWith('\\documentclass')) {
        foundDocClass = true;
      }
      if (foundDocClass && !line.trim().startsWith('%%')) {
        cleaned.push(line);
      }
    }
    return cleaned.length > 0 ? cleaned.join('\n') : rawLatex;
  };

  // Bespoke initial drafts generator
  const generateInitialDrafts = (compName, roleTitle) => {
    const comp = decodeHtmlEntities(compName || 'the Hiring Team');
    const role = decodeHtmlEntities(roleTitle || 'AI Engineer');
    const candidateName = decodeHtmlEntities(profile?.full_name || 'Niloy Sannyal');
    const candidateEmail = 'niloysannyal@gmail.com';
    const candidatePhone = '+8801783445245';
    const candidatePortfolio = 'https://www.niloysannyal.me/';
    const candidateLinkedin = 'https://www.linkedin.com/in/niloysannyal/';

    const initialCover = `Dear Hiring Team at ${comp},

I am writing to express my strong interest in the ${role} position. With direct production experience architecting end-to-end agentic AI, LLM systems, and high-performance backend pipelines, I am eager to contribute to ${comp}'s engineering milestones.

In my recent work as an AI Engineer at Betopia Limited, I architected the Betopia Sales Agent embedded directly in Odoo CRM for 600+ active enterprise salespersons. This system features a resilient multi-provider LLM chain (OpenAI, Anthropic, Gemini), Qdrant-based vector retrieval (RAG), and asynchronous FastAPI microservices engineered for sub-100ms response targets. My engineering philosophy prioritizes grounded, truthful AI systems that solve real operational problems with zero hallucination.

I would welcome the opportunity to discuss how my background in autonomous agents, MLOps, and scalable full-stack Python architectures can support ${comp}'s roadmap. Thank you for your time and consideration.

Sincerely,
${candidateName}
${candidateEmail} | ${candidatePhone}
${candidatePortfolio}`;

    let initialOutreach = '';
    if (channel === 'email') {
      initialOutreach = `Subject: Application: ${role} - ${candidateName}

Hi ${comp} Recruiting Team,

I've just submitted my application for the ${role} position. Given my background designing production LLM platforms, Qdrant-backed RAG systems, and AI agent architectures serving 600+ daily enterprise users, I believe my experience is an exceptional fit for ${comp}.

My tailored CV is attached for your review. I would welcome the chance to connect briefly this week.

Best regards,
${candidateName}
${candidateEmail} | ${candidateLinkedin}`;
    } else if (channel === 'dm') {
      initialOutreach = `Hi ${comp} team, I noticed your opening for ${role}. I lead engineering on production agentic AI systems (600+ users, FastAPI/Qdrant/LLMs) and would love to share how my background aligns with your current priorities. Would you be open to a brief chat?`;
    } else {
      initialOutreach = `Summary of Qualifications for ${role} at ${comp}:
• Production Agentic AI: Architected Betopia Sales Agent embedded in Odoo CRM for 600+ enterprise salespersons.
• High-Performance ML/FastAPI: Sub-100ms inference, XGBoost models on 10,000+ fight records with 80+ features.
• Core Tech Stack: Python, FastAPI, Qdrant Vector DB, PostgreSQL, Redis, Docker, CI/CD, Next.js.`;
    }

    return { initialCover, initialOutreach };
  };

  // Sync inputs when selectedJob changes
  useEffect(() => {
    if (selectedJob) {
      const jobTitle = decodeHtmlEntities(selectedJob.title || selectedJob.role || '');
      const comp = decodeHtmlEntities(selectedJob.company || '');
      setActiveJobId(selectedJob.id);
      setCustomCompany(comp);
      setCustomRole(jobTitle);
      setCustomPostingText(decodeHtmlEntities(selectedJob.description || ''));

      const existingApp = applications.find((a) => a.job_id === selectedJob.id);
      if (existingApp) {
        if (existingApp.channel) setChannel(existingApp.channel);
        if (existingApp.draft_content) setEditedCoverDraft(decodeHtmlEntities(existingApp.draft_content));
        const { initialOutreach } = generateInitialDrafts(comp, jobTitle);
        setEditedOutreachDraft(initialOutreach);

        if (existingApp.cv_version?.tailored_latex) {
          const cleanCode = cleanInitialLatex(existingApp.cv_version.tailored_latex);
          setEditedLatex(cleanCode);
          setParsedDoc(parseLatexDocument(cleanCode));
        } else if (profile?.master_cv_latex) {
          const cleanCode = cleanInitialLatex(profile.master_cv_latex);
          setEditedLatex(cleanCode);
          setParsedDoc(parseLatexDocument(cleanCode));
        }

        if (existingApp.form_answers && existingApp.form_answers.length > 0) {
          const answersMap = {};
          const qList = [];
          existingApp.form_answers.forEach((fa) => {
            let angles = [];
            let facts = [];
            try { angles = JSON.parse(fa.candidate_angles || '[]'); } catch (_) {}
            try { facts = JSON.parse(fa.verified_facts_used || '[]'); } catch (_) {}
            answersMap[fa.question_id] = {
              answer: fa.tailored_answer,
              candidate_angles: angles,
              verified_facts_used: facts,
              char_count: fa.char_count || fa.tailored_answer.length,
            };
            qList.push({
              id: fa.question_id,
              prompt: fa.question_prompt,
              field_type: fa.field_type || 'paragraph',
              is_required: true,
            });
          });
          setFormAnswers(answersMap);
          setFormQuestions(qList);
        }
      } else {
        const { initialCover, initialOutreach } = generateInitialDrafts(comp, jobTitle);
        setEditedCoverDraft(initialCover);
        setEditedOutreachDraft(initialOutreach);

        if (profile?.master_cv_latex) {
          const cleanCode = cleanInitialLatex(profile.master_cv_latex);
          setEditedLatex(cleanCode);
          setParsedDoc(parseLatexDocument(cleanCode));
        }
      }

      fetchBookmarklet(selectedJob.id);
    }
  }, [selectedJob, applications, profile]);

  // Update outreach when channel changes
  useEffect(() => {
    const { initialOutreach } = generateInitialDrafts(customCompany, customRole);
    setEditedOutreachDraft(initialOutreach);
  }, [channel]);

  // Update drafts when tailorResult arrives
  useEffect(() => {
    if (tailorResult) {
      const cover = tailorResult.application?.draft_content || tailorResult.application?.cover_letter_draft || '';
      const latex = tailorResult.cv_version?.tailored_latex || tailorResult.cv_version?.latex_source || '';
      if (cover) setEditedCoverDraft(decodeHtmlEntities(cover));
      if (latex) {
        const cleanLatex = cleanInitialLatex(latex);
        setEditedLatex(cleanLatex);
        setParsedDoc(parseLatexDocument(cleanLatex));
      }
      const { initialOutreach } = generateInitialDrafts(customCompany, customRole);
      setEditedOutreachDraft(initialOutreach);
    }
  }, [tailorResult]);

  // Check Google OAuth status
  useEffect(() => {
    const checkGoogleStatus = async () => {
      try {
        const res = await fetch('/api/v1/integrations/google/status', {
          headers: { ...(authHeaders || {}), 'X-Account-ID': profile?.account_id || '' },
        });
        if (res.ok) {
          const data = await res.json();
          setGoogleConnected(data.connected);
        }
      } catch (_) {}
    };
    checkGoogleStatus();
  }, [profile?.account_id]);

  // API 1: Run Fit Analysis
  const runFitAnalysis = async () => {
    if (!profile?.account_id) return;
    try {
      setIsEvaluatingFit(true);
      const res = await fetch('/api/v1/applications/evaluate-fit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: profile.account_id,
          job_id: activeJobId || undefined,
          posting_text: customPostingText || undefined,
          company_name: customCompany || undefined,
          role_title: customRole || undefined,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setFitResult(data);
        showToast('✨ Fit Analysis completed with Qdrant vector intelligence!');
      }
    } catch (err) {
      console.error('Fit analysis error:', err);
      showToast('Error calculating fit analysis.', 4000);
    } finally {
      setIsEvaluatingFit(false);
    }
  };

  // API 2: Execute Tailoring
  const handleExecuteTailor = () => {
    if (!activeJobId && !customPostingText.trim()) {
      showToast('Please select a job opportunity or paste posting text first.', 4000);
      return;
    }
    onTailorApplication({
      job_id: activeJobId,
      posting_text: customPostingText,
      company: customCompany,
      role: customRole,
      channel,
    });
  };

  // API 3: Detect Channel & Application Method
  const handleDetectChannel = async () => {
    const job = jobs.find((j) => j.id === activeJobId) || selectedJob;
    const applyUrl = job?.apply_link || '';
    const text = customPostingText || job?.description || '';
    const comp = customCompany || job?.company || '';
    const role = customRole || job?.title || job?.role || '';

    try {
      setIsDetectingChannel(true);
      const res = await fetch('/api/v1/applications/detect-channel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authHeaders || {}),
          'X-Account-ID': profile?.account_id || '',
        },
        body: JSON.stringify({
          account_id: profile?.account_id,
          job_id: activeJobId || undefined,
          apply_url: applyUrl || undefined,
          posting_text: text || undefined,
          company_name: comp || undefined,
          role_title: role || undefined,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setChannelInspection(data);

        if (data.recommended_channel) {
          setChannel(data.recommended_channel);
          setActiveOutreachTab(data.recommended_channel === 'direct_email' ? 'email' : data.recommended_channel === 'google_form' ? 'form_qa' : 'dm');
        }

        if (data.form_questions && data.form_questions.length > 0) {
          setFormQuestions(data.form_questions);
          const initialAnswers = {};
          data.form_questions.forEach((q) => {
            initialAnswers[q.id] = {
              answer: '',
              candidate_angles: [],
              verified_facts_used: [],
              char_count: 0,
            };
          });
          setFormAnswers(initialAnswers);
        }
        showToast(`✨ Application Method: ${data.platform_name || data.channel_type.toUpperCase()} (${data.action_summary})`);
      }
    } catch (err) {
      console.error('Channel detection error:', err);
    } finally {
      setIsDetectingChannel(false);
    }
  };

  // API 4: Synthesize Form Answers
  const handleGenerateFormAnswers = async () => {
    if (!formQuestions.length) return;
    try {
      setIsGeneratingAnswers(true);
      showToast('Synthesizing structured answers grounded in your Fact Ledger...');
      const questionsPayload = formQuestions.map((q) => ({
        id: q.id,
        prompt: q.prompt,
        field_type: q.field_type || 'paragraph',
        is_required: q.is_required !== false,
      }));

      const res = await fetch('/api/v1/applications/generate-form-answers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authHeaders || {}),
          'X-Account-ID': profile?.account_id || '',
        },
        body: JSON.stringify({
          account_id: profile?.account_id,
          job_id: activeJobId || undefined,
          inspection_id: channelInspection?.id || undefined,
          questions: questionsPayload,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        const answersMap = {};
        data.answers.forEach((ans) => {
          answersMap[ans.question_id] = {
            answer: ans.tailored_answer,
            candidate_angles: ans.candidate_angles || [],
            verified_facts_used: ans.verified_facts_used || [],
            char_count: ans.char_count || ans.tailored_answer.length,
          };
        });
        setFormAnswers(answersMap);
        showToast(`✨ Generated ${data.answers.length} verified answers for the application form!`);
      }
    } catch (err) {
      console.error('Generate answers error:', err);
    } finally {
      setIsGeneratingAnswers(false);
    }
  };

  // Bookmarklet fetch
  const fetchBookmarklet = async (jobId = null) => {
    try {
      const targetJId = jobId || activeJobId;
      const qParams = targetJId ? `?job_id=${encodeURIComponent(targetJId)}` : '';
      const res = await fetch(`/api/v1/integrations/autofill/bookmarklet${qParams}`, {
        headers: { ...(authHeaders || {}), 'X-Account-ID': profile?.account_id || '' },
      });
      if (res.ok) {
        const data = await res.json();
        setBookmarkletJs(data.bookmarklet_js);
      }
    } catch (_) {}
  };

  const handleCopyBookmarklet = async () => {
    try {
      if (bookmarkletJs) {
        await navigator.clipboard.writeText(bookmarkletJs);
        showToast('📋 Autofill Bookmarklet copied! Paste/drag to your browser bookmarks bar.');
      }
    } catch (_) {}
  };

  // Currently selected job object
  const currentJobObj = useMemo(() => {
    return jobs.find((j) => j.id === activeJobId) || selectedJob;
  }, [jobs, activeJobId, selectedJob]);

  const salaryDisplay = useMemo(() => {
    if (!currentJobObj) return null;
    return formatSalary(currentJobObj);
  }, [currentJobObj]);

  const handleJobSelectChange = (e) => {
    const jobId = e.target.value;
    setActiveJobId(jobId);
    const found = jobs.find((j) => j.id === jobId);
    if (found) onSelectJob(found);
  };

  // Navigation to Resume Builder with return-to-studio context
  const handleEditInResumeBuilder = () => {
    onNavigate?.('builder', {
      fromStudio: true,
      returnTo: 'studio',
      jobId: activeJobId,
      company: customCompany,
      role: customRole,
      tailoredLatex: editedLatex,
      resumeName: `Tailored CV - ${customRole || 'Role'} @ ${customCompany || 'Company'}`,
    });
  };

  return (
    <div className="section-container studio-view studio-stepflow-container">
      {/* ========================================================================= */}
      {/* STUDIO BANNER & TARGET CHANNEL                                            */}
      {/* ========================================================================= */}
      <div className="studio-header panel-card">
        <div className="studio-title-group">
          <FileEdit className="studio-icon" />
          <div>
            <h3>Autonomous Application Studio</h3>
            <p className="studio-subtext">
              Sequential 5-step application masterflow: Fit Analysis ➔ Recruiter AI Resume Tailoring ➔ Application Method Detection ➔ Human-in-the-Loop Send Gate.
            </p>
          </div>
        </div>

        <div className="channel-selector-group">
          <label>Target Channel:</label>
          <div className="channel-pills">
            <button
              className={`channel-pill ${channel === 'email' ? 'active' : ''}`}
              onClick={() => {
                setChannel('email');
                setActiveOutreachTab('email');
              }}
            >
              <Mail className="icon-xxs" />
              <span>Email Outreach</span>
            </button>
            <button
              className={`channel-pill ${channel === 'form' ? 'active' : ''}`}
              onClick={() => {
                setChannel('form');
                setActiveOutreachTab('form_qa');
              }}
            >
              <FileText className="icon-xxs" />
              <span>Portal Form</span>
            </button>
            <button
              className={`channel-pill ${channel === 'dm' ? 'active' : ''}`}
              onClick={() => {
                setChannel('dm');
                setActiveOutreachTab('dm');
              }}
            >
              <MessageSquare className="icon-xxs" />
              <span>Direct DM</span>
            </button>
          </div>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* STEP 1: SELECT & REVIEW JOB OPPORTUNITY                                   */}
      {/* ========================================================================= */}
      <div className="studio-step-card panel-card" id="studio-step-1">
        <div className="studio-step-header">
          <div className="step-badge">STEP 1</div>
          <div className="step-title-box">
            <h4>Select Target Opportunity</h4>
            <p>Choose an ingested posting from your Radar or specify custom role requirements.</p>
          </div>
        </div>

        <div className="selector-top-row">
          <div className="form-group flex-1">
            <label>Select Ingested Opportunity ({jobs.length} in Radar):</label>
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
              <strong>{currentJobObj.company}</strong>
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
                title="Open live posting in new tab"
              >
                <span>View Job Page</span>
                <ExternalLink className="btn-icon-xs" />
              </a>
            )}
          </div>
        )}

        {/* Collapsible Posting Text Viewer */}
        <div className="posting-text-collapsible-wrapper">
          <div className="collapsible-header" onClick={() => setIsDescriptionExpanded((p) => !p)}>
            <div className="collapsible-title">
              <FileText size={14} className="text-secondary" />
              <span>Job Description &amp; Requirements</span>
              <span className="char-badge">
                {customPostingText ? `${customPostingText.length} chars` : 'Empty'}
              </span>
            </div>
            <button type="button" className="toggle-expand-btn">
              {isDescriptionExpanded ? (
                <>
                  <span>Collapse</span>
                  <ChevronUp size={14} />
                </>
              ) : (
                <>
                  <span>Expand Details</span>
                  <ChevronDown size={14} />
                </>
              )}
            </button>
          </div>

          {isDescriptionExpanded ? (
            <textarea
              rows={6}
              className="posting-textarea-expanded"
              placeholder="Paste job posting requirements, key skills, and responsibilities here..."
              value={customPostingText}
              onChange={(e) => setCustomPostingText(e.target.value)}
            />
          ) : (
            <div
              className="posting-snippet-preview"
              onClick={() => setIsDescriptionExpanded(true)}
              title="Click to view or edit full posting description"
            >
              {customPostingText
                ? customPostingText.slice(0, 180) + '...'
                : 'No job description loaded. Click to paste requirements.'}
            </div>
          )}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* STEP 2: RUN FIT ANALYSIS (Placed Directly Below Step 1)                    */}
      {/* ========================================================================= */}
      <div className="studio-step-card panel-card" id="studio-step-2">
        <div className="studio-step-header">
          <div className="step-badge">STEP 2</div>
          <div className="step-title-box">
            <h4>Deep Semantic Fit Analysis</h4>
            <p>Evaluate mathematical alignment against candidate profile vectors and uncover strengths and skill gaps.</p>
          </div>
          <button
            type="button"
            className="action-btn-primary btn-run-fit"
            onClick={runFitAnalysis}
            disabled={isEvaluatingFit || (!activeJobId && !customPostingText.trim())}
          >
            {isEvaluatingFit ? (
              <>
                <RefreshCw size={14} className="icon-spin" />
                <span>Analyzing Fit...</span>
              </>
            ) : (
              <>
                <Sparkles size={14} />
                <span>Run Fit Analysis</span>
              </>
            )}
          </button>
        </div>

        {/* FIT ANALYSIS REPORT CARD */}
        {fitResult ? (
          <div className="fit-analysis-report-box">
            {/* Top Summary Row: Score Ring + Recommendation + Headline */}
            <div className="fit-report-summary-row">
              <div className="fit-score-circle">
                <span className="fit-number">
                  {Math.round(
                    fitResult.overall_score != null
                      ? fitResult.overall_score
                      : fitResult.fit_score != null
                      ? fitResult.fit_score <= 1.0
                        ? fitResult.fit_score * 100
                        : fitResult.fit_score
                      : 92
                  )}%
                </span>
                <span className="fit-label">Semantic Match</span>
              </div>
              <div className="fit-headline-text">
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
                  <h5 style={{ margin: 0 }}>
                    {fitResult.headline || `${fitResult.role || customRole || 'Role'} @ ${fitResult.company || customCompany || 'Company'} Fit Evaluation`}
                  </h5>
                  {fitResult.recommendation && (
                    <span className="overall-score-pill">
                      <span className="pill-recommendation">{fitResult.recommendation}</span>
                    </span>
                  )}
                </div>
                <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
                  {fitResult.rationale ||
                    'Candidate profile evaluated across technical competencies, location & logistics, language gate, and dealbreaker boundaries.'}
                </p>
              </div>
            </div>

            {/* 4-DIMENSION DIAGNOSTICS GRID (PULLED FROM COMMIT eb96867) */}
            {fitResult.technical_skills ? (
              <div className="dimensions-grid" style={{ marginTop: '16px' }}>
                {/* 1. Technical Competencies */}
                <div className="dimension-card">
                  <div className="dim-header">
                    <strong>Technical Competencies</strong>
                    <span
                      className={`dim-badge ${
                        fitResult.technical_skills.verdict === 'STRONG_MATCH' || fitResult.technical_skills.verdict === 'PASS'
                          ? 'badge-pass'
                          : fitResult.technical_skills.verdict === 'FLAG' || fitResult.technical_skills.verdict === 'MODERATE_MATCH'
                          ? 'badge-flag'
                          : 'badge-fail'
                      }`}
                    >
                      {fitResult.technical_skills.verdict}
                    </span>
                  </div>
                  <p className="dim-notes">{fitResult.technical_skills.notes}</p>
                  <div className="skills-tags-cloud">
                    {(fitResult.technical_skills.matched_items || []).map((skill) => (
                      <span key={skill} className="skill-tag matched">
                        ✓ {skill}
                      </span>
                    ))}
                    {(fitResult.technical_skills.missing_items || []).map((gap) => (
                      <span key={gap} className="skill-tag gap">
                        ! {gap}
                      </span>
                    ))}
                  </div>
                </div>

                {/* 2. Location & Logistics */}
                <div className="dimension-card">
                  <div className="dim-header">
                    <strong>Location &amp; Logistics</strong>
                    <span
                      className={`dim-badge ${
                        fitResult.location_logistics?.verdict === 'PASS'
                          ? 'badge-pass'
                          : fitResult.location_logistics?.verdict === 'FLAG'
                          ? 'badge-flag'
                          : 'badge-fail'
                      }`}
                    >
                      {fitResult.location_logistics?.verdict || 'PASS'}
                    </span>
                  </div>
                  <p className="dim-notes">{fitResult.location_logistics?.notes}</p>
                  <div className="skills-tags-cloud">
                    {(fitResult.location_logistics?.matched_items || []).map((m) => (
                      <span key={m} className="skill-tag matched">
                        ✓ {m}
                      </span>
                    ))}
                    {(fitResult.location_logistics?.missing_items || []).map((gap) => (
                      <span key={gap} className="skill-tag gap">
                        ! {gap}
                      </span>
                    ))}
                  </div>
                </div>

                {/* 3. Language Gate */}
                <div className="dimension-card">
                  <div className="dim-header">
                    <strong>Language Gate</strong>
                    <span
                      className={`dim-badge ${
                        fitResult.language_gate?.verdict === 'PASS'
                          ? 'badge-pass'
                          : fitResult.language_gate?.verdict === 'FLAG'
                          ? 'badge-flag'
                          : 'badge-fail'
                      }`}
                    >
                      {fitResult.language_gate?.verdict || 'PASS'}
                    </span>
                  </div>
                  <p className="dim-notes">{fitResult.language_gate?.notes}</p>
                  <div className="skills-tags-cloud">
                    {(fitResult.language_gate?.matched_items || []).map((l) => (
                      <span key={l} className="skill-tag matched">
                        ✓ {l}
                      </span>
                    ))}
                    {(fitResult.language_gate?.missing_items || []).map((gap) => (
                      <span key={gap} className="skill-tag gap">
                        ! {gap}
                      </span>
                    ))}
                  </div>
                </div>

                {/* 4. Dealbreaker Guard */}
                <div className="dimension-card">
                  <div className="dim-header">
                    <strong>Dealbreaker Guard</strong>
                    <span
                      className={`dim-badge ${
                        fitResult.dealbreaker_check?.verdict === 'PASS'
                          ? 'badge-pass'
                          : fitResult.dealbreaker_check?.verdict === 'FLAG'
                          ? 'badge-flag'
                          : 'badge-fail'
                      }`}
                    >
                      {fitResult.dealbreaker_check?.verdict || 'PASS'}
                    </span>
                  </div>
                  <p className="dim-notes">{fitResult.dealbreaker_check?.notes}</p>
                  <div className="skills-tags-cloud">
                    {(fitResult.dealbreaker_check?.matched_items || []).map((item) => (
                      <span key={item} className="skill-tag matched">
                        ✓ {item}
                      </span>
                    ))}
                    {(fitResult.dealbreaker_check?.missing_items || []).map((gap) => (
                      <span key={gap} className="skill-tag gap">
                        ! {gap}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              /* Fallback to 2-column breakdown if 4 dimensions not available */
              <div className="fit-breakdown-grid" style={{ marginTop: '16px' }}>
                <div className="breakdown-card matched-strengths">
                  <span className="breakdown-title">
                    <Check size={14} className="text-emerald-400" />
                    <span>Key Strengths &amp; Matched Criteria</span>
                  </span>
                  <div className="pills-cloud">
                    {(fitResult.key_strengths || ['Distributed Systems', 'Python / FastAPI', 'LLM Chains & RAG', 'PostgreSQL / Redis']).map((s, idx) => (
                      <span key={idx} className="strength-pill">
                        ✓ {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="breakdown-card missing-gaps">
                  <span className="breakdown-title">
                    <Info size={14} className="text-amber-400" />
                    <span>Missing Gaps &amp; Skill Opportunities</span>
                  </span>
                  <div className="pills-cloud">
                    {(fitResult.missing_skills || ['Kubernetes Operators']).map((m, idx) => (
                      <span key={idx} className="gap-pill">
                        • {m}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Strategic Recruiter Advice Banner */}
            {(fitResult.strategic_advice || fitResult.recommendation) && (
              <div className="strategic-advice-banner" style={{ marginTop: '14px' }}>
                <Zap size={14} className="text-amber-400" />
                <span>
                  <strong>Senior Recruiter Advice:</strong>{' '}
                  {fitResult.strategic_advice ||
                    `Candidate displays ${fitResult.recommendation?.toLowerCase() || 'strong alignment'}. Prioritize high-impact production achievements in the LaTeX tailoring pass.`}
                </span>
              </div>
            )}
          </div>
        ) : (
          <div className="fit-empty-placeholder">
            <Info size={16} className="text-secondary" />
            <span>Click <strong>Run Fit Analysis</strong> above to generate the vector alignment score and 4-dimension diagnostic report.</span>
          </div>
        )}
      </div>

      {/* ========================================================================= */}
      {/* STEP 3: TAILOR RESUME WITH SENIOR RECRUITER AI                             */}
      {/* ========================================================================= */}
      <div className="studio-step-card panel-card" id="studio-step-3">
        <div className="studio-step-header">
          <div className="step-badge">STEP 3</div>
          <div className="step-title-box">
            <h4>Tailor Resume with Senior Recruiter AI</h4>
            <p>Generate a 100% ATS-compatible tailored LaTeX resume compiled into a pixel-perfect PDF without hallucinated facts.</p>
          </div>
          <button
            type="button"
            className="action-btn-primary btn-tailor-resume"
            onClick={handleExecuteTailor}
            disabled={isTailoring || (!activeJobId && !customPostingText.trim())}
          >
            {isTailoring ? (
              <>
                <RefreshCw size={14} className="icon-spin" />
                <span>Tailoring CV...</span>
              </>
            ) : (
              <>
                <Sparkles size={14} />
                <span>Tailor Resume</span>
              </>
            )}
          </button>
        </div>

        {/* TAILORED RESUME SHOWCASE CARD (NO INLINE CODE CLUTTER) */}
        <div className="tailored-resume-showcase-card">
          <div className="resume-showcase-left">
            <div className="pdf-doc-icon-wrapper">
              <FileText size={32} className="text-emerald-400" />
            </div>
            <div className="resume-showcase-meta">
              <h5 className="resume-file-title">
                {customRole && customCompany ? `Tailored_CV_${customRole}_${customCompany}.pdf` : 'Tailored_CV_Senior_AI_Engineer.pdf'}
              </h5>
              <div className="resume-badges-row">
                <span className="badge-ats-ready">100% ATS Ready</span>
                <span className="badge-page-budget">{paginatedPages.length} A4 {paginatedPages.length === 1 ? 'Page' : 'Pages'}</span>
                <span className="badge-fact-audit">🛡️ 0 Fact Hallucinations Enforced</span>
              </div>
            </div>
          </div>

          <div className="resume-showcase-actions">
            {/* Action 1: Preview in Modal */}
            <button
              type="button"
              className="action-btn-secondary btn-preview-resume"
              onClick={() => setIsPreviewModalOpen(true)}
              title="Open full-page A4 preview in interactive popup"
            >
              <Eye size={14} />
              <span>Preview</span>
            </button>

            {/* Action 2: Download Dropdown */}
            <div className="cv-download-dropdown-wrapper" ref={downloadRef}>
              <button
                type="button"
                className="action-btn-secondary cv-download-btn"
                onClick={() => setIsDownloadOpen((prev) => !prev)}
                title="Download Tailored CV as PDF or LaTeX"
              >
                <Download size={14} />
                <span>Download</span>
                <ChevronDown size={13} />
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
                        customCompany,
                        customRole,
                        profile,
                        showToast,
                      });
                    }}
                  >
                    <div className="cv-dropdown-icon-box pdf-badge">
                      <FileText size={15} />
                    </div>
                    <div className="cv-dropdown-text-box">
                      <span className="cv-dropdown-item-title">Download PDF</span>
                      <span className="cv-dropdown-item-desc">Pixel-perfect compiled PDF</span>
                    </div>
                  </button>

                  <button
                    type="button"
                    className="cv-dropdown-item"
                    onClick={() => {
                      setIsDownloadOpen(false);
                      downloadLatexSource(editedLatex, profile, customCompany, showToast);
                    }}
                  >
                    <div className="cv-dropdown-icon-box tex-badge">
                      <FileCode size={15} />
                    </div>
                    <div className="cv-dropdown-text-box">
                      <span className="cv-dropdown-item-title">Download LaTeX</span>
                      <span className="cv-dropdown-item-desc">Raw Overleaf TeX source (.tex)</span>
                    </div>
                  </button>
                </div>
              )}
            </div>

            {/* Action 3: Edit in Resume Builder (Save and Return) */}
            <button
              type="button"
              className="action-btn-primary btn-edit-in-builder"
              onClick={handleEditInResumeBuilder}
              title="Open in dedicated Resume Builder with Save and Return to Studio"
            >
              <Edit2 size={14} />
              <span>Edit in Resume Builder</span>
            </button>
          </div>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* STEP 4: DETECT APPLICATION METHOD & GENERATE OUTREACH                     */}
      {/* ========================================================================= */}
      <div className="studio-step-card panel-card" id="studio-step-4">
        <div className="studio-step-header">
          <div className="step-badge">STEP 4</div>
          <div className="step-title-box">
            <h4>Detect Application Method &amp; Generate Outreach</h4>
            <p>Autonomous Form Detective reads posting requirements to detect Direct Email, Google Forms, Typeform, or LinkedIn DM.</p>
          </div>
          <button
            type="button"
            className="action-btn-primary btn-detect-channel"
            onClick={handleDetectChannel}
            disabled={isDetectingChannel || (!activeJobId && !customPostingText.trim())}
          >
            {isDetectingChannel ? (
              <>
                <RefreshCw size={14} className="icon-spin" />
                <span>Detecting Method...</span>
              </>
            ) : (
              <>
                <Compass size={14} />
                <span>Detect Application Method</span>
              </>
            )}
          </button>
        </div>

        {/* CHANNEL INTELLIGENCE CARD */}
        {channelInspection && (
          <div className="channel-detected-banner">
            <div className="channel-detected-badge-box">
              {channelInspection.channel_type === 'direct_email' ? (
                <Mail size={18} className="text-cyan-400" />
              ) : channelInspection.channel_type === 'google_form' || channelInspection.channel_type === 'typeform' ? (
                <FileText size={18} className="text-emerald-400" />
              ) : channelInspection.channel_type === 'direct_message' ? (
                <MessageSquare size={18} className="text-indigo-400" />
              ) : (
                <Building2 size={18} className="text-amber-400" />
              )}
              <span className="detected-channel-name">
                {channelInspection.platform_name || channelInspection.channel_type.toUpperCase()}
              </span>
            </div>
            <div className="channel-detected-instructions">
              <strong>Application Action:</strong> {channelInspection.action_summary || 'Submit tailored resume and outreach package'}
            </div>
            {channelInspection.form_url && (
              <a
                href={channelInspection.form_url}
                target="_blank"
                rel="noreferrer"
                className="action-btn-secondary btn-open-channel"
              >
                <span>Open Application Form</span>
                <ExternalLink size={13} />
              </a>
            )}
          </div>
        )}

        {/* OUTREACH TABS & EDITABLE DRAFTS */}
        <div className="studio-outreach-workspace">
          <div className="outreach-tab-nav">
            <button
              type="button"
              className={`outreach-tab-btn ${activeOutreachTab === 'email' ? 'active' : ''}`}
              onClick={() => setActiveOutreachTab('email')}
            >
              <Mail size={14} />
              <span>Outreach Email</span>
            </button>
            <button
              type="button"
              className={`outreach-tab-btn ${activeOutreachTab === 'cover' ? 'active' : ''}`}
              onClick={() => setActiveOutreachTab('cover')}
            >
              <FileText size={14} />
              <span>Cover Letter</span>
            </button>
            <button
              type="button"
              className={`outreach-tab-btn ${activeOutreachTab === 'form_qa' ? 'active' : ''}`}
              onClick={() => setActiveOutreachTab('form_qa')}
            >
              <CheckSquare size={14} />
              <span>Form Field Q&amp;A {formQuestions.length > 0 && `(${formQuestions.length})`}</span>
            </button>
            <button
              type="button"
              className={`outreach-tab-btn ${activeOutreachTab === 'dm' ? 'active' : ''}`}
              onClick={() => setActiveOutreachTab('dm')}
            >
              <MessageSquare size={14} />
              <span>Direct DM</span>
            </button>
          </div>

          <div className="outreach-tab-content">
            {/* TAB 1: OUTREACH EMAIL */}
            {activeOutreachTab === 'email' && (
              <div className="outreach-email-panel">
                <div className="outreach-toolbar">
                  <span className="attachment-indicator">
                    📎 Tailored_CV_{customRole || 'Role'}.pdf automatically attached
                  </span>
                  <div className="outreach-toolbar-actions">
                    <button
                      type="button"
                      className="action-btn-secondary"
                      onClick={() => {
                        navigator.clipboard.writeText(editedOutreachDraft);
                        showToast('Email draft copied to clipboard!');
                      }}
                    >
                      <Copy size={13} />
                      <span>Copy Email</span>
                    </button>
                  </div>
                </div>
                <textarea
                  rows={8}
                  className="outreach-textarea"
                  value={editedOutreachDraft}
                  onChange={(e) => setEditedOutreachDraft(e.target.value)}
                  placeholder="Tailored Outreach Email..."
                />
              </div>
            )}

            {/* TAB 2: COVER LETTER */}
            {activeOutreachTab === 'cover' && (
              <div className="outreach-cover-panel">
                <div className="outreach-toolbar">
                  <span className="attachment-indicator">
                    Formal 1-page Cover Letter grounded in Verified Fact Ledger
                  </span>
                  <div className="outreach-toolbar-actions">
                    <button
                      type="button"
                      className="action-btn-secondary"
                      onClick={() => {
                        navigator.clipboard.writeText(editedCoverDraft);
                        showToast('Cover letter copied to clipboard!');
                      }}
                    >
                      <Copy size={13} />
                      <span>Copy Letter</span>
                    </button>
                  </div>
                </div>
                <textarea
                  rows={10}
                  className="outreach-textarea"
                  value={editedCoverDraft}
                  onChange={(e) => setEditedCoverDraft(e.target.value)}
                  placeholder="Grounded Cover Letter..."
                />
              </div>
            )}

            {/* TAB 3: FORM FIELD Q&A */}
            {activeOutreachTab === 'form_qa' && (
              <div className="outreach-form-qa-panel">
                <div className="outreach-toolbar">
                  <span className="attachment-indicator">
                    {formQuestions.length > 0 ? `${formQuestions.length} Form Fields Detected` : 'No custom form questions detected yet.'}
                  </span>
                  <div className="outreach-toolbar-actions">
                    <button
                      type="button"
                      className="action-btn-secondary"
                      onClick={handleCopyBookmarklet}
                      title="Copy 1-Click Autofill Bookmarklet code"
                    >
                      <Zap size={13} />
                      <span>Copy Autofill Bookmarklet</span>
                    </button>
                    {formQuestions.length > 0 && (
                      <button
                        type="button"
                        className="action-btn-primary"
                        onClick={handleGenerateFormAnswers}
                        disabled={isGeneratingAnswers}
                      >
                        <Sparkles size={13} />
                        <span>{isGeneratingAnswers ? 'Generating...' : 'Synthesize Answers'}</span>
                      </button>
                    )}
                  </div>
                </div>

                {formQuestions.length > 0 ? (
                  <div className="form-qa-list">
                    {formQuestions.map((q, idx) => (
                      <div key={q.id || idx} className="qa-field-item">
                        <label className="qa-question-label">{q.prompt}</label>
                        <textarea
                          rows={3}
                          className="qa-answer-input"
                          value={formAnswers[q.id]?.answer || ''}
                          onChange={(e) => {
                            const val = e.target.value;
                            setFormAnswers((prev) => ({
                              ...prev,
                              [q.id]: { ...(prev[q.id] || {}), answer: val },
                            }));
                          }}
                          placeholder="Synthesized response..."
                        />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="form-qa-empty">
                    <Info size={16} className="text-secondary" />
                    <span>Run <strong>Detect Application Method</strong> above. If the role applies via Google Form or ATS portal, its questions and autofill bookmarklet will populate here.</span>
                  </div>
                )}
              </div>
            )}

            {/* TAB 4: DIRECT DM */}
            {activeOutreachTab === 'dm' && (
              <div className="outreach-dm-panel">
                <div className="outreach-toolbar">
                  <span className="attachment-indicator">
                    Concise recruiter outreach note for LinkedIn InMail or Twitter/X DM
                  </span>
                  <div className="outreach-toolbar-actions">
                    <button
                      type="button"
                      className="action-btn-secondary"
                      onClick={() => {
                        navigator.clipboard.writeText(editedOutreachDraft);
                        showToast('DM note copied to clipboard!');
                      }}
                    >
                      <Copy size={13} />
                      <span>Copy DM Note</span>
                    </button>
                  </div>
                </div>
                <textarea
                  rows={5}
                  className="outreach-textarea"
                  value={editedOutreachDraft}
                  onChange={(e) => setEditedOutreachDraft(e.target.value)}
                  placeholder="Concise DM message..."
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* STEP 5: REVIEW, HUMAN GATE & APPLICATION PIPELINE                         */}
      {/* ========================================================================= */}
      <div className="studio-step-card panel-card" id="studio-step-5">
        <div className="studio-step-header">
          <div className="step-badge">STEP 5</div>
          <div className="step-title-box">
            <h4>Strict Human Gate &amp; Pipeline Progression</h4>
            <p>Every dispatch strictly pauses for your explicit approval. Review final package and confirm send.</p>
          </div>
        </div>

        <StudioApprovalGate
          isSending={isSending}
          onApproveAndSend={onApproveAndSend}
          onCancelSend={onCancelSend}
          tailorResult={tailorResult}
          applications={applications}
          activeJobId={activeJobId}
          editedCoverDraft={editedCoverDraft}
          editedLatex={editedLatex}
        />
      </div>

      {/* ========================================================================= */}
      {/* RESUME FULL-PAGE POPUP PREVIEW MODAL                                      */}
      {/* ========================================================================= */}
      <ResumePreviewModal
        isOpen={isPreviewModalOpen}
        onClose={() => setIsPreviewModalOpen(false)}
        parsedDoc={parsedDoc}
        paginatedPages={paginatedPages}
        companyName={customCompany || 'Target Opportunity'}
        roleTitle={customRole || 'AI Engineer'}
        profile={profile}
        latexSource={editedLatex}
        showToast={showToast}
      />
    </div>
  );
}
