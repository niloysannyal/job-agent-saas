import React, { useState, useRef, useEffect } from 'react';
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
  PanelLeftOpen,
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
}) {
  const {
    messages,
    isStreaming,
    activeThought,
    activeTool,
    proposalsCount = 0,
    sendMessage,
    resetConversation,
  } = useAgent();

  const [input, setInput] = useState('');
  const [expandedThoughts, setExpandedThoughts] = useState({});
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

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

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input, activeContext);
    setInput('');
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

  return (
    <div className="copilot-fullscreen-view" role="main" aria-label="Career Copilot Autonomous Operating System">
      {/* Top Header Bar (ChatGPT / Claude Style) */}
      <header className="copilot-topbar">
        <div className="copilot-topbar-left">
          {isSidebarCollapsed && onExpandSidebar && (
            <button
              type="button"
              className="copilot-expand-sidebar-btn"
              onClick={onExpandSidebar}
              title="Expand sidebar (⌘\)"
              aria-label="Expand sidebar"
            >
              <PanelLeftOpen size={18} />
            </button>
          )}
          <div className="copilot-brand-icon">
            <Bot size={20} className="text-emerald" />
            <span className="copilot-status-dot" />
          </div>
          <div className="copilot-title-group">
            <div className="copilot-title-row">
              <h2 className="copilot-main-title">Career Copilot</h2>
              <span className="copilot-pill-badge">AUTONOMOUS</span>
              <span className="copilot-model-pill">GPT-4o / Claude 3.5 Sonnet</span>
            </div>
            <span className="copilot-subtitle-desc">
              Fact-Verified Agent • Continuous Job Radar, ATS CV Tailoring & Human-in-the-Loop Send Gate
            </span>
          </div>
        </div>

        <div className="copilot-topbar-right">
          {proposalsCount > 0 && (
            <div className="copilot-top-proposals-pill" title={`${proposalsCount} staged action(s) awaiting your review`}>
              <Clock size={13} />
              <span>{proposalsCount} Action{proposalsCount > 1 ? 's' : ''} Staged</span>
            </div>
          )}
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

              return (
                <article
                  key={msg.id}
                  className={`copilot-turn-container ${isUser ? 'user-turn-container' : 'assistant-turn-container'}`}
                >
                  <div className="turn-avatar-badge">
                    {isUser ? (
                      <span className="user-initials-txt">ME</span>
                    ) : (
                      <div className="assistant-bot-avatar">
                        <Bot size={16} className="text-emerald" />
                      </div>
                    )}
                  </div>

                  <div className="turn-body-content">
                    {/* Collapsible Chain-of-Thought Disclosure */}
                    {hasThought && !isUser && (
                      <div className="copilot-thought-accordion">
                        <button
                          type="button"
                          className="thought-accordion-trigger"
                          onClick={() => toggleThought(msg.id)}
                          aria-expanded={isThoughtOpen}
                        >
                          <Lightbulb size={13} className="text-amber" />
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

          {/* Composer Form Input Box */}
          <form className="copilot-input-box" onSubmit={handleSubmit}>
            <textarea
              ref={inputRef}
              rows={2}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask Career Copilot or request autonomous action... (Shift+Enter for newline)"
              disabled={isStreaming}
              className="copilot-prompt-textarea"
            />

            <div className="copilot-input-actions">
              <button
                type="submit"
                className="copilot-send-button"
                disabled={!input.trim() || isStreaming}
                title="Send message to Career Copilot (Enter)"
                aria-label="Send message"
              >
                {isStreaming ? (
                  <Loader2 size={16} className="spin" />
                ) : (
                  <Send size={15} />
                )}
              </button>
            </div>
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
    </div>
  );
}

