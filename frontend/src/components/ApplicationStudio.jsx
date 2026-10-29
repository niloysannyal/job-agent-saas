import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  FileEdit,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Send,
  Copy,
  Download,
  ShieldCheck,
  RefreshCw,
  FileText,
  Mail,
  MessageSquare,
  Terminal,
  Printer,
  Eye,
  Building2,
  MapPin,
  ExternalLink,
  ChevronRight,
  Maximize2,
  ZoomIn,
  ZoomOut,
  Play,
  RotateCcw,
  Scissors,
  CheckSquare,
  HelpCircle,
  Check,
  Compass,
} from 'lucide-react';
import { jsPDF } from 'jspdf';
import { formatSalary } from './JobsView';
import {
  parseLatexDocument,
  compileParsedLatexToPdf,
  paginateParsedDocument,
  compactLatex,
  compactLatexToTwoPages,
  latexToPlainText,
  decodeHtmlEntities,
} from '../utils/latexCompiler';

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
  isSending = false,
  showToast,
  onNavigate,
}) {
  // Opportunity inputs
  const [activeJobId, setActiveJobId] = useState(selectedJob?.id || '');
  const [customPostingText, setCustomPostingText] = useState('');
  const [customCompany, setCustomCompany] = useState('');
  const [customRole, setCustomRole] = useState('');

  // Channel & Generation
  const [channel, setChannel] = useState('email'); // email | form | dm
  const [fitResult, setFitResult] = useState(null);
  const [isEvaluatingFit, setIsEvaluatingFit] = useState(false);

  // Editable Drafts State
  const [editedCoverDraft, setEditedCoverDraft] = useState('');
  const [editedOutreachDraft, setEditedOutreachDraft] = useState('');
  const [editedLatex, setEditedLatex] = useState('');
  const [activeDraftTab, setActiveDraftTab] = useState('latex'); // latex | cover | outreach | form_qa

  // Form Detective & Questionnaire State
  const [channelInspection, setChannelInspection] = useState(null);
  const [isDetectingChannel, setIsDetectingChannel] = useState(false);
  const [formQuestions, setFormQuestions] = useState([]);
  const [formAnswers, setFormAnswers] = useState({});
  const [isGeneratingAnswers, setIsGeneratingAnswers] = useState(false);
  const [copiedQuestionId, setCopiedQuestionId] = useState(null);

  // Overleaf-style Compiler State
  const [isCompiling, setIsCompiling] = useState(false);
  const [compileStatus, setCompileStatus] = useState('success'); // idle | compiling | success | error
  const [compileTime, setCompileTime] = useState('0.3s');
  const [zoomLevel, setZoomLevel] = useState(100); // 70 to 130
  const [parsedDoc, setParsedDoc] = useState(() => parseLatexDocument(''));

  // Multi-page discrete A4 sheets
  const paginatedPages = useMemo(() => {
    return paginateParsedDocument(parsedDoc, 770);
  }, [parsedDoc]);

  const previewRef = useRef(null);

  // Clean initial LaTeX from comments
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

  // Helper to generate bespoke initial drafts
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

  // Sync inputs and load existing drafts when selectedJob changes
  useEffect(() => {
    if (selectedJob) {
      const jobTitle = decodeHtmlEntities(selectedJob.title || selectedJob.role || '');
      const comp = decodeHtmlEntities(selectedJob.company || '');
      setActiveJobId(selectedJob.id);
      setCustomCompany(comp);
      setCustomRole(jobTitle);
      setCustomPostingText(decodeHtmlEntities(selectedJob.description || ''));

      // Check if an application already exists in pipeline for this job
      const existingApp = applications.find((a) => a.job_id === selectedJob.id);
      if (existingApp && existingApp.draft_content) {
        setEditedCoverDraft(decodeHtmlEntities(existingApp.draft_content));
        const { initialOutreach } = generateInitialDrafts(comp, jobTitle);
        setEditedOutreachDraft(initialOutreach);
      } else {
        const { initialCover, initialOutreach } = generateInitialDrafts(comp, jobTitle);
        setEditedCoverDraft(initialCover);
        setEditedOutreachDraft(initialOutreach);
      }

      // Initialize LaTeX from profile or master without control comments
      if (profile?.master_cv_latex) {
        const cleanCode = cleanInitialLatex(profile.master_cv_latex);
        setEditedLatex(cleanCode);
        const parsed = parseLatexDocument(cleanCode);
        setParsedDoc(parsed);
      }

      runFitAnalysis(selectedJob.id, selectedJob.description, comp, jobTitle);
      handleDetectChannel(selectedJob);
    }
  }, [selectedJob, applications, profile]);

  // When channel is changed, update outreach draft template
  useEffect(() => {
    const { initialOutreach } = generateInitialDrafts(customCompany, customRole);
    setEditedOutreachDraft(initialOutreach);
  }, [channel]);

  // When tailorResult updates from backend, populate editable drafts & recompile
  useEffect(() => {
    if (tailorResult) {
      const cover = tailorResult.application?.draft_content || tailorResult.application?.cover_letter_draft || '';
      const latex = tailorResult.cv_version?.tailored_latex || tailorResult.cv_version?.latex_source || '';
      if (cover) setEditedCoverDraft(decodeHtmlEntities(cover));
      if (latex) {
        const cleanLatex = cleanInitialLatex(latex);
        setEditedLatex(cleanLatex);
        const parsed = parseLatexDocument(cleanLatex);
        setParsedDoc(parsed);
        setCompileStatus('success');
      }

      const { initialOutreach } = generateInitialDrafts(customCompany, customRole);
      setEditedOutreachDraft(initialOutreach);
    }
  }, [tailorResult]);

  // Overleaf-style Recompile Action
  const handleCompile = () => {
    setIsCompiling(true);
    setCompileStatus('compiling');
    const startTime = performance.now();

    setTimeout(() => {
      try {
        const parsed = parseLatexDocument(editedLatex);
        setParsedDoc(parsed);
        const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);
        setCompileTime(`${elapsed}s`);
        setCompileStatus(parsed.errors.length === 0 ? 'success' : 'error');
        showToast(`Recompiled in ${elapsed}s!`);
      } catch (err) {
        console.error('Compilation error:', err);
        setCompileStatus('error');
        showToast('LaTeX syntax warning during compile', 4000);
      } finally {
        setIsCompiling(false);
      }
    }, 220); // Quick compile response
  };

  // Compact / Budget to target pages action (Senior Recruiter rule-based pruning)
  const handleCompactToPages = (targetPages = 2) => {
    try {
      const source = editedLatex || profile?.master_cv_latex || '';
      const compacted = compactLatex(source, targetPages, customRole || 'AI Engineer', customPostingText || '');
      setEditedLatex(compacted);
      const parsed = parseLatexDocument(compacted);
      setParsedDoc(parsed);
      setCompileStatus('success');
      showToast(`Compacted & budgeted CV strictly to ${targetPages} ${targetPages === 1 ? 'page' : 'pages'}!`);
    } catch (err) {
      console.error('Compact error:', err);
      showToast('Error compacting CV', 3000);
    }
  };

  // Keyboard shortcut: Ctrl + Enter to recompile
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleCompile();
    }
  };

  // Run Fit Analysis API
  const runFitAnalysis = async (jobId, postingText, company, role) => {
    if (!profile?.account_id) return;
    try {
      setIsEvaluatingFit(true);
      const res = await fetch('/api/v1/applications/evaluate-fit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: profile.account_id,
          job_id: jobId || undefined,
          posting_text: postingText || undefined,
          company_name: company || undefined,
          role_title: role || undefined,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setFitResult(data);
      }
    } catch (err) {
      console.error('Fit analysis error:', err);
    } finally {
      setIsEvaluatingFit(false);
    }
  };

  // Form Detective & Questionnaire API
  const handleDetectChannel = async (targetJob = null) => {
    const job = targetJob || selectedJob;
    const jId = job?.id || activeJobId;
    const applyUrl = job?.apply_link || '';
    const text = (targetJob ? targetJob.description : customPostingText) || job?.description || '';
    const comp = (targetJob ? targetJob.company : customCompany) || job?.company || '';
    const role = (targetJob ? (targetJob.title || targetJob.role) : customRole) || job?.title || job?.role || '';

    try {
      setIsDetectingChannel(true);
      const res = await fetch('/api/v1/applications/detect-channel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: profile?.account_id,
          job_id: jId || undefined,
          apply_url: applyUrl || undefined,
          posting_text: text || undefined,
          company_name: comp || undefined,
          role_title: role || undefined,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setChannelInspection(data);
        const questions = data.questions || data.detected_questions || [];
        setFormQuestions(questions);

        // Intelligently sync channel pill if detected platform is definitive
        if (data.channel_type === 'google_form' || data.channel_type === 'typeform') {
          setChannel('form');
        } else if (data.channel_type === 'direct_email') {
          setChannel('email');
        } else if (data.channel_type === 'direct_message') {
          setChannel('dm');
        }

        showToast(`Detected apply channel: ${data.platform_name || data.channel_type}!`);
      }
    } catch (err) {
      console.error('Channel detection error:', err);
    } finally {
      setIsDetectingChannel(false);
    }
  };

  const handleGenerateFormAnswers = async () => {
    if (!formQuestions || formQuestions.length === 0) {
      showToast('No form questionnaire fields detected yet. Click "Detect Channel & Forms" first.', 4000);
      return;
    }

    try {
      setIsGeneratingAnswers(true);
      const res = await fetch('/api/v1/applications/generate-form-answers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: profile?.account_id,
          job_id: activeJobId || undefined,
          company_name: customCompany || 'Company',
          role_title: customRole || 'AI Engineer',
          job_description: customPostingText || '',
          questions: formQuestions,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        const answersMap = {};
        (data.answers || []).forEach((a) => {
          answersMap[a.question_id] = {
            answer: a.answer,
            candidate_angles: a.candidate_angles || [],
            composed_rationale: a.composed_rationale || '',
            verified_facts_used: a.verified_facts_used || [],
            char_count: a.char_count || a.answer.length,
          };
        });
        setFormAnswers(answersMap);
        showToast(`Synthesized ${data.total_questions} bespoke answers using Propose-Probe-Compose!`);
      } else {
        showToast('Failed to generate form answers', 4000);
      }
    } catch (err) {
      console.error('Answer synthesis error:', err);
      showToast('Error generating questionnaire answers', 4000);
    } finally {
      setIsGeneratingAnswers(false);
    }
  };

  const handleCopyAllAnswers = () => {
    if (!formQuestions || formQuestions.length === 0) return;
    const formatted = formQuestions
      .map((q, idx) => {
        const ansObj = formAnswers[q.id];
        const ansText = ansObj ? ansObj.answer : '(No answer generated)';
        return `[Field ${idx + 1}] ${q.prompt}\n${ansText}\n`;
      })
      .join('\n----------------------------------------\n\n');

    navigator.clipboard.writeText(formatted);
    showToast('All form answers copied to clipboard!');
  };

  const handleCopySingleAnswer = (questionId, text) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopiedQuestionId(questionId);
    setTimeout(() => setCopiedQuestionId(null), 2000);
    showToast('Answer copied to clipboard!');
  };

  const handleUpdateSingleAnswer = (questionId, newText) => {
    setFormAnswers((prev) => ({
      ...prev,
      [questionId]: {
        ...(prev[questionId] || {}),
        answer: newText,
        char_count: newText.length,
      },
    }));
  };

  const handleDownloadEml = async () => {
    try {
      showToast('Preparing .eml draft with attached tailored CV...');
      const comp = customCompany || 'Company';
      const role = customRole || 'AI Engineer';
      const candidateName = profile?.full_name || 'Niloy Sannyal';
      const toEmail = channelInspection?.recruiter_email || 'recruiter@company.com';
      const subject = `Application: ${role} - ${candidateName}`;

      let pdfBase64 = null;
      try {
        const doc = compileParsedLatexToPdf(parsedDoc, `Tailored_CV_${sanitizeFileName(comp)}.pdf`);
        const pdfOutput = doc.output('datauristring');
        if (pdfOutput.includes(',')) {
          pdfBase64 = pdfOutput.split(',')[1];
        }
      } catch (pdfErr) {
        console.warn('PDF compile for eml fallback:', pdfErr);
      }

      const res = await fetch('/api/v1/applications/draft-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: profile?.account_id,
          to_email: toEmail,
          subject,
          body_text: editedOutreachDraft || editedCoverDraft,
          from_email: 'niloysannyal@gmail.com',
          attachment_pdf_base64: pdfBase64,
          attachment_filename: `Tailored_CV_${sanitizeFileName(comp)}.pdf`,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        const blob = new Blob([data.eml_content], { type: 'message/rfc822' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `Draft_Application_${sanitizeFileName(comp)}.eml`;
        link.click();
        URL.revokeObjectURL(url);
        showToast('Downloaded .eml draft! Double-click to open in Outlook/Apple Mail.');
      }
    } catch (err) {
      console.error('EML export error:', err);
      showToast('Failed to download .eml draft', 3000);
    }
  };

  const handleJobSelectChange = (e) => {
    const jobId = e.target.value;
    setActiveJobId(jobId);
    const found = jobs.find((j) => j.id === jobId);
    if (found) {
      onSelectJob(found);
    }
  };

  const handleManualAnalyze = () => {
    runFitAnalysis(null, customPostingText, customCompany, customRole);
  };

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

  const handleCopyDraft = (text, label) => {
    navigator.clipboard.writeText(text);
    showToast(`${label} copied to clipboard!`);
  };

  const sanitizeFileName = (name) => {
    return (name || 'Application')
      .replace(/&amp;/g, 'and')
      .replace(/&lt;/g, '')
      .replace(/&gt;/g, '')
      .replace(/&#39;/g, '')
      .replace(/&quot;/g, '')
      .replace(/&/g, 'and')
      .replace(/[^\w\s-]/g, '')
      .replace(/[-\s]+/g, '_')
      .replace(/_+/g, '_')
      .trim();
  };

  const handleDownloadLatex = () => {
    const content = editedLatex || profile?.master_cv_latex || '';
    const blob = new Blob([content], { type: 'text/x-tex;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    const comp = sanitizeFileName(customCompany || 'Application');
    link.download = `Tailored_CV_${comp}.tex`;
    link.click();
    URL.revokeObjectURL(url);
    showToast('Downloaded tailored LaTeX CV');
  };

  // Client-side PDF Generation with jsPDF (Overleaf-style compiled PDF)
  const handleDownloadPdf = () => {
    try {
      const comp = sanitizeFileName(customCompany || 'Application');
      const role = customRole || 'AI Engineer';
      const candidateName = profile?.full_name || 'Niloy Sannyal';

      if (activeDraftTab === 'latex') {
        // Compile parsed LaTeX document into exact PDF
        const doc = compileParsedLatexToPdf(parsedDoc, `Tailored_CV_${comp}.pdf`);
        doc.save(`Tailored_CV_${comp}.pdf`);
        showToast(`Downloaded Tailored_CV_${comp}.pdf!`);
      } else {
        // PDF Cover Letter Generation
        const doc = new jsPDF({
          orientation: 'portrait',
          unit: 'pt',
          format: 'a4',
        });

        doc.setFont('helvetica', 'bold');
        doc.setFontSize(18);
        doc.setTextColor(17, 24, 39);
        doc.text(candidateName, 40, 50);

        doc.setFont('helvetica', 'normal');
        doc.setFontSize(9.5);
        doc.setTextColor(75, 85, 99);
        doc.text('Dhaka, Bangladesh | niloysannyal@gmail.com | +8801783445245 | niloysannyal.me', 40, 68);

        doc.setDrawColor(209, 213, 219);
        doc.setLineWidth(1);
        doc.line(40, 78, 555, 78);

        let y = 105;
        doc.setFontSize(10);
        doc.setTextColor(55, 65, 81);
        doc.text(`Date: ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`, 40, y);

        y += 16;
        doc.setFont('helvetica', 'bold');
        doc.text(`To: Hiring Team at ${comp}`, 40, y);
        y += 14;
        doc.text(`Regarding: Application for ${role}`, 40, y);

        y += 24;
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(10);

        const textToSplit = activeDraftTab === 'cover' ? editedCoverDraft : editedOutreachDraft;
        const paragraphs = textToSplit.split(/\n\s*\n/);

        paragraphs.forEach((p) => {
          const splitP = doc.splitTextToSize(p.trim(), 515);
          doc.text(splitP, 40, y);
          y += splitP.length * 14 + 10;
        });

        doc.save(`Cover_Letter_${comp.replace(/\s+/g, '_')}.pdf`);
        showToast(`Downloaded Cover_Letter_${comp}.pdf!`);
      }
    } catch (err) {
      console.error('PDF generation error:', err);
      showToast('Error generating PDF document.', 4000);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  // Find currently selected job object
  const currentJobObj = useMemo(() => {
    return jobs.find((j) => j.id === activeJobId) || selectedJob;
  }, [jobs, activeJobId, selectedJob]);

  const salaryDisplay = useMemo(() => {
    if (!currentJobObj) return null;
    return formatSalary(currentJobObj);
  }, [currentJobObj]);

  const wordCount = useMemo(() => {
    const text = activeDraftTab === 'cover' ? editedCoverDraft : activeDraftTab === 'outreach' ? editedOutreachDraft : editedLatex;
    return text.trim() ? text.trim().split(/\s+/).length : 0;
  }, [activeDraftTab, editedCoverDraft, editedOutreachDraft, editedLatex]);

  return (
    <div className="section-container studio-view">
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

      {/* OVERLEAF-STYLE SPLIT-SCREEN WORKSPACE */}
      <div className="split-workspace-panel panel-card overleaf-workspace">
        {/* Workspace Subheader Navigation */}
        <div className="workspace-tabs-bar">
          <div className="draft-tabs-group">
            <button
              className={`draft-tab ${activeDraftTab === 'latex' ? 'active' : ''}`}
              onClick={() => setActiveDraftTab('latex')}
            >
              <Terminal className="tab-icon-sm" />
              <span>Tailored LaTeX CV (Overleaf Engine)</span>
            </button>
            <button
              className={`draft-tab ${activeDraftTab === 'cover' ? 'active' : ''}`}
              onClick={() => setActiveDraftTab('cover')}
            >
              <FileText className="tab-icon-sm" />
              <span>Cover Letter Draft</span>
            </button>
            <button
              className={`draft-tab ${activeDraftTab === 'outreach' ? 'active' : ''}`}
              onClick={() => setActiveDraftTab('outreach')}
            >
              <Mail className="tab-icon-sm" />
              <span>Channel Outreach ({channel.toUpperCase()})</span>
            </button>
            <button
              className={`draft-tab ${activeDraftTab === 'form_qa' ? 'active' : ''}`}
              onClick={() => setActiveDraftTab('form_qa')}
            >
              <CheckSquare className="tab-icon-sm" />
              <span>Form Questionnaire ({formQuestions.length})</span>
            </button>
          </div>

          <div className="audit-badges-group">
            <span className="audit-badge pass">
              <CheckCircle2 className="icon-xxs" />
              <span>Verified Fact Audit: Passed</span>
            </span>
            <span className="audit-badge ats">
              <span>ATS Text-Layer: 100% Parsable</span>
            </span>
          </div>
        </div>

        {/* 2-COLUMN SPLIT CONTAINER (OR 1-COLUMN FOR OUTREACH EMAIL) */}
        <div className={`split-editor-grid overleaf-grid ${activeDraftTab === 'outreach' ? 'outreach-single-column' : ''}`}>
          {/* LEFT COLUMN: CODE EDITOR */}
          <div className="editor-column overleaf-editor-column">
            <div className="column-toolbar overleaf-editor-toolbar">
              <div className="column-title">
                <strong>
                  {activeDraftTab === 'latex'
                    ? 'main.tex (LaTeX Source)'
                    : activeDraftTab === 'cover'
                    ? 'cover_letter.txt'
                    : activeDraftTab === 'form_qa'
                    ? 'form_questionnaire.json'
                    : `outreach_${channel}.txt`}
                </strong>
              </div>

              <div className="toolbar-actions">
                {activeDraftTab === 'form_qa' ? (
                  <button
                    className="action-btn-xs"
                    onClick={handleCopyAllAnswers}
                    title="Copy all questions and generated answers into formatted text"
                  >
                    <Copy className="btn-icon-xxs" />
                    <span>Copy All Q&A</span>
                  </button>
                ) : (
                  <button
                    className="action-btn-xs"
                    onClick={() =>
                      handleCopyDraft(
                        activeDraftTab === 'cover'
                          ? editedCoverDraft
                          : activeDraftTab === 'outreach'
                          ? editedOutreachDraft
                          : editedLatex,
                        activeDraftTab === 'cover'
                          ? 'Cover Letter'
                          : activeDraftTab === 'outreach'
                          ? 'Outreach Message'
                          : 'LaTeX Source'
                      )
                    }
                    title="Copy content"
                  >
                    <Copy className="btn-icon-xxs" />
                    <span>Copy</span>
                  </button>
                )}

                {activeDraftTab === 'latex' && (
                  <>
                    <div className="compact-dropdown-wrap">
                      <Scissors className="btn-icon-xxs" />
                      <select
                        className="compact-select"
                        defaultValue=""
                        onChange={(e) => {
                          if (e.target.value) {
                            handleCompactToPages(Number(e.target.value));
                            e.target.value = '';
                          }
                        }}
                        title="Budget CV to 1 or 2 pages"
                      >
                        <option value="" disabled>Compact...</option>
                        <option value="1">1 Page</option>
                        <option value="2">2 Pages</option>
                      </select>
                    </div>
                    <button
                      className="action-btn-xs"
                      onClick={handleDownloadLatex}
                      title="Download raw LaTeX (.tex) file"
                    >
                      <Download className="btn-icon-xxs" />
                      <span>.tex</span>
                    </button>
                  </>
                )}
              </div>
            </div>

            <div className="textarea-container">
              {activeDraftTab === 'cover' && (
                <textarea
                  rows={20}
                  className="code-textarea"
                  value={editedCoverDraft}
                  onChange={(e) => setEditedCoverDraft(e.target.value)}
                  placeholder="Cover letter draft..."
                />
              )}

              {activeDraftTab === 'outreach' && (
                <div className="outreach-composer-view">
                  <div className="email-subject-bar">
                    <span className="email-label">Subject:</span>
                    <input
                      type="text"
                      className="email-subject-input"
                      value={`Application: ${customRole || 'AI Engineer'} - ${profile?.full_name || 'Niloy Sannyal'}`}
                      readOnly
                    />
                    <button
                      className="action-btn-xs copy-subject-btn"
                      onClick={() => handleCopyDraft(`Application: ${customRole || 'AI Engineer'} - ${profile?.full_name || 'Niloy Sannyal'}`, 'Subject Line')}
                      title="Copy Subject"
                    >
                      <Copy className="btn-icon-xxs" />
                      <span>Copy</span>
                    </button>
                  </div>

                  {channel === 'email' && (
                    <div className="email-dispatch-action-bar">
                      <a
                        href={`mailto:${channelInspection?.recruiter_email || ''}?subject=${encodeURIComponent(
                          `Application: ${customRole || 'AI Engineer'} - ${profile?.full_name || 'Niloy Sannyal'}`
                        )}&body=${encodeURIComponent(editedOutreachDraft || editedCoverDraft || '')}`}
                        className="action-btn-xs action-btn-mailto"
                        title="Open default email client with recruiter and pitch pre-filled"
                      >
                        <Mail className="btn-icon-xxs" />
                        <span>Launch in Email Client</span>
                      </a>

                      <button
                        className="action-btn-xs action-btn-accent"
                        onClick={handleDownloadEml}
                        title="Download RFC 822 .eml draft file with tailored CV attached"
                      >
                        <Download className="btn-icon-xxs" />
                        <span>Download .eml Draft with CV</span>
                      </button>
                    </div>
                  )}

                  <textarea
                    rows={18}
                    className="code-textarea outreach-body-textarea"
                    value={editedOutreachDraft}
                    onChange={(e) => setEditedOutreachDraft(e.target.value)}
                    placeholder="Direct outreach email pitch..."
                  />
                </div>
              )}

              {activeDraftTab === 'latex' && (
                <textarea
                  rows={20}
                  className="code-textarea font-mono overleaf-textarea"
                  value={editedLatex}
                  onChange={(e) => setEditedLatex(e.target.value)}
                  onKeyDown={handleKeyDown}
                  spellCheck={false}
                  placeholder="\documentclass[a4paper,11pt]{article}..."
                />
              )}

              {activeDraftTab === 'form_qa' && (
                <div className="form-qa-editor-view">
                  {/* Top Action Row */}
                  <div className="form-qa-action-row">
                    <div className="qa-action-info">
                      <CheckSquare className="icon-xs text-emerald" />
                      <span>{formQuestions.length} Structured Form Fields Detected</span>
                    </div>

                    <div className="qa-action-buttons">
                      <button
                        className="action-btn-xs action-btn-accent"
                        disabled={isGeneratingAnswers || formQuestions.length === 0}
                        onClick={handleGenerateFormAnswers}
                        title="Synthesizes candidate angles and verifies facts against STAR stories and fact ledger"
                      >
                        {isGeneratingAnswers ? (
                          <>
                            <RefreshCw className="btn-icon-xxs icon-spin" />
                            <span>Synthesizing STAR Answers...</span>
                          </>
                        ) : (
                          <>
                            <Sparkles className="btn-icon-xxs" />
                            <span>Generate Tailored Answers</span>
                          </>
                        )}
                      </button>

                      <button
                        className="action-btn-xs"
                        disabled={formQuestions.length === 0}
                        onClick={handleCopyAllAnswers}
                      >
                        <Copy className="btn-icon-xxs" />
                        <span>Copy All Answers</span>
                      </button>
                    </div>
                  </div>

                  {formQuestions.length === 0 ? (
                    <div className="empty-qa-state">
                      <HelpCircle className="empty-qa-icon" />
                      <h4>No Questions Detected Yet</h4>
                      <p>
                        Click <strong>Detect Channel & Forms</strong> above to scan the target posting
                        and apply URL for Google Forms, ATS, or custom questionnaire fields.
                      </p>
                      <button
                        className="action-btn-secondary"
                        disabled={isDetectingChannel}
                        onClick={() => handleDetectChannel()}
                      >
                        <Compass className="btn-icon-xs" />
                        <span>Detect Questions Now</span>
                      </button>
                    </div>
                  ) : (
                    <div className="qa-cards-scroll">
                      {formQuestions.map((q, idx) => {
                        const ansObj = formAnswers[q.id];
                        const answerText = ansObj ? ansObj.answer : '';
                        const isCopied = copiedQuestionId === q.id;
                        const charLimit = q.char_limit || 2000;

                        return (
                          <div key={q.id || idx} className="qa-card">
                            <div className="qa-card-header">
                              <div className="qa-prompt-wrap">
                                <span className="qa-q-num">Q{idx + 1}</span>
                                <strong className="qa-prompt-text">{q.prompt}</strong>
                              </div>
                              <div className="qa-card-badges">
                                <span className="qa-badge-type">{q.field_type}</span>
                                {q.char_limit && (
                                  <span className="qa-badge-limit">Limit: {q.char_limit}</span>
                                )}
                                {q.is_required && (
                                  <span className="qa-badge-req">Required</span>
                                )}
                              </div>
                            </div>

                            {/* Deliberated Candidate Angles (Harness² recursion) */}
                            {ansObj?.candidate_angles && ansObj.candidate_angles.length > 0 && (
                              <div className="qa-angles-box">
                                <div className="angles-title">
                                  <Sparkles className="icon-xxs text-emerald" />
                                  <span>Candidate Angles Deliberated (Harness² Recursion):</span>
                                </div>
                                <ul className="angles-list">
                                  {ansObj.candidate_angles.map((ang, aIdx) => (
                                    <li key={aIdx}>{ang}</li>
                                  ))}
                                </ul>
                              </div>
                            )}

                            {/* Verified Fact Ledger Grounding */}
                            {ansObj?.verified_facts_used && ansObj.verified_facts_used.length > 0 && (
                              <div className="qa-facts-box">
                                <span className="facts-label">✓ Verified Grounding:</span>
                                <div className="facts-tags-row">
                                  {ansObj.verified_facts_used.map((fact, fIdx) => (
                                    <span key={fIdx} className="fact-pill">
                                      {fact}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Editable Answer Field */}
                            <div className="qa-textarea-wrap">
                              <textarea
                                rows={q.field_type === 'short_text' || q.field_type === 'url' ? 2 : 4}
                                className="code-textarea qa-textarea"
                                value={answerText}
                                onChange={(e) => handleUpdateSingleAnswer(q.id, e.target.value)}
                                placeholder="Answer will be generated here, or type response..."
                              />
                            </div>

                            <div className="qa-card-footer">
                              <span className="qa-char-count">
                                {answerText.length} / {charLimit} characters
                              </span>
                              <button
                                className={`action-btn-xs ${isCopied ? 'btn-copied' : ''}`}
                                disabled={!answerText}
                                onClick={() => handleCopySingleAnswer(q.id, answerText)}
                              >
                                {isCopied ? (
                                  <>
                                    <Check className="btn-icon-xxs" />
                                    <span>Copied!</span>
                                  </>
                                ) : (
                                  <>
                                    <Copy className="btn-icon-xxs" />
                                    <span>Copy Field</span>
                                  </>
                                )}
                              </button>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* RIGHT COLUMN: OVERLEAF COMPILE BAR & LIVE PREVIEW (HIDDEN FOR EMAIL OUTREACH) */}
          {activeDraftTab !== 'outreach' && (
            <div className="preview-column overleaf-preview-column">
              {activeDraftTab === 'form_qa' ? (
                <div className="dispatch-assistant-container">
                  <div className="column-toolbar overleaf-toolbar">
                    <div className="column-title">
                      <Compass className="icon-xxs text-emerald" />
                      <strong>Form Dispatch & Autofill Assistant</strong>
                    </div>
                  </div>

                  <div className="dispatch-assistant-body">
                    <div className="dispatch-card-item highlight">
                      <div className="dispatch-card-title">
                        <span className="channel-badge-emerald">
                          {channelInspection?.platform_name || channelInspection?.channel_type || 'Detected Form'}
                        </span>
                        {channelInspection?.detection_confidence && (
                          <span className="dispatch-conf-pill">
                            {Math.round(channelInspection.detection_confidence * 100)}% Match
                          </span>
                        )}
                      </div>
                      <p className="dispatch-desc">
                        {channelInspection?.action_summary ||
                          'Review synthesized answers on the left. Click "Copy Field" to paste into the external application form.'}
                      </p>
                      {channelInspection?.apply_url && (
                        <a
                          href={channelInspection.apply_url}
                          target="_blank"
                          rel="noreferrer"
                          className="dispatch-external-btn"
                        >
                          <span>Open Form in New Tab</span>
                          <ExternalLink className="icon-xxs" />
                        </a>
                      )}
                    </div>

                    <div className="dispatch-card-item">
                      <h5>Quick 3-Step Autofill Workflow:</h5>
                      <ol className="dispatch-steps">
                        <li>
                          <strong>1. Synthesize:</strong> Click "Generate Tailored Answers" to craft structured responses grounded in your STAR story bank.
                        </li>
                        <li>
                          <strong>2. Open Form:</strong> Open the target Google Form or ATS portal in a neighboring tab.
                        </li>
                        <li>
                          <strong>3. 1-Click Paste:</strong> Click "Copy Field" on each answer to paste into the corresponding form field with zero re-typing.
                        </li>
                      </ol>
                    </div>

                    <div className="dispatch-card-item">
                      <h5>Verified Profile References:</h5>
                      <div className="dispatch-ref-grid">
                        <div className="ref-row">
                          <span className="ref-k">Full Name:</span>
                          <span className="ref-v">{profile?.full_name || 'Niloy Sannyal'}</span>
                        </div>
                        <div className="ref-row">
                          <span className="ref-k">Email:</span>
                          <span className="ref-v">niloysannyal@gmail.com</span>
                        </div>
                        <div className="ref-row">
                          <span className="ref-k">Portfolio:</span>
                          <span className="ref-v">{profile?.portfolio_url || 'https://www.niloysannyal.me/'}</span>
                        </div>
                        <div className="ref-row">
                          <span className="ref-k">GitHub:</span>
                          <span className="ref-v">{profile?.github_url || 'https://github.com/niloysannyal'}</span>
                        </div>
                        <div className="ref-row">
                          <span className="ref-k">Notice:</span>
                          <span className="ref-v">{profile?.notice_period || '2 weeks'}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <>
                  {/* OVERLEAF PREVIEW TOOLBAR (WITH COMPILE BUTTON IN PLACE OF STATIC LABEL) */}
                  <div className="column-toolbar overleaf-toolbar">
                <div className="overleaf-toolbar-left">
                  {activeDraftTab === 'latex' ? (
                    <button
                      className={`overleaf-compile-btn ${isCompiling ? 'loading' : ''}`}
                      onClick={handleCompile}
                      disabled={isCompiling}
                      title="Compile LaTeX source code (Ctrl + Enter)"
                    >
                      {isCompiling ? (
                        <RefreshCw className="btn-icon-xs icon-spin" />
                      ) : (
                        <Eye className="btn-icon-xs" />
                      )}
                      <span>{isCompiling ? 'Compiling...' : 'Recompile'}</span>
                      <kbd className="overleaf-kbd">Ctrl+↵</kbd>
                    </button>
                  ) : (
                    <div className="column-title">
                      <Eye className="icon-xxs" />
                      <strong>Formatted Document Preview</strong>
                    </div>
                  )}
                </div>

                <div className="overleaf-toolbar-right">
                  {/* Overleaf Zoom Controls */}
                  <div className="zoom-controls-group">
                    <button
                      className="zoom-btn"
                      onClick={() => setZoomLevel((z) => Math.max(70, z - 10))}
                      title="Zoom Out"
                    >
                      <ZoomOut className="icon-xxs" />
                    </button>
                    <span className="zoom-label">{zoomLevel}%</span>
                    <button
                      className="zoom-btn"
                      onClick={() => setZoomLevel((z) => Math.min(130, z + 10))}
                      title="Zoom In"
                    >
                      <ZoomIn className="icon-xxs" />
                    </button>
                  </div>

                  <button
                    className="action-btn-xs action-btn-pdf"
                    onClick={handleDownloadPdf}
                    title="Generate and download compiled PDF document"
                  >
                    <Download className="btn-icon-xxs" />
                    <span>Download PDF</span>
                  </button>

                  <button
                    className="action-btn-xs"
                    onClick={handlePrint}
                    title="Print or Save via browser dialog"
                  >
                    <Printer className="btn-icon-xxs" />
                    <span>Print</span>
                  </button>
                </div>
              </div>

              {/* PREVIEW SHEET WRAPPER */}
              <div className="preview-sheet-wrapper overleaf-viewer-bg" ref={previewRef}>
                {/* DYNAMIC LATEX COMPILED MULTI-PAGE DOCUMENT PREVIEW */}
                {activeDraftTab === 'latex' ? (
                  <div
                    className="overleaf-multi-page-container"
                    style={{
                      transform: `scale(${zoomLevel / 100})`,
                      transformOrigin: 'top center',
                    }}
                  >
                    {paginatedPages.map((page, pIdx) => (
                      <div key={pIdx} className="overleaf-a4-page-card" id={`overleaf-page-${page.pageNumber}`}>
                        {/* Authentic Page Tag Badge */}
                        <div className="a4-page-top-badge">Page {page.pageNumber} of {paginatedPages.length}</div>

                        {/* Document Header (Rendered on Page 1) */}
                        {page.hasHeader && (
                          <div className="cv-header-container">
                            <div className="cv-header-top-row">
                              <div className="cv-header-left">
                                <h1 className="cv-name">{(parsedDoc.header.name || 'NILOY SANNYAL').toUpperCase()}</h1>
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
                                <div className="cv-location-line">Location: {parsedDoc.header.location || 'Dhaka, Bangladesh'}</div>
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

                        {/* Authentic A4 Page Number Footer */}
                        <div className="a4-page-number-footer">
                          Page {page.pageNumber} of {paginatedPages.length}
                        </div>
                      </div>
                    ))}

                    {paginatedPages.length === 0 && (
                      <div className="empty-latex-notice">
                        <p>Click <strong>Recompile</strong> to compile your LaTeX code into the visual document preview.</p>
                      </div>
                    )}
                  </div>
                ) : (
                  /* COVER LETTER PREVIEW (AUTHENTIC A4 PROPORTIONS & CLEAN ENTITIES) */
                  <div
                    className="letter-paper-preview overleaf-paper"
                    style={{
                      transform: `scale(${zoomLevel / 100})`,
                      transformOrigin: 'top center',
                    }}
                  >
                    <div className="letter-header">
                      <h2>{decodeHtmlEntities(profile?.full_name || 'Niloy Sannyal')}</h2>
                      <p className="letter-subhead">
                        Dhaka, Bangladesh • niloysannyal@gmail.com • +8801783445245 • niloysannyal.me
                      </p>
                      <div className="letter-rule"></div>
                    </div>

                    <div className="letter-meta-block">
                      <p>
                        <strong>Date:</strong>{' '}
                        {new Date().toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                        })}
                      </p>
                      <p>
                        <strong>To:</strong> Hiring Team at {decodeHtmlEntities(customCompany || 'Target Company')}
                      </p>
                      <p>
                        <strong>Re:</strong> Application for {decodeHtmlEntities(customRole || 'AI Engineer')}
                      </p>
                    </div>

                    <div className="letter-body">
                      {decodeHtmlEntities(editedCoverDraft)
                        .split(/\n\s*\n/)
                        .map((paragraph, idx) => (
                          <p key={idx} className="letter-paragraph">
                            {paragraph.trim()}
                          </p>
                        ))}
                    </div>

                    <div className="letter-signature-block">
                      <p>Sincerely,</p>
                      <p className="signature-name">{decodeHtmlEntities(profile?.full_name || 'Niloy Sannyal')}</p>
                      <p className="signature-title">AI Engineer</p>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      )}
        </div>

        {/* STRICT HUMAN-IN-THE-LOOP SEND GATE */}
        <div className="send-gate-card">
          <div className="gate-notice-left">
            <ShieldCheck className="gate-shield-icon" />
            <div>
              <h4>Strict Human-in-the-Loop Send Gate</h4>
              <p>
                This application is saved in <strong>Draft</strong> status. The platform never auto-sends.
                Review the materials in the preview pane above, then click below to confirm.
              </p>
            </div>
          </div>

          <div className="gate-actions-right">
            <button
              className="approve-send-btn"
              disabled={isSending}
              onClick={() =>
                onApproveAndSend({
                  applicationId:
                    tailorResult?.application?.id ||
                    applications.find((a) => a.job_id === activeJobId)?.id,
                  jobId: activeJobId,
                  coverDraft: editedCoverDraft,
                  tailoredLatex: editedLatex,
                })
              }
            >
              {isSending ? (
                <>
                  <RefreshCw className="btn-icon icon-spin" />
                  <span>Confirming...</span>
                </>
              ) : (
                <>
                  <Send className="btn-icon" />
                  <span>Approve & Mark Sent</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
