import React, { useState, useRef, useEffect } from 'react';
import {
  Bot,
  Sparkles,
  Send,
  X,
  ChevronRight,
  ChevronDown,
  Lightbulb,
  Loader2,
  RefreshCw,
  Clock,
  Layers,
  ArrowUpRight,
  Cpu,
  Minimize2,
} from 'lucide-react';
import { useAgent } from '../../hooks/useAgent';
import RenderWidget from './widgets/WidgetRegistry';

const QUICK_CHIPS = [
  { label: '⚡ Run Daily Radar Scan', prompt: 'Run daily radar scan for matching AI Engineer jobs' },
  { label: '🎯 Auto-Tailor Top Match', prompt: 'Auto-tailor my CV for the highest scoring job match' },
  { label: '📬 Draft Due Follow-Ups', prompt: 'Check which applications are due for follow-ups and draft them' },
  { label: '🎙 Practice Interview', prompt: 'Practice technical interview with STAR method for system scalability' },
  { label: '🔍 Reflect Profile', prompt: 'Reflect candidate profile and summarize verified accomplishments' },
];

export default function CareerAgentDock({ activeContext = {} }) {
  const {
    messages,
    isStreaming,
    activeThought,
    activeTool,
    isDockOpen,
    dockWidth,
    proposalsCount,
    sendMessage,
    toggleDock,
    closeDock,
    setDockWidth,
  } = useAgent();

  const [input, setInput] = useState('');
  const [expandedThoughts, setExpandedThoughts] = useState({});
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isStreaming, activeThought]);

  // Focus input when dock opens
  useEffect(() => {
    if (isDockOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isDockOpen]);

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

  // Resize handler
  const handleMouseDownResize = (e) => {
    e.preventDefault();
    const startX = e.clientX;
    const startWidth = dockWidth;

    const onMouseMove = (moveEvent) => {
      const delta = startX - moveEvent.clientX;
      const newWidth = Math.min(640, Math.max(380, startWidth + delta));
      setDockWidth(newWidth);
    };

    const onMouseUp = () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  };

  if (!isDockOpen) {
    return (
      <button
        type="button"
        className="floating-agent-trigger"
        onClick={toggleDock}
        title="Open Career Agent Copilot (⌘J)"
      >
        <div className="trigger-icon-wrap">
          <Bot size={20} className="agent-trigger-bot" />
          <span className="pulse-emitter" />
        </div>
        <span className="trigger-label">Career Copilot</span>
        {proposalsCount > 0 && (
          <span className="trigger-proposals-badge">{proposalsCount}</span>
        )}
        <span className="trigger-shortcut-hint">⌘J</span>
      </button>
    );
  }

  return (
    <aside
      className="career-agent-dock-panel"
      style={{ width: `${dockWidth}px` }}
      aria-label="Autonomous Career Agent Copilot"
    >
      {/* Draggable resize handle on left border */}
      <div
        className="dock-resize-handle"
        onMouseDown={handleMouseDownResize}
        title="Drag to resize copilot drawer"
      />

      {/* Dock Header */}
      <div className="dock-header">
        <div className="dock-header-identity">
          <div className="agent-avatar-wrap">
            <Bot size={18} className="text-emerald" />
            <span className={`status-dot ${isStreaming ? 'streaming' : 'idle'}`} />
          </div>
          <div className="agent-header-titles">
            <div className="dock-title-row">
              <span className="dock-title">Career Copilot</span>
              <span className="autonomy-badge">AUTONOMOUS</span>
            </div>
            <span className="dock-subtitle">Fact-verified talent agent</span>
          </div>
        </div>

        <div className="dock-header-controls">
          {proposalsCount > 0 && (
            <div className="proposals-pill" title={`${proposalsCount} staged action(s) awaiting review`}>
              <Clock size={12} />
              <span>{proposalsCount} Staged</span>
            </div>
          )}
          <button
            type="button"
            className="dock-icon-btn"
            onClick={closeDock}
            title="Minimize Copilot (⌘J)"
          >
            <Minimize2 size={16} />
          </button>
        </div>
      </div>

      {/* Message List */}
      <div className="dock-messages-scroll">
        {messages.map((msg) => {
          const isUser = msg.role === 'user';
          const hasThought = Boolean(msg.thought);
          const isThoughtOpen = expandedThoughts[msg.id];

          return (
            <div key={msg.id} className={`agent-message-row ${isUser ? 'user-turn' : 'assistant-turn'}`}>
              <div className="turn-avatar">
                {isUser ? (
                  <span className="user-initials">ME</span>
                ) : (
                  <Bot size={15} className="text-emerald" />
                )}
              </div>

              <div className="turn-content-box">
                {/* Collapsible Chain-of-Thought Disclosure */}
                {hasThought && !isUser && (
                  <div className="thought-disclosure-block">
                    <button
                      type="button"
                      className="thought-toggle-btn"
                      onClick={() => toggleThought(msg.id)}
                    >
                      <Lightbulb size={12} className="text-amber" />
                      <span>{isThoughtOpen ? 'Hide Agent Reasoning' : 'Show Agent Reasoning'}</span>
                      {isThoughtOpen ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
                    </button>
                    {isThoughtOpen && (
                      <div className="thought-body">
                        <p>{msg.thought}</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Message Body */}
                {msg.content && (
                  <div className="message-markdown-text">
                    <p>{msg.content}</p>
                  </div>
                )}

                {/* Generative UI Widget */}
                {msg.ui_widget && (
                  <div className="message-widget-container">
                    <RenderWidget widget={msg.ui_widget} />
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Live Streaming Indicator */}
        {isStreaming && (
          <div className="agent-streaming-indicator">
            <Loader2 size={14} className="spin text-emerald" />
            <span className="streaming-status-text">
              {activeTool
                ? `Running ${activeTool.tool}...`
                : activeThought || 'Synthesizing response...'}
            </span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Fast-Track Prompt Chips */}
      <div className="dock-quick-chips">
        {QUICK_CHIPS.map((chip, idx) => (
          <button
            key={idx}
            type="button"
            className="quick-chip-btn"
            disabled={isStreaming}
            onClick={() => sendMessage(chip.prompt, activeContext)}
          >
            <span>{chip.label}</span>
          </button>
        ))}
      </div>

      {/* Dock Input Bar */}
      <form className="dock-input-bar" onSubmit={handleSubmit}>
        <textarea
          ref={inputRef}
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask Copilot or request action... (Enter to send)"
          disabled={isStreaming}
          className="dock-textarea"
        />
        <button
          type="submit"
          className="dock-send-btn"
          disabled={!input.trim() || isStreaming}
          title="Send to Copilot"
        >
          {isStreaming ? (
            <Loader2 size={16} className="spin" />
          ) : (
            <Send size={15} />
          )}
        </button>
      </form>
    </aside>
  );
}
