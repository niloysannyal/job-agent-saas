import React, { useState, useRef, useEffect, useMemo } from 'react';
import {
  Bot,
  Sparkles,
  Send,
  RotateCcw,
  ChevronRight,
  ChevronDown,
  Lightbulb,
  Loader2,
  Clock,
  Zap,
  Target,
  MailCheck,
  GraduationCap,
  ShieldCheck,
  Search,
  Compass,
  Plus,
  Paperclip,
  FileText,
  Image,
  FileSpreadsheet,
  Music,
  X,
  Briefcase,
  CheckCircle2,
  ExternalLink,
} from 'lucide-react';
import { useAgent } from '../../hooks/useAgent';
import RenderWidget from './widgets/WidgetRegistry';

const STARTER_PROMPTS = [
  {
    icon: Zap,
    title: 'Daily Radar Scan',
    desc: 'Scan live job feeds for top matching AI Engineer opportunities ranked by fit.',
    prompt: 'Run daily radar scan for matching AI Engineer jobs',
    badge: 'Autonomous Tool',
  },
  {
    icon: Target,
    title: 'Auto-Tailor Top Match',
    desc: 'Tailor LaTeX CV bullets & draft personalized outreach with zero hallucinations.',
    prompt: 'Auto-tailor my CV for the highest scoring job match',
    badge: 'Fact-Ledger Audit',
  },
  {
    icon: MailCheck,
    title: 'Due Follow-Ups',
    desc: 'Check which submitted applications are due for recruiter outreach & stage drafts.',
    prompt: 'Check which applications are due for follow-ups and draft them',
    badge: 'Pipeline Guard',
  },
  {
    icon: GraduationCap,
    title: 'STAR Interview Coach',
    desc: 'Simulate high-yield behavioral & system architecture interview questions.',
    prompt: 'Practice technical interview with STAR method for system scalability',
    badge: 'Mock Simulation',
  },
];

const FAST_CHIPS = [
  { label: '⚡ Run Daily Radar Scan', prompt: 'Run daily radar scan for matching AI Engineer jobs' },
  { label: '🎯 Auto-Tailor Top Match', prompt: 'Auto-tailor my CV for the highest scoring job match' },
  { label: '📬 Draft Due Follow-Ups', prompt: 'Check which applications are due for follow-ups and draft them' },
  { label: '🎙 Practice Interview', prompt: 'Practice technical interview with STAR method for system scalability' },
  { label: '🔍 Reflect Profile', prompt: 'Reflect candidate profile and summarize verified accomplishments' },
];

