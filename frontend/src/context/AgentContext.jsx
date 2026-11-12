import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from './AuthContext';

const AgentContext = createContext(null);

const CONVERSATIONS_STORAGE_KEY = 'jobeazy_agent_conversations';
const ACTIVE_CONVO_STORAGE_KEY = 'jobeazy_active_conversation_id';
const MESSAGES_PREFIX = 'jobeazy_messages_';

const DEFAULT_WELCOME_MESSAGE = {
  id: 'welcome-1',
  role: 'assistant',
  content: "Hello! I am your JobEazy Career Agent. I can continuously scan the radar for high-fit roles, tailor your LaTeX CV to match ATS requirements, verify every claim against your Fact Ledger, and stage outreach for your approval.",
  thought: null,
  ui_widget: null,
  timestamp: new Date().toISOString(),
};

export const AgentProvider = ({ children }) => {
  const { token, user, effectiveAccountId } = useAuth() || {};

  // 1. Conversations list with localStorage persistence
  const [conversations, setConversations] = useState(() => {
    try {
      const saved = localStorage.getItem(CONVERSATIONS_STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // 2. Active conversation ID with localStorage persistence
  const [activeConversationId, setActiveConversationId] = useState(() => {
    try {
      return localStorage.getItem(ACTIVE_CONVO_STORAGE_KEY) || null;
    } catch {
      return null;
    }
  });

  // 3. Messages state with instant cache hydration
  const [messages, setMessages] = useState(() => {
    try {
      const savedConvoId = localStorage.getItem(ACTIVE_CONVO_STORAGE_KEY);
      if (savedConvoId) {
        const savedMsgs = localStorage.getItem(`${MESSAGES_PREFIX}${savedConvoId}`);
        if (savedMsgs) {
          const parsed = JSON.parse(savedMsgs);
          if (Array.isArray(parsed) && parsed.length > 0) {
            return parsed;
          }
        }
      }
    } catch {}
    return [DEFAULT_WELCOME_MESSAGE];
  });

  const [isStreaming, setIsStreaming] = useState(false);
  const [activeThought, setActiveThought] = useState(null);
  const [activeTool, setActiveTool] = useState(null);
  const [isDockOpen, setIsDockOpen] = useState(false);
  const [dockWidth, setDockWidth] = useState(440);
  const [pendingProposals, setPendingProposals] = useState([]);

  const abortControllerRef = useRef(null);
  const initialSyncedRef = useRef(false);

  // Headers helper
  const getHeaders = useCallback(() => {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (effectiveAccountId) headers['X-Account-ID'] = effectiveAccountId;
    return headers;
  }, [token, effectiveAccountId]);

  // Persist messages whenever they change for the active conversation
  useEffect(() => {
    if (activeConversationId && messages.length > 0) {
      try {
        localStorage.setItem(`${MESSAGES_PREFIX}${activeConversationId}`, JSON.stringify(messages));
      } catch (e) {
        console.warn('Failed to cache messages:', e);
      }
    }
  }, [messages, activeConversationId]);

  // Persist conversations list whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem(CONVERSATIONS_STORAGE_KEY, JSON.stringify(conversations));
    } catch (e) {
      console.warn('Failed to cache conversations:', e);
    }
  }, [conversations]);

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

  // Fetch conversations from server
  const fetchConversations = useCallback(async () => {
    try {
      const url = effectiveAccountId 
        ? `/api/v1/agent/conversations?account_id=${effectiveAccountId}&limit=30`
        : `/api/v1/agent/conversations?limit=30`;
      const res = await fetch(url, { headers: getHeaders() });
      if (res.ok) {
        const serverConvos = await res.json();
        if (Array.isArray(serverConvos)) {
          setConversations((prev) => {
            const mergedMap = new Map();
            serverConvos.forEach((c) => mergedMap.set(c.id, c));
            prev.forEach((c) => {
              if (!mergedMap.has(c.id)) mergedMap.set(c.id, c);
            });
            return Array.from(mergedMap.values()).sort(
              (a, b) => new Date(b.updated_at || b.created_at) - new Date(a.updated_at || a.created_at)
            );
          });
        }
      }
    } catch (err) {
      console.warn('Failed to fetch conversations from server, using local cache:', err);
    }
  }, [effectiveAccountId, getHeaders]);


  // Select a conversation from history
  const selectConversation = useCallback(async (conversationId) => {
    if (!conversationId) return;
    setActiveConversationId(conversationId);
    try {
      localStorage.setItem(ACTIVE_CONVO_STORAGE_KEY, conversationId);
      
      // 1. Instant local cache hydration
      const cached = localStorage.getItem(`${MESSAGES_PREFIX}${conversationId}`);
      if (cached) {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setMessages(parsed);
        }
      }

      // 2. Fetch full conversation from backend to ensure complete sync
      const url = effectiveAccountId
        ? `/api/v1/agent/conversations/${conversationId}?account_id=${effectiveAccountId}`
        : `/api/v1/agent/conversations/${conversationId}`;
      const res = await fetch(url, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        if (data.messages && Array.isArray(data.messages)) {
          const formatted = data.messages.map((m) => ({
            id: m.id,
            role: m.role,
            content: m.content,
            thought: m.thought,
            ui_widget: m.ui_widget,
            tool_calls: m.tool_calls,
            timestamp: m.created_at,
          }));
          if (formatted.length > 0) {
            setMessages(formatted);
            localStorage.setItem(`${MESSAGES_PREFIX}${conversationId}`, JSON.stringify(formatted));
          }
        }
      }
    } catch (err) {
      console.warn('Failed to sync conversation:', err);
    }
  }, [effectiveAccountId, getHeaders]);

  // Reset conversation to a new chat
  const resetConversation = useCallback(() => {
    setActiveConversationId(null);
    try {
      localStorage.removeItem(ACTIVE_CONVO_STORAGE_KEY);
    } catch {}
    setMessages([
      {
        ...DEFAULT_WELCOME_MESSAGE,
        id: 'welcome-' + Date.now(),
        timestamp: new Date().toISOString(),
      }
    ]);
  }, []);

  // Delete a conversation from history
  const deleteConversation = useCallback(async (conversationId, e) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    try {
      setConversations((prev) => prev.filter((c) => c.id !== conversationId));
      localStorage.removeItem(`${MESSAGES_PREFIX}${conversationId}`);

      const url = effectiveAccountId
        ? `/api/v1/agent/conversations/${conversationId}?account_id=${effectiveAccountId}`
        : `/api/v1/agent/conversations/${conversationId}`;
      await fetch(url, { method: 'DELETE', headers: getHeaders() });

      if (activeConversationId === conversationId) {
        resetConversation();
      }
    } catch (err) {
      console.warn('Failed to delete conversation:', err);
    }
  }, [effectiveAccountId, getHeaders, activeConversationId, resetConversation]);

  // Rename conversation title
  const renameConversation = useCallback(async (conversationId, newTitle) => {
    if (!conversationId || !newTitle || !newTitle.trim()) return;
    const trimmed = newTitle.trim();
    setConversations((prev) =>
      prev.map((c) => (c.id === conversationId ? { ...c, title: trimmed } : c))
    );
    try {
      const url = effectiveAccountId
        ? `/api/v1/agent/conversations/${conversationId}?account_id=${effectiveAccountId}`
        : `/api/v1/agent/conversations/${conversationId}`;
      await fetch(url, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify({ title: trimmed }),
      });
    } catch (err) {
      console.warn('Failed to rename conversation:', err);
    }
  }, [effectiveAccountId, getHeaders]);

  // Toggle pin conversation
  const togglePinConversation = useCallback(async (conversationId, isPinned) => {
    if (!conversationId) return;
    setConversations((prev) =>
      prev.map((c) => (c.id === conversationId ? { ...c, is_pinned: isPinned } : c))
    );
    try {
      const url = effectiveAccountId
        ? `/api/v1/agent/conversations/${conversationId}?account_id=${effectiveAccountId}`
        : `/api/v1/agent/conversations/${conversationId}`;
      await fetch(url, {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify({ is_pinned: isPinned }),
      });
    } catch (err) {
      console.warn('Failed to toggle pin state:', err);
    }
  }, [effectiveAccountId, getHeaders]);

  // Upload files and extract data/text
  const uploadFiles = useCallback(async (fileList) => {
    if (!fileList || fileList.length === 0) return [];
    const formData = new FormData();
    Array.from(fileList).forEach((f) => formData.append('files', f));

    const url = effectiveAccountId
      ? `/api/v1/agent/upload?account_id=${effectiveAccountId}`
      : `/api/v1/agent/upload`;

    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    if (effectiveAccountId) headers['X-Account-ID'] = effectiveAccountId;

    const res = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    });
    if (res.ok) {
      const data = await res.json();
      return data.files || [];
    } else {
      throw new Error(`Upload failed with status ${res.status}`);
    }
  }, [effectiveAccountId, token]);

  // Initial Sync & Polling on Mount
  useEffect(() => {
    fetchProposals();
    fetchConversations();
    if (!initialSyncedRef.current && activeConversationId) {
      initialSyncedRef.current = true;
      selectConversation(activeConversationId);
    }
  }, [fetchProposals, fetchConversations, activeConversationId, selectConversation]);

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

  // Send message with SSE streaming and optional file attachments
  const sendMessage = useCallback(async (userPrompt, contextFilters = {}, attachments = []) => {
    if ((!userPrompt || !userPrompt.trim()) && (!attachments || attachments.length === 0)) return;

    const trimmedPrompt = (userPrompt || '').trim();
    const userMsgId = 'user-' + Date.now();
    const assistantMsgId = 'assistant-' + Date.now();

    // 1. Optimistic user turn with file attachments widget if any
    const userWidget = attachments && attachments.length > 0
      ? { type: 'AttachmentList', props: { files: attachments } }
      : null;

    setMessages((prev) => [
      ...prev,
      {
        id: userMsgId,
        role: 'user',
        content: trimmedPrompt,
        ui_widget: userWidget,
        timestamp: new Date().toISOString(),
      },
      {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        thought: '',
        actionLabel: 'Connecting to Career Agent...',
        steps: [
          { type: 'status', label: 'Connecting to Career Agent...', timestamp: Date.now() }
        ],
        ui_widget: null,
        timestamp: new Date().toISOString(),
      }
    ]);

    setIsStreaming(true);
    setActiveThought('Connecting to Career Agent...');
    setActiveTool(null);

    // If starting a fresh chat session without an ID yet, create optimistic entry
    const isNewSession = !activeConversationId;
    const tempSessionId = 'temp-' + Date.now();

    const targetJob = contextFilters?.targetJob || contextFilters?.job;
    let titleSnippet;
    if (targetJob && targetJob.company && targetJob.role) {
      titleSnippet = `${targetJob.company} - ${targetJob.role}`;
    } else {
      const match = trimmedPrompt.match(/(?:for|at)\s+([A-Za-z0-9\s/+#.-]+?)\s+at\s+([A-Za-z0-9\s/+#.-]+)/i);
      if (match && match[1] && match[2] && !match[1].toLowerCase().includes('application')) {
        titleSnippet = `${match[2].trim()} - ${match[1].trim()}`;
      } else {
        titleSnippet = trimmedPrompt.slice(0, 32) + (trimmedPrompt.length > 32 ? '...' : '');
      }
    }

    if (isNewSession) {
      const optimisticConvo = {
        id: tempSessionId,
        title: titleSnippet,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setConversations((prev) => [optimisticConvo, ...prev]);
    }

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
          attachments: attachments,
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
                    m.id === assistantMsgId
                      ? {
                          ...m,
                          thought: latestThought,
                          actionLabel: frame.content ? 'Analyzing intent & profile context...' : m.actionLabel,
                          steps: [
                            ...(m.steps || []).filter((s) => s.type !== 'thought'),
                            {
                              type: 'thought',
                              label: 'Planning & Reasoning',
                              content: frame.content,
                              timestamp: Date.now(),
                            },
                          ],
                        }
                      : m
                  )
                );
              } else if (frame.type === 'tool_start') {
                const toolName = frame.tool;
                const toolLabel = `Executing ${toolName.replace(/_/g, ' ')}...`;
                setActiveTool({ tool: toolName, arguments: frame.arguments });
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId
                      ? {
                          ...m,
                          actionLabel: toolLabel,
                          steps: [
                            ...(m.steps || []),
                            {
                              type: 'tool',
                              tool: toolName,
                              label: toolLabel,
                              status: 'running',
                              arguments: frame.arguments,
                              timestamp: Date.now(),
                            },
                          ],
                        }
                      : m
                  )
                );
              } else if (frame.type === 'tool_complete') {
                if (frame.ui_widget) {
                  latestWidget = frame.ui_widget;
                  const p = frame.ui_widget.props;
                  if (p && p.company && (p.role || p.job_role)) {
                    const compRoleTitle = `${p.company} - ${p.role || p.job_role}`;
                    setConversations((prev) =>
                      prev.map((c) =>
                        (c.id === activeConversationId || c.id === tempSessionId)
                          ? { ...c, title: compRoleTitle }
                          : c
                      )
                    );
                  }
                }
                const toolName = frame.tool;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId
                      ? {
                          ...m,
                          ui_widget: latestWidget || m.ui_widget,
                          tool_calls: [{ name: toolName, summary: frame.summary }],
                          actionLabel: frame.summary || `Completed ${toolName.replace(/_/g, ' ')}`,
                          steps: (m.steps || []).map((s) =>
                            s.type === 'tool' && s.tool === toolName
                              ? { ...s, status: 'completed', summary: frame.summary }
                              : s
                          ),
                        }
                      : m
                  )
                );
              } else if (frame.type === 'proposal_created') {
                fetchProposals();
                if (frame.ui_widget) {
                  latestWidget = frame.ui_widget;
                  const p = frame.ui_widget.props;
                  if (p && p.company && (p.job_role || p.role)) {
                    const compRoleTitle = `${p.company} - ${p.job_role || p.role}`;
                    setConversations((prev) =>
                      prev.map((c) =>
                        (c.id === activeConversationId || c.id === tempSessionId)
                          ? { ...c, title: compRoleTitle }
                          : c
                      )
                    );
                  }
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
                    m.id === assistantMsgId
                      ? {
                          ...m,
                          content: accumulatedText,
                          actionLabel: 'Synthesizing response with Fact Ledger audit...',
                        }
                      : m
                  )
                );
              } else if (frame.type === 'done' || lines[i - 1]?.startsWith('event: done')) {
                if (frame.conversation_id) {
                  const realId = frame.conversation_id;
                  const resolvedTitle = frame.title || titleSnippet;
                  setActiveConversationId(realId);
                  localStorage.setItem(ACTIVE_CONVO_STORAGE_KEY, realId);
                  setConversations((prev) => {
                    const filtered = prev.filter((c) => c.id !== tempSessionId && c.id !== realId);
                    return [
                      {
                        id: realId,
                        title: resolvedTitle,
                        created_at: new Date().toISOString(),
                        updated_at: new Date().toISOString(),
                      },
                      ...filtered,
                    ];
                  });
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
      fetchConversations();
    }
  }, [effectiveAccountId, activeConversationId, getHeaders, fetchProposals, fetchConversations]);

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

      setMessages((prev) =>
        prev.map((m) => {
          if (m.ui_widget?.type === 'SendApprovalGate' && m.ui_widget.props?.proposal_id === proposalId) {
            return {
              ...m,
              ui_widget: {
                ...m.ui_widget,
                props: {
                  ...m.ui_widget.props,
                  status: result.status || 'queued',
                  undo_expires_at: result.undo_expires_at,
                  hold_queue_item_id: result.hold_queue_item_id,
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

  // Human-in-the-loop Cancel during Undo Window
  const cancelProposal = useCallback(async (proposalId) => {
    try {
      const url = effectiveAccountId
        ? `/api/v1/agent/proposals/${proposalId}/cancel?account_id=${effectiveAccountId}`
        : `/api/v1/agent/proposals/${proposalId}/cancel`;

      const res = await fetch(url, {
        method: 'POST',
        headers: getHeaders(),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to cancel dispatch');
      }

      const result = await res.json();

      setMessages((prev) =>
        prev.map((m) => {
          if (m.ui_widget?.type === 'SendApprovalGate' && m.ui_widget.props?.proposal_id === proposalId) {
            return {
              ...m,
              ui_widget: {
                ...m.ui_widget,
                props: {
                  ...m.ui_widget.props,
                  status: 'aborted',
                  abort_reason: 'user_cancelled',
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
      console.error('Error cancelling proposal:', err);
      throw err;
    }
  }, [effectiveAccountId, getHeaders, fetchProposals]);

  const toggleDock = useCallback(() => setIsDockOpen((prev) => !prev), []);
  const openDock = useCallback(() => setIsDockOpen(true), []);
  const closeDock = useCallback(() => setIsDockOpen(false), []);

  const value = {
    messages,
    isStreaming,
    activeThought,
    activeTool,
    isDockOpen,
    dockWidth,
    pendingProposals,
    proposalsCount: pendingProposals.length,
    activeConversationId,
    conversations,
    sendMessage,
    selectConversation,
    deleteConversation,
    renameConversation,
    togglePinConversation,
    uploadFiles,
    approveProposal,
    rejectProposal,
    cancelProposal,
    fetchProposals,
    fetchConversations,
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
