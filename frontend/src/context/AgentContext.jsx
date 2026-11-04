import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from './AuthContext';

const AgentContext = createContext(null);

export const AgentProvider = ({ children }) => {
  const { token, user, effectiveAccountId } = useAuth() || {};

  const [messages, setMessages] = useState([
    {
      id: 'welcome-1',
      role: 'assistant',
      content: "Hello! I am your JobEazy Career Agent. I can continuously scan the radar for high-fit roles, tailor your LaTeX CV to match ATS requirements, verify every claim against your Fact Ledger, and stage outreach for your approval.",
      thought: null,
      ui_widget: null,
      timestamp: new Date().toISOString(),
    }
  ]);

  const [isStreaming, setIsStreaming] = useState(false);
  const [activeThought, setActiveThought] = useState(null);
  const [activeTool, setActiveTool] = useState(null);
  const [isDockOpen, setIsDockOpen] = useState(false);
  const [dockWidth, setDockWidth] = useState(440);
  const [pendingProposals, setPendingProposals] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);

  const abortControllerRef = useRef(null);

  // Headers helper
  const getHeaders = useCallback(() => {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (effectiveAccountId) headers['X-Account-ID'] = effectiveAccountId;
    return headers;
  }, [token, effectiveAccountId]);

  // Fetch pending proposals
  const fetchProposals = useCallback(async () => {
    try {
      const url = effectiveAccountId 
        ? `/api/v1/agent/proposals?proposal_status=pending&account_id=${effectiveAccountId}`
        : `/api/v1/agent/proposals?proposal_status=pending`;
      const res = await fetch(url, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setPendingProposals(data);
      }
    } catch (err) {
      console.warn('Failed to fetch action proposals:', err);
    }
  }, [effectiveAccountId, getHeaders]);

  useEffect(() => {
    fetchProposals();
  }, [fetchProposals]);

  // Global Keyboard Shortcut: ⌘J / Ctrl+J
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'j') {
        e.preventDefault();
        setIsDockOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Send message with SSE streaming
  const sendMessage = useCallback(async (userPrompt, contextFilters = {}) => {
    if (!userPrompt || !userPrompt.trim()) return;

    const trimmedPrompt = userPrompt.trim();
    const userMsgId = 'user-' + Date.now();
    const assistantMsgId = 'assistant-' + Date.now();

    // 1. Optimistic user turn
    setMessages((prev) => [
      ...prev,
      {
        id: userMsgId,
        role: 'user',
        content: trimmedPrompt,
        timestamp: new Date().toISOString(),
      },
      {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        thought: 'Initializing reasoning...',
        ui_widget: null,
        timestamp: new Date().toISOString(),
      }
    ]);

    setIsStreaming(true);
    setActiveThought('Connecting to Career Agent...');
    setActiveTool(null);

    try {
      abortControllerRef.current = new AbortController();
      const chatUrl = effectiveAccountId
        ? `/api/v1/agent/chat?account_id=${effectiveAccountId}`
        : `/api/v1/agent/chat`;

      const response = await fetch(chatUrl, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({
          message: trimmedPrompt,
          conversation_id: activeConversationId,
          context_filters: contextFilters,
        }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`Agent API returned ${response.status}: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      let accumulatedText = '';
      let latestWidget = null;
      let latestThought = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // keep last incomplete line in buffer

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i].trim();
          if (line.startsWith('data:')) {
            const rawJson = line.replace('data:', '').trim();
            if (!rawJson) continue;
            try {
              const frame = JSON.parse(rawJson);
              
              if (frame.type === 'thought') {
                latestThought = frame.content;
                setActiveThought(frame.content);
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId ? { ...m, thought: latestThought } : m
                  )
                );
              } else if (frame.type === 'tool_start') {
                setActiveTool({ tool: frame.tool, arguments: frame.arguments });
              } else if (frame.type === 'tool_complete') {
                if (frame.ui_widget) {
                  latestWidget = frame.ui_widget;
                }
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId
                      ? {
                          ...m,
                          ui_widget: latestWidget || m.ui_widget,
                          tool_calls: [{ name: frame.tool, summary: frame.summary }],
                        }
                      : m
                  )
                );
              } else if (frame.type === 'proposal_created') {
                fetchProposals();
                if (frame.ui_widget) {
                  latestWidget = frame.ui_widget;
                  setMessages((prev) =>
                    prev.map((m) =>
                      m.id === assistantMsgId ? { ...m, ui_widget: latestWidget } : m
                    )
                  );
                }
              } else if (frame.type === 'text_chunk') {
                accumulatedText += frame.content;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId ? { ...m, content: accumulatedText } : m
                  )
                );
              } else if (frame.type === 'done' || lines[i - 1]?.startsWith('event: done')) {
                if (frame.conversation_id) {
                  setActiveConversationId(frame.conversation_id);
                }
              }
            } catch (err) {
              console.debug('SSE frame parse error:', err, rawJson);
            }
          }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('Agent chat error:', err);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId
              ? {
                  ...m,
                  content: m.content || `Agent encountered an error: ${err.message}`,
                  thought: 'Execution interrupted.',
                }
              : m
          )
        );
      }
    } finally {
      setIsStreaming(false);
      setActiveThought(null);
      setActiveTool(null);
      fetchProposals();
    }
  }, [effectiveAccountId, activeConversationId, getHeaders, fetchProposals]);

  // Human-in-the-loop Approve
  const approveProposal = useCallback(async (proposalId, feedback = null) => {
    try {
      const url = effectiveAccountId
        ? `/api/v1/agent/proposals/${proposalId}/approve?account_id=${effectiveAccountId}`
        : `/api/v1/agent/proposals/${proposalId}/approve`;

      const res = await fetch(url, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ feedback }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to approve proposal');
      }

      const result = await res.json();

      // Optimistically update widget in messages
      setMessages((prev) =>
        prev.map((m) => {
          if (m.ui_widget?.type === 'SendApprovalGate' && m.ui_widget.props?.proposal_id === proposalId) {
            return {
              ...m,
              ui_widget: {
                ...m.ui_widget,
                props: {
                  ...m.ui_widget.props,
                  status: 'executed',
                },
              },
            };
          }
          return m;
        })
      );

      fetchProposals();
      return result;
    } catch (err) {
      console.error('Error approving proposal:', err);
      throw err;
    }
  }, [effectiveAccountId, getHeaders, fetchProposals]);

  // Human-in-the-loop Reject
  const rejectProposal = useCallback(async (proposalId, feedback = null) => {
    try {
      const url = effectiveAccountId
        ? `/api/v1/agent/proposals/${proposalId}/reject?account_id=${effectiveAccountId}`
        : `/api/v1/agent/proposals/${proposalId}/reject`;

      const res = await fetch(url, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ feedback }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to reject proposal');
      }

      setMessages((prev) =>
        prev.map((m) => {
          if (m.ui_widget?.type === 'SendApprovalGate' && m.ui_widget.props?.proposal_id === proposalId) {
            return {
              ...m,
              ui_widget: {
                ...m.ui_widget,
                props: {
                  ...m.ui_widget.props,
                  status: 'rejected',
                },
              },
            };
          }
          return m;
        })
      );

      fetchProposals();
    } catch (err) {
      console.error('Error rejecting proposal:', err);
      throw err;
    }
  }, [effectiveAccountId, getHeaders, fetchProposals]);

  const toggleDock = useCallback(() => setIsDockOpen((prev) => !prev), []);
  const openDock = useCallback(() => setIsDockOpen(true), []);
  const closeDock = useCallback(() => setIsDockOpen(false), []);

  const resetConversation = useCallback(() => {
    setActiveConversationId(null);
    setMessages([
      {
        id: 'welcome-' + Date.now(),
        role: 'assistant',
        content: 'Hello! I am your JobEazy Career Agent. I can continuously scan the radar for high-fit roles, tailor your LaTeX CV to match ATS requirements, verify every claim against your Fact Ledger, and stage outreach for your approval.',
        thought: null,
        ui_widget: null,
        timestamp: new Date().toISOString(),
      }
    ]);
  }, []);
  const value = {
    messages,
    isStreaming,
    activeThought,
    activeTool,
    isDockOpen,
    dockWidth,
    pendingProposals,
    proposalsCount: pendingProposals.length,
    sendMessage,
    approveProposal,
    rejectProposal,
    fetchProposals,
    toggleDock,
    openDock,
    closeDock,
    setDockWidth,
    resetConversation,
  };

  return <AgentContext.Provider value={value}>{children}</AgentContext.Provider>;
};

export const useAgent = () => {
  const ctx = useContext(AgentContext);
  if (!ctx) {
    throw new Error('useAgent must be used within an AgentProvider');
  }
  return ctx;
};