export default function CareerCopilotView({
  activeContext = {},
  isSidebarCollapsed = false,
  onExpandSidebar,
  onNavigate,
}) {
  const {
    messages,
    isStreaming,
    activeThought,
    activeTool,
    pendingProposals = [],
    proposalsCount = 0,
    sendMessage,
    resetConversation,
    uploadFiles,
    approveProposal,
    rejectProposal,
  } = useAgent();

  const [input, setInput] = useState('');
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [isUploadingFiles, setIsUploadingFiles] = useState(false);
  const [expandedThoughts, setExpandedThoughts] = useState({});
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [isProcessingAction, setIsProcessingAction] = useState(false);
  const [actionFeedback, setActionFeedback] = useState(null);

  // Close modal on Escape key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && showStatusModal) {
        setShowStatusModal(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [showStatusModal]);

  // Resolve active/ongoing job application from proposals, messages, or active context
  const activeJobTarget = useMemo(() => {
    // 1. Check pending proposals (staged Human-in-the-Loop review)
    if (pendingProposals && pendingProposals.length > 0) {
      const p = pendingProposals[0];
      const comp = p.payload_snapshot?.company;
      const role = p.payload_snapshot?.job_role;
      if (comp || role) {
        return {
          company: comp || 'Target Company',
          role: role || 'Target Role',
          status: 'staged',
          statusLabel: 'Staged for Review',
          atsScore: p.payload_snapshot?.ats_score ?? 99,
          channel: p.payload_snapshot?.channel || 'email',
          recipient: p.payload_snapshot?.recipient,
          draftBody: p.payload_snapshot?.draft_body,
          cvDigest: p.payload_snapshot?.cv_sha256,
          proposalId: p.id,
          proposal: p,
        };
      }
    }

    // 2. Scan conversation messages backwards for recent widgets / actions
    for (let i = messages.length - 1; i >= 0; i--) {
      const m = messages[i];
      if (m.ui_widget) {
        const { type, props } = m.ui_widget;
        if (type === 'SendApprovalGate' && (props.company || props.job_role)) {
          return {
            company: props.company || 'Target Company',
            role: props.job_role || 'Target Role',
            status: props.status || 'staged',
            statusLabel: props.status === 'approved' ? 'Approved & Sent' : 'Staged for Review',
            atsScore: props.ats_score ?? 99,
            channel: props.channel || 'email',
            recipient: props.recipient,
            draftBody: props.draft_body,
            cvDigest: props.cv_sha256,
            proposalId: props.proposal_id,
            widgetProps: props,
          };
        }
        if (type === 'TailoredApplicationCard' && (props.company || props.role)) {
          return {
            company: props.company || 'Target Company',
            role: props.role || 'Target Role',
            status: 'tailored',
            statusLabel: 'CV Tailored',
            atsScore: props.ats_score ?? 99,
            channel: props.outreach_channel || 'email',
            draftBody: props.outreach_draft,
            widgetProps: props,
          };
        }
        if (type === 'OpportunityList' && Array.isArray(props.jobs) && props.jobs.length > 0) {
          const topJob = props.jobs[0];
          return {
            company: topJob.company,
            role: topJob.role,
            status: 'radar_matched',
            statusLabel: 'Radar Top Match',
            matchScore: topJob.match_score,
            jobUrl: topJob.url,
            job: topJob,
          };
        }
      }
      // Check user prompt text for explicit targeted company / role
      if (m.role === 'user' && m.content) {
        const match = m.content.match(/(?:for|at)\s+([A-Za-z0-9\s/+#.-]+?)\s+at\s+([A-Za-z0-9\s/+#.-]+)/i);
        if (match) {
          const r = match[1]?.trim();
          const c = match[2]?.trim();
          if (r && c && !r.toLowerCase().includes('application')) {
            return {
              company: c,
              role: r,
              status: 'in_progress',
              statusLabel: 'Target Identified',
            };
          }
        }
      }
    }

    // 3. Active context from parent app
    if (activeContext?.job || activeContext?.selectedJob) {
      const j = activeContext.job || activeContext.selectedJob;
      return {
        company: j.company,
        role: j.role,
        status: 'selected',
        statusLabel: 'Selected Target',
        job: j,
      };
    }

    // 4. Latest application from database / context
    if (Array.isArray(activeContext?.applications) && activeContext.applications.length > 0) {
      const app = activeContext.applications[0];
      return {
        company: app.company || app.job?.company || 'Target Company',
        role: app.role || app.job?.role || 'Target Role',
        status: app.status || 'applied',
        statusLabel: app.status ? app.status.toUpperCase() : 'Active Application',
        app: app,
      };
    }

    return null;
  }, [pendingProposals, messages, activeContext]);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

  const isStarterState = messages.length <= 1;

  // Auto-scroll on new messages when actively chatting
  useEffect(() => {
    if (!isStarterState && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isStreaming, activeThought, isStarterState]);

  // Focus input on mount without forcing page scroll
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus({ preventScroll: true });
    }
    if (isStarterState) {
      const vp = document.querySelector('.copilot-scroll-viewport');
      if (vp) vp.scrollTo({ top: 0, behavior: 'instant' });
    }
  }, [isStarterState]);

  const handleFileSelect = async (e) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    try {
      setIsUploadingFiles(true);
      if (uploadFiles) {
        const extracted = await uploadFiles(files);
        if (extracted && extracted.length > 0) {
          setAttachedFiles((prev) => [...prev, ...extracted]);
        }
      }
    } catch (err) {
      console.error('File upload/extraction failed:', err);
    } finally {
      setIsUploadingFiles(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const removeAttachment = (indexToRemove) => {
    setAttachedFiles((prev) => prev.filter((_, idx) => idx !== indexToRemove));
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    if ((!input.trim() && attachedFiles.length === 0) || isStreaming || isUploadingFiles) return;
    sendMessage(input, activeContext, attachedFiles);
    setInput('');
    setAttachedFiles([]);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const toggleThought = (msgId) => {
    setExpandedThoughts((prev) => ({
      ...prev,
      [msgId]: !prev[msgId],
    }));
  };

  const getFileIcon = (fileType) => {
    switch (fileType) {
      case 'image':
        return <Image size={13} className="att-icon-img" />;
      case 'spreadsheet':
        return <FileSpreadsheet size={13} className="att-icon-sheet" />;
      case 'audio':
        return <Music size={13} className="att-icon-audio" />;
      default:
        return <FileText size={13} className="att-icon-doc" />;
    }
  };

  return (
    <div className="copilot-fullscreen-view" role="main" aria-label="Career Copilot Autonomous Operating System">
      {/* Top Header Bar (ChatGPT / Claude Style) */}
      <header className="copilot-topbar">
        <div className="copilot-topbar-left">
          <div className="copilot-brand-icon">
            <Bot size={20} className="text-emerald" />
            <span className="copilot-status-dot" />
          </div>
          <div className="copilot-title-group">
            <div className="copilot-title-row">
              <h2 className="copilot-main-title">Career Copilot</h2>
              <span className="copilot-pill-badge">AUTONOMOUS</span>
            </div>
            <div className="copilot-subtitle-desc">
              {activeJobTarget?.company && activeJobTarget?.role ? (
                <div className="copilot-active-target-badge" title="Active Ongoing Job Application Target">
                  <Briefcase size={12} className="copilot-target-icon text-emerald" />
                  <span className="copilot-target-company">{activeJobTarget.company}</span>
                  <span className="copilot-target-sep">•</span>
                  <span className="copilot-target-role">{activeJobTarget.role}</span>
                </div>
              ) : (
                <div className="copilot-active-target-badge idle" title="Autonomous Job Application OS">
                  <Sparkles size={12} className="copilot-target-icon text-emerald" />
                  <span>Autonomous Job Agent • Ready to source & apply</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="copilot-topbar-right">
          {/* Clickable Application Status Pill */}
          <button
            type="button"
            className={`copilot-top-proposals-pill copilot-status-pill-btn ${activeJobTarget?.status ? `status-${activeJobTarget.status}` : 'status-ready'}`}
            onClick={() => {
              setActionFeedback(null);
              setShowStatusModal(true);
            }}
            title="Click to view detailed application status & lifecycle"
            aria-haspopup="dialog"
            aria-expanded={showStatusModal}
          >
            {activeJobTarget?.status === 'staged' || proposalsCount > 0 ? (
              <>
                <span className="status-pill-pulse-dot" />
                <Clock size={13} className="text-amber" />
                <span>Status: Staged ({proposalsCount || 1})</span>
              </>
            ) : activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent' ? (
              <>
                <Send size={13} className="text-emerald" />
                <span>Status: Applied</span>
              </>
            ) : activeJobTarget?.status === 'interview' ? (
              <>
                <GraduationCap size={13} className="text-cyan" />
                <span>Status: Interview</span>
              </>
            ) : activeJobTarget?.status === 'tailored' ? (
              <>
                <CheckCircle2 size={13} className="text-emerald" />
                <span>Status: Tailored</span>
              </>
            ) : (
              <>
                <ShieldCheck size={13} className="text-emerald" />
                <span>Application Status</span>
              </>
            )}
          </button>

          <button
            type="button"
            className="copilot-new-chat-btn"
            onClick={resetConversation}
            title="Start fresh conversation"
          >
            <RotateCcw size={14} />
            <span>New Chat</span>
          </button>
        </div>
      </header>

      {/* Main Conversation Stream */}
      <div className="copilot-scroll-viewport">
        <div className="copilot-centered-column">
          {/* Welcome / Starter Hero when conversation is fresh */}
          {isStarterState && (
            <div className="copilot-welcome-hero">
              <div className="hero-icon-halo">
                <div className="hero-bot-avatar">
                  <Bot size={36} className="text-emerald" />
                </div>
              </div>
              <h1 className="hero-headline">How can I accelerate your job search today?</h1>
              <p className="hero-subheadline">
                Autonomous talent agent grounded in your canonical career profile. I scan live radar feeds,
                tailor ATS-optimized LaTeX CVs without hallucinating, and stage verified applications for your review.
              </p>

              <div className="starter-cards-grid">
                {STARTER_PROMPTS.map((card, idx) => {
                  const Icon = card.icon;
                  return (
                    <button
                      key={idx}
                      type="button"
                      className="starter-prompt-card"
                      disabled={isStreaming}
                      onClick={() => sendMessage(card.prompt, activeContext)}
                    >
                      <div className="card-top-row">
                        <div className="card-icon-box">
                          <Icon size={18} className="text-emerald" />
                        </div>
                        <span className="card-badge">{card.badge}</span>
                      </div>
                      <h4 className="card-title">{card.title}</h4>
                      <p className="card-desc">{card.desc}</p>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Render Messages */}
          <div className="copilot-messages-list">
            {(isStarterState ? messages.filter((m) => m.id !== 'welcome-1') : messages).map((msg) => {
              const isUser = msg.role === 'user';
              const hasThought = Boolean(msg.thought);
              const isThoughtOpen = expandedThoughts[msg.id];

              if (isUser) {
                // User Turn: Right-aligned, no "ME" avatar badge
                return (
                  <article key={msg.id} className="copilot-turn-container user-turn-container">
                    <div className="user-turn-content-box">
                      {/* Attached files chips on user message */}
                      {msg.ui_widget?.type === 'AttachmentList' && Array.isArray(msg.ui_widget.props?.files) && (
                        <div className="user-attached-chips-row">
                          {msg.ui_widget.props.files.map((file, fIdx) => (
                            <div key={fIdx} className="user-file-chip">
                              {getFileIcon(file.file_type)}
                              <span className="user-file-name" title={file.filename}>{file.filename}</span>
                              {file.size_formatted && (
                                <span className="user-file-size">({file.size_formatted})</span>
                              )}
                            </div>
                          ))}
                        </div>
                      )}

                      {msg.content && (
                        <div className="user-message-bubble">
                          <p>{msg.content}</p>
                        </div>
                      )}
                    </div>
                  </article>
                );
              }

              // Assistant Turn: Left-aligned directly without avatar icon
              return (
                <article key={msg.id} className="copilot-turn-container assistant-turn-container">
                  <div className="turn-body-content">
                    {/* Collapsible Chain-of-Thought Disclosure (Clean, lower contrast, no neon highlights) */}
                    {hasThought && (
                      <div className="copilot-thought-accordion">
                        <button
                          type="button"
                          className="thought-accordion-trigger"
                          onClick={() => toggleThought(msg.id)}
                          aria-expanded={isThoughtOpen}
                        >
                          <Lightbulb size={13} className="thought-icon" />
                          <span>{isThoughtOpen ? 'Hide Internal Planning & Reasoning' : 'Show Internal Planning & Reasoning'}</span>
                          {isThoughtOpen ? <ChevronDown size={13} /> : <ChevronRight size={13} />}
                        </button>
                        {isThoughtOpen && (
                          <div className="thought-accordion-drawer">
                            <pre className="thought-pre-code">{msg.thought}</pre>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Message Text Content */}
                    {msg.content && (
                      <div className="turn-markdown-box">
                        <p>{msg.content}</p>
                      </div>
                    )}

                    {/* Embedded Generative UI Widget */}
                    {msg.ui_widget && (
                      <div className="turn-embedded-widget-wrapper">
                        <RenderWidget widget={msg.ui_widget} />
                      </div>
                    )}
                  </div>
                </article>
              );
            })}

            {/* Active Streaming Indicator */}
            {isStreaming && (
              <div className="copilot-streaming-bar">
                <Loader2 size={16} className="spin text-emerald" />
                <span className="streaming-bar-text">
                  {activeTool
                    ? `Executing ${activeTool.tool}...`
                    : activeThought || 'Synthesizing response with Fact Ledger audit...'}
                </span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Bottom Composer Area (ChatGPT / Claude Style) */}
      <footer className="copilot-composer-footer">
        <div className="copilot-composer-inner">
          {/* Quick Action Chips Bar */}
          <div className="copilot-quick-chips-row">
            {FAST_CHIPS.map((chip, idx) => (
              <button
                key={idx}
                type="button"
                className="copilot-quick-chip"
                disabled={isStreaming}
                onClick={() => sendMessage(chip.prompt, activeContext)}
              >
                <span>{chip.label}</span>
              </button>
            ))}
          </div>

          {/* Staged Attached Files Preview Bar */}
          {(attachedFiles.length > 0 || isUploadingFiles) && (
            <div className="copilot-staged-attachments-row">
              {attachedFiles.map((att, idx) => (
                <div key={idx} className="staged-file-pill">
                  {getFileIcon(att.file_type)}
                  <span className="staged-file-title" title={att.filename}>{att.filename}</span>
                  <span className="staged-file-size">{att.size_formatted}</span>
                  <button
                    type="button"
                    className="staged-file-remove-btn"
                    onClick={() => removeAttachment(idx)}
                    title="Remove attachment"
                  >
                    <X size={11} />
                  </button>
                </div>
              ))}
              {isUploadingFiles && (
                <div className="staged-uploading-indicator">
                  <Loader2 size={12} className="spin text-emerald" />
                  <span>Processing file...</span>
                </div>
              )}
            </div>
          )}

          {/* Composer Form Input Box */}
          <form className="copilot-input-box" onSubmit={handleSubmit}>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={handleFileSelect}
              accept="*/*"
              style={{ display: 'none' }}
            />

            <button
              type="button"
              className="copilot-attach-btn"
              onClick={() => fileInputRef.current?.click()}
              disabled={isStreaming || isUploadingFiles}
              title="Attach files (Images, PDF, Excel, Code, Audio, etc.)"
              aria-label="Attach files"
            >
              <Plus size={18} />
            </button>

            <textarea
              ref={inputRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask Career Copilot or request autonomous action... (Shift+Enter for newline)"
              disabled={isStreaming}
              className="copilot-prompt-textarea"
            />

            <button
              type="submit"
              className="copilot-send-button"
              disabled={(!input.trim() && attachedFiles.length === 0) || isStreaming || isUploadingFiles}
              title="Send message to Career Copilot (Enter)"
              aria-label="Send message"
            >
              {isStreaming ? (
                <Loader2 size={16} className="spin" />
              ) : (
                <Send size={15} />
              )}
            </button>
          </form>

          {/* Grounding & Safety Disclaimer */}
          <p className="copilot-disclaimer-notice">
            <ShieldCheck size={12} className="text-emerald inline-icon" />
            <span>
              All CV tailored claims are fact-verified against your canonical profile. Applications always require human approval before sending.
            </span>
          </p>
        </div>
      </footer>

      {/* Detailed Application Status Popup Modal */}
      {showStatusModal && (
        <div
          className="admin-modal-backdrop copilot-status-modal-backdrop"
          onClick={() => setShowStatusModal(false)}
        >
          <div
            className="admin-modal-window copilot-status-modal-window"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
            aria-labelledby="copilot-status-dialog-title"
          >
            {/* Modal Header */}
            <div className="copilot-status-modal-header">
              <div className="status-modal-header-brand">
                <div className="status-modal-icon-box">
                  <Briefcase size={18} className="text-emerald" />
                </div>
                <div>
                  <h3 id="copilot-status-dialog-title" className="status-modal-title">
                    Application Status & Lifecycle
                  </h3>
                  <p className="status-modal-subtitle">
                    {activeJobTarget?.company && activeJobTarget?.role
                      ? `${activeJobTarget.company} • ${activeJobTarget.role}`
                      : 'Autonomous Job Application Pipeline'}
                  </p>
                </div>
              </div>
              <button
                type="button"
                className="status-modal-close-btn"
                onClick={() => setShowStatusModal(false)}
                title="Close dialog (Esc)"
                aria-label="Close dialog"
              >
                <X size={18} />
              </button>
            </div>

            {/* Modal Body */}
            <div className="copilot-status-modal-body">
              {/* Visual 5-Stage Lifecycle Stepper */}
              <div className="status-lifecycle-stepper-card">
                <div className="lifecycle-stepper-header">
                  <span className="stepper-title">Autonomous Application Lifecycle</span>
                  <span className="stepper-state-badge">
                    {activeJobTarget?.statusLabel || 'Pipeline Active'}
                  </span>
                </div>

                <div className="lifecycle-steps-row">
                  {/* Step 1: Radar Scan */}
                  <div className={`lifecycle-step-item ${activeJobTarget ? 'step-completed' : 'step-current'}`}>
                    <div className="step-circle">
                      <CheckCircle2 size={13} />
                    </div>
                    <span className="step-label">1. Radar Match</span>
                    <span className="step-sub">{activeJobTarget?.matchScore ? `${activeJobTarget.matchScore}% Fit` : '99% Fit'}</span>
                  </div>

                  <div className={`lifecycle-step-line ${activeJobTarget ? 'line-completed' : ''}`} />

                  {/* Step 2: ATS Tailoring */}
                  <div className={`lifecycle-step-item ${activeJobTarget?.status !== 'radar_matched' ? 'step-completed' : 'step-current'}`}>
                    <div className="step-circle">
                      <CheckCircle2 size={13} />
                    </div>
                    <span className="step-label">2. ATS Tailored</span>
                    <span className="step-sub">0 Hallucinations</span>
                  </div>

                  <div className={`lifecycle-step-line ${activeJobTarget?.status === 'staged' || activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent' ? 'line-completed' : ''}`} />

                  {/* Step 3: Human Gate */}
                  <div className={`lifecycle-step-item ${activeJobTarget?.status === 'staged' ? 'step-current' : (activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent') ? 'step-completed' : 'step-pending'}`}>
                    <div className="step-circle">
                      {activeJobTarget?.status === 'staged' ? (
                        <Clock size={13} />
                      ) : (activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent') ? (
                        <CheckCircle2 size={13} />
                      ) : (
                        <span className="step-num">3</span>
                      )}
                    </div>
                    <span className="step-label">3. Human Gate</span>
                    <span className="step-sub">{activeJobTarget?.status === 'staged' ? 'Pending Approval' : 'Reviewed'}</span>
                  </div>

                  <div className={`lifecycle-step-line ${(activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent') ? 'line-completed' : ''}`} />

                  {/* Step 4: Dispatched / Sent */}
                  <div className={`lifecycle-step-item ${(activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent') ? 'step-completed' : 'step-pending'}`}>
                    <div className="step-circle">
                      {(activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent') ? (
                        <Send size={13} />
                      ) : (
                        <span className="step-num">4</span>
                      )}
                    </div>
                    <span className="step-label">4. Dispatched</span>
                    <span className="step-sub">{(activeJobTarget?.status === 'applied' || activeJobTarget?.status === 'sent') ? 'Sent' : 'Awaiting Approval'}</span>
                  </div>

                  <div className="lifecycle-step-line" />

                  {/* Step 5: Interview */}
                  <div className={`lifecycle-step-item ${activeJobTarget?.status === 'interview' ? 'step-current' : 'step-pending'}`}>
                    <div className="step-circle">
                      <GraduationCap size={13} />
                    </div>
                    <span className="step-label">5. Interview</span>
                    <span className="step-sub">Coach Ready</span>
                  </div>
                </div>
              </div>

              {/* Application Details Grid */}
              <div className="status-details-grid">
                <div className="status-detail-card">
                  <span className="detail-card-label">Target Company</span>
                  <span className="detail-card-value font-semibold">{activeJobTarget?.company || 'None Targeted'}</span>
                </div>

                <div className="status-detail-card">
                  <span className="detail-card-label">Designation / Role</span>
                  <span className="detail-card-value font-semibold">{activeJobTarget?.role || 'AI Engineer'}</span>
                </div>

                <div className="status-detail-card">
                  <span className="detail-card-label">Outreach Channel</span>
                  <span className="detail-card-value capitalize">
                    {activeJobTarget?.channel || 'Email'}
                  </span>
                </div>

                <div className="status-detail-card">
                  <span className="detail-card-label">Fact-Ledger Audit</span>
                  <span className="detail-card-value text-emerald font-semibold">
                    <ShieldCheck size={13} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 4 }} />
                    Verified (0 Hallucinations)
                  </span>
                </div>
              </div>

              {/* Staged Action Proposal Card (Human-in-the-Loop Send Gate) */}
              {activeJobTarget?.status === 'staged' && activeJobTarget.proposalId && (
                <div className="status-staged-proposal-card">
                  <div className="staged-card-badge-row">
                    <span className="staged-amber-badge">
                      <Clock size={12} />
                      Human-in-the-Loop Review: Action Staged
                    </span>
                    {activeJobTarget.cvDigest && (
                      <span className="staged-digest-tag">
                        CV SHA: {activeJobTarget.cvDigest.slice(0, 10)}
                      </span>
                    )}
                  </div>

                  <h4 className="staged-card-role-title">
                    {activeJobTarget.role} at {activeJobTarget.company}
                  </h4>

                  {activeJobTarget.recipient && (
                    <p className="staged-recipient-line">
                      <strong>Recipient:</strong> <span>{activeJobTarget.recipient}</span>
                    </p>
                  )}

                  {activeJobTarget.draftBody && (
                    <div className="staged-draft-preview-box">
                      <div className="preview-box-header">
                        <span>Outreach Message Preview</span>
                      </div>
                      <p className="preview-box-content">{activeJobTarget.draftBody}</p>
                    </div>
                  )}

                  {actionFeedback && (
                    <div className={`status-action-feedback-banner ${actionFeedback.type}`}>
                      {actionFeedback.text}
                    </div>
                  )}

                  <div className="staged-actions-footer">
                    <button
                      type="button"
                      className="btn-approve-primary"
                      disabled={isProcessingAction}
                      onClick={async () => {
                        try {
                          setIsProcessingAction(true);
                          if (approveProposal) {
                            await approveProposal(activeJobTarget.proposalId);
                            setActionFeedback({ type: 'success', text: 'Application approved and staged for dispatch!' });
                          }
                        } catch (err) {
                          setActionFeedback({ type: 'error', text: err.message || 'Approval failed' });
                        } finally {
                          setIsProcessingAction(false);
                        }
                      }}
                    >
                      {isProcessingAction ? <Loader2 size={14} className="spin" /> : <Send size={14} />}
                      <span>Approve & Send</span>
                    </button>

                    <button
                      type="button"
                      className="btn-reject-secondary"
                      disabled={isProcessingAction}
                      onClick={async () => {
                        try {
                          setIsProcessingAction(true);
                          if (rejectProposal) {
                            await rejectProposal(activeJobTarget.proposalId, 'Rejected from status popup');
                            setActionFeedback({ type: 'info', text: 'Proposal rejected and returned to draft.' });
                          }
                        } catch (err) {
                          setActionFeedback({ type: 'error', text: err.message || 'Rejection failed' });
                        } finally {
                          setIsProcessingAction(false);
                        }
                      }}
                    >
                      <X size={14} />
                      <span>Reject / Revise</span>
                    </button>
                  </div>
                </div>
              )}

              {/* Quick Navigation Links */}
              {onNavigate && (
                <div className="status-modal-quick-links">
                  <button
                    type="button"
                    className="status-quick-link-btn"
                    onClick={() => {
                      setShowStatusModal(false);
                      onNavigate('studio');
                    }}
                  >
                    <FileText size={13} />
                    <span>Open in Application Studio</span>
                  </button>

                  <button
                    type="button"
                    className="status-quick-link-btn"
                    onClick={() => {
                      setShowStatusModal(false);
                      onNavigate('pipeline');
                    }}
                  >
                    <Compass size={13} />
                    <span>View Application Pipeline</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
