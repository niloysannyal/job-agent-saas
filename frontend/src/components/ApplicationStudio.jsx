import React, { useState, useEffect, useMemo, useRef } from 'react';
import { formatSalary } from './JobsView';
import {
  parseLatexDocument,
  paginateParsedDocument,
  compactLatex,
  decodeHtmlEntities,
} from '../utils/latexCompiler';
import StudioJobContext from './studio/StudioJobContext';
import StudioDrafterWorkspace from './studio/StudioDrafterWorkspace';
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
  const [bookmarkletJs, setBookmarkletJs] = useState('');

  // Google OAuth & Gmail State
  const [googleConnected, setGoogleConnected] = useState(false);
  const [googleEmail, setGoogleEmail] = useState('');
  const [isDraftingGmail, setIsDraftingGmail] = useState(false);
  const [gmailDraftLink, setGmailDraftLink] = useState('');

  // Overleaf-style Compiler State
  const [isCompiling, setIsCompiling] = useState(false);
  const [compileStatus, setCompileStatus] = useState('success'); // idle | compiling | success | error
  const [compileTime, setCompileTime] = useState('0.3s');
  const [zoomLevel, setZoomLevel] = useState(75); // Responsive fit default for split view
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
      if (existingApp) {
        if (existingApp.channel) {
          setChannel(existingApp.channel);
        }
        if (existingApp.draft_content) {
          setEditedCoverDraft(decodeHtmlEntities(existingApp.draft_content));
        }
        const { initialOutreach } = generateInitialDrafts(comp, jobTitle);
        setEditedOutreachDraft(initialOutreach);

        // Load tailored LaTeX from existing application if present
        if (existingApp.cv_version?.tailored_latex) {
          const cleanCode = cleanInitialLatex(existingApp.cv_version.tailored_latex);
          setEditedLatex(cleanCode);
          const parsed = parseLatexDocument(cleanCode);
          setParsedDoc(parsed);
          setCompileStatus('success');
        } else if (profile?.master_cv_latex) {
          const cleanCode = cleanInitialLatex(profile.master_cv_latex);
          setEditedLatex(cleanCode);
          const parsed = parseLatexDocument(cleanCode);
          setParsedDoc(parsed);
        }

        // Restore existing form answers if present
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
          const parsed = parseLatexDocument(cleanCode);
          setParsedDoc(parsed);
        }
      }

      runFitAnalysis(selectedJob.id, selectedJob.description, comp, jobTitle);
      handleDetectChannel(selectedJob);
      fetchBookmarklet(selectedJob.id);
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

  // Check Google OAuth integration status
  useEffect(() => {
    const checkGoogleStatus = async () => {
      try {
        const res = await fetch('/api/v1/integrations/google/status', {
          headers: { ...(authHeaders || {}), 'X-Account-ID': profile?.account_id || '' },
        });
        if (res.ok) {
          const data = await res.json();
          setGoogleConnected(data.connected);
          setGoogleEmail(data.email || '');
        }
      } catch (e) {
        // quiet fallback
      }
    };
    checkGoogleStatus();
  }, [profile?.account_id]);

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
    }, 220);
  };

  // Compact / Budget to target pages action
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
        headers: {
          'Content-Type': 'application/json',
          ...(authHeaders || {}),
          'X-Account-ID': profile?.account_id || '',
        },
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

        if (data.recommended_channel) {
          setChannel(data.recommended_channel);
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
        showToast(`✨ Channel detected: ${data.platform_name || data.channel_type.toUpperCase()} (${data.action_summary})`);
      }
    } catch (err) {
      console.error('Channel detection error:', err);
    } finally {
      setIsDetectingChannel(false);
    }
  };

  const handleGenerateFormAnswers = async () => {
    if (!channelInspection?.id && !formQuestions.length) return;
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
        showToast(`✨ Generated ${data.answers.length} verified responses for the application form!`);
      } else {
        showToast('Error synthesizing form answers.');
      }
    } catch (err) {
      console.error('Generate answers error:', err);
      showToast('Failed to generate form answers.');
    } finally {
      setIsGeneratingAnswers(false);
    }
  };

  const handleCopyQuestionAnswer = async (qId, text, prompt) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedQuestionId(qId);
      setTimeout(() => setCopiedQuestionId(null), 2000);
      showToast(`Copied answer for: "${prompt.slice(0, 30)}..."`);
    } catch (e) {
      showToast('Failed to copy text');
    }
  };

  const handleCopyAllAnswers = async () => {
    try {
      const formatted = formQuestions
        .map((q, idx) => {
          const ans = formAnswers[q.id]?.answer || '(No answer generated)';
          return `Question ${idx + 1}: ${q.prompt}\nAnswer:\n${ans}\n`;
        })
        .join('\n---\n\n');

      await navigator.clipboard.writeText(formatted);
      showToast('Copied all form questions and answers!');
    } catch (e) {
      showToast('Failed to copy questions and answers');
    }
  };

  const handleFormAnswerChange = (questionId, newText) => {
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

  const handleConnectGmail = async () => {
    try {
      const res = await fetch('/api/v1/integrations/google/auth-url', {
        headers: { 'X-Account-ID': profile?.account_id || '' },
      });
      if (res.ok) {
        const data = await res.json();
        window.open(data.auth_url, '_blank', 'width=550,height=650');
        showToast('Google OAuth opened. Complete sign-in to enable 1-click drafting.');
      }
    } catch (e) {
      showToast('Error opening Google authentication');
    }
  };

  const handleDraftInGmail = async () => {
    setIsDraftingGmail(true);
    setGmailDraftLink('');
    try {
      showToast('Creating Draft in your Gmail...');
      const comp = customCompany || 'Company';
      const role = customRole || 'AI Engineer';
      const candidateName = profile?.full_name || 'Niloy Sannyal';
      const toEmail = channelInspection?.recruiter_email || 'recruiter@company.com';
      const subject = `Application: ${role} - ${candidateName}`;
      const body = editedOutreachDraft || editedCoverDraft;

      const res = await fetch('/api/v1/integrations/google/create-draft', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Account-ID': profile?.account_id || '',
        },
        body: JSON.stringify({
          application_id: applications.find((a) => a.job_id === activeJobId)?.id,
          recipient_email: toEmail,
          subject,
          body_text: body,
          attach_cv: true,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setGmailDraftLink(data.web_link);
        showToast('✨ Draft created in Gmail! 1-Click ready for your review.');
      } else {
        const err = await res.json();
        if (err.detail && err.detail.includes('not connected')) {
          handleConnectGmail();
        } else {
          showToast(err.detail || 'Failed to create Gmail draft');
        }
      }
    } catch (e) {
      showToast('Failed to connect to Gmail service');
    } finally {
      setIsDraftingGmail(false);
    }
  };

  const handleCopyBookmarklet = async () => {
    try {
      const qParams = activeJobId ? `?job_id=${encodeURIComponent(activeJobId)}` : '';
      const res = await fetch(`/api/v1/integrations/autofill/bookmarklet${qParams}`, {
        headers: { ...(authHeaders || {}), 'X-Account-ID': profile?.account_id || '' },
      });
      if (res.ok) {
        const data = await res.json();
        setBookmarkletJs(data.bookmarklet_js);
        await navigator.clipboard.writeText(data.bookmarklet_js);
        showToast('📋 Job-specific Autofill Bookmarklet copied! Click it on any job application or ATS page.');
      }
    } catch (e) {
      showToast('Failed to copy bookmarklet');
    }
  };

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
    } catch (e) {
      // quiet fallback
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

  const handleDownloadLatex = () => {
    downloadLatexSource(editedLatex, profile, customCompany, showToast);
  };

  const handleDownloadPdf = () => {
    downloadPdfDocument({
      activeDraftTab,
      parsedDoc,
      customCompany,
      customRole,
      profile,
      editedCoverDraft,
      editedOutreachDraft,
      showToast,
    });
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

  return (
    <div className="section-container studio-view">
      {/* Target Opportunity Selector & Diagnostics */}
      <StudioJobContext
        channel={channel}
        setChannel={setChannel}
        activeJobId={activeJobId}
        handleJobSelectChange={handleJobSelectChange}
        jobs={jobs}
        customCompany={customCompany}
        setCustomCompany={setCustomCompany}
        customRole={customRole}
        setCustomRole={setCustomRole}
        currentJobObj={currentJobObj}
        salaryDisplay={salaryDisplay}
        customPostingText={customPostingText}
        setCustomPostingText={setCustomPostingText}
        isEvaluatingFit={isEvaluatingFit}
        handleManualAnalyze={handleManualAnalyze}
        isDetectingChannel={isDetectingChannel}
        handleDetectChannel={handleDetectChannel}
        isTailoring={isTailoring}
        handleExecuteTailor={handleExecuteTailor}
        channelInspection={channelInspection}
        formQuestions={formQuestions}
        profile={profile}
        editedOutreachDraft={editedOutreachDraft}
        editedCoverDraft={editedCoverDraft}
        setActiveDraftTab={setActiveDraftTab}
        fitResult={fitResult}
      />

      {/* OVERLEAF-STYLE SPLIT-SCREEN WORKSPACE */}
      <StudioDrafterWorkspace
        activeDraftTab={activeDraftTab}
        setActiveDraftTab={setActiveDraftTab}
        channel={channel}
        formQuestions={formQuestions}
        formAnswers={formAnswers}
        bookmarkletJs={bookmarkletJs}
        handleCopyBookmarklet={handleCopyBookmarklet}
        handleCopyAllAnswers={handleCopyAllAnswers}
        handleCopyDraft={handleCopyDraft}
        handleDownloadLatex={handleDownloadLatex}
        handleCompactToPages={handleCompactToPages}
        editedCoverDraft={editedCoverDraft}
        setEditedCoverDraft={setEditedCoverDraft}
        editedOutreachDraft={editedOutreachDraft}
        setEditedOutreachDraft={setEditedOutreachDraft}
        editedLatex={editedLatex}
        setEditedLatex={setEditedLatex}
        handleKeyDown={handleKeyDown}
        customCompany={customCompany}
        customRole={customRole}
        profile={profile}
        channelInspection={channelInspection}
        handleDownloadEml={handleDownloadEml}
        googleConnected={googleConnected}
        isDraftingGmail={isDraftingGmail}
        handleDraftInGmail={handleDraftInGmail}
        handleConnectGmail={handleConnectGmail}
        gmailDraftLink={gmailDraftLink}
        isGeneratingAnswers={isGeneratingAnswers}
        handleGenerateFormAnswers={handleGenerateFormAnswers}
        handleDetectChannel={handleDetectChannel}
        isDetectingChannel={isDetectingChannel}
        copiedQuestionId={copiedQuestionId}
        handleCopyQuestionAnswer={handleCopyQuestionAnswer}
        handleFormAnswerChange={handleFormAnswerChange}
        handleCompile={handleCompile}
        isCompiling={isCompiling}
        zoomLevel={zoomLevel}
        setZoomLevel={setZoomLevel}
        handleDownloadPdf={handleDownloadPdf}
        handlePrint={handlePrint}
        previewRef={previewRef}
        paginatedPages={paginatedPages}
        parsedDoc={parsedDoc}
        onNavigate={onNavigate}
      />

      {/* STRICT HUMAN-IN-THE-LOOP SEND GATE */}
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
  );
}
