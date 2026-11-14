import React, { useState, useRef, useEffect } from 'react';
import { useAgent } from '../hooks/useAgent';
import {
  Bot,
  LayoutDashboard,
  Briefcase,
  FileEdit,
  Kanban,
  GraduationCap,
  Sparkles,
  User,
  LogOut,
  ChevronUp,
  Users,
  ShieldCheck,
  ShieldAlert,
  Server,
  Layers,
  FileCode,
  FileText,
  Mail,
  Search,
  Moon,
  Sun,
  Laptop,
  PanelLeftClose,
  PanelLeftOpen,
  SquarePen,
  Plus,
  MessageSquare,
  Trash2,
  Pin,
  PinOff,
  Edit2,
  MoreHorizontal,
  ChevronDown,
  ChevronRight,
  Check,
  X,
} from 'lucide-react';

export default function Sidebar({
  activeSection,
  setActiveSection,
  adminTab = 'tenants',
  setAdminTab,
  profileName = 'Niloy Sannyal',
  tenantEmail = 'niloy@example.com',
  isSuperadmin = false,
  isImpersonating = false,
  onLogout,
  showToast,
  theme = 'dark',
  setTheme,
  toggleTheme,
  onOpenCommandPalette,
  isCollapsed = false,
  onToggleCollapse,
  onNewApplication,
}) {
  const {
    conversations = [],
    activeConversationId,
    selectConversation,
    deleteConversation,
    renameConversation,
    togglePinConversation,
    resetConversation,
    proposalsCount = 0,
  } = useAgent();

  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef(null);

  // Section collapse states (persisted)
  const [isPinnedExpanded, setIsPinnedExpanded] = useState(() => {
    try {
      const saved = localStorage.getItem('jobeazy_sidebar_pinned_expanded');
      return saved !== null ? saved === 'true' : true;
    } catch {
      return true;
    }
  });

  const [isRecentExpanded, setIsRecentExpanded] = useState(() => {
    try {
      const saved = localStorage.getItem('jobeazy_sidebar_recent_expanded');
      return saved !== null ? saved === 'true' : true;
    } catch {
      return true;
    }
  });

  // 3-dot dropdown menu & inline rename state
  const [activeMenuConvoId, setActiveMenuConvoId] = useState(null);
  const [editingConvoId, setEditingConvoId] = useState(null);
  const [editingTitle, setEditingTitle] = useState('');
  const menuRef = useRef(null);

  const togglePinnedSection = () => {
    setIsPinnedExpanded((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('jobeazy_sidebar_pinned_expanded', String(next));
      } catch {}
      return next;
    });
  };

  const toggleRecentSection = () => {
    setIsRecentExpanded((prev) => {
      const next = !prev;
      try {
        localStorage.setItem('jobeazy_sidebar_recent_expanded', String(next));
      } catch {}
      return next;
    });
  };

  // Close menus when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setShowProfileMenu(false);
      }
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setActiveMenuConvoId(null);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const navItems = [];

  if (isSuperadmin && !isImpersonating) {
    navItems.push(
      {
        id: 'overview',
        label: 'Platform Overview',
        icon: LayoutDashboard,
        isAdminTab: true,
      },
      {
        id: 'tenants',
        label: 'Tenants & Workspaces',
        icon: Users,
        isAdminTab: true,
      },
      {
        id: 'providers',
        label: 'Dynamic LLM Providers',
        icon: Server,
        isAdminTab: true,
      },
      {
        id: 'sources',
        label: 'Job Sources & Feeds',
        icon: Layers,
        isAdminTab: true,
      },
      {
        id: 'templates',
        label: 'Curated LaTeX Templates',
        icon: FileCode,
        isAdminTab: true,
      },
      {
        id: 'flagged',
        label: 'Posting Guard Flags',
        icon: ShieldAlert,
        isAdminTab: true,
      },
      {
        id: 'integrations',
        label: 'OAuth & Email Config',
        icon: Mail,
        isAdminTab: true,
      },
    );
  } else {
    navItems.push(
      {
        id: 'dashboard',
        label: 'Dashboard',
        icon: LayoutDashboard,
      },
      {
        id: 'jobs',
        label: 'Jobs & Radar',
        icon: Briefcase,
      },
      {
        id: 'builder',
        label: 'Resume Builder',
        icon: FileText,
      },
      {
        id: 'studio',
        label: 'Application Studio',
        icon: FileEdit,
      },
      {
        id: 'pipeline',
        label: 'Application Pipeline',
        icon: Kanban,
      },
      {
        id: 'interview',
        label: 'STAR Interview Coach',
        icon: GraduationCap,
      },
    );
  }

  // Derive user initials
  const initials =
    profileName
      .split(' ')
      .map((n) => n[0])
      .filter(Boolean)
      .slice(0, 2)
      .join('')
      .toUpperCase() || 'NS';

  const handleSelectOption = (sectionId, message) => {
    setShowProfileMenu(false);
    if (sectionId) {
      setActiveSection(sectionId);
    }
    if (message && showToast) {
      showToast(message);
    }
  };

  const handleLogoutClick = () => {
    setShowProfileMenu(false);
    if (onLogout) {
      onLogout();
    } else if (showToast) {
      showToast('Logged out of session. (Multi-tenant mode ready)');
    }
  };

  // Split into pinned and recent
  const pinnedList = conversations.filter((c) => Boolean(c.is_pinned));
  const recentList = conversations.filter((c) => !c.is_pinned);

  // Render an individual conversation item (with 3-dot dropdown menu)
  const renderConvoItem = (convo) => {
    const isSelected = activeSection === 'copilot' && activeConversationId === convo.id;
    const isEditing = editingConvoId === convo.id;
    const isMenuOpen = activeMenuConvoId === convo.id;

    return (
      <div
        key={convo.id}
        className={`history-chat-item ${isSelected ? 'active' : ''}`}
        onClick={() => {
          if (!isEditing) {
            selectConversation(convo.id);
            setActiveSection('copilot');
          }
        }}
        title={convo.title || 'Career Session'}
      >
        <MessageSquare size={13} className="history-chat-icon" />

        {isEditing ? (
          <form
            className="history-inline-rename-form"
            onSubmit={(e) => {
              e.preventDefault();
              if (renameConversation) {
                renameConversation(convo.id, editingTitle);
              }
              setEditingConvoId(null);
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <input
              autoFocus
              type="text"
              value={editingTitle}
              onChange={(e) => setEditingTitle(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Escape') setEditingConvoId(null);
              }}
              className="history-inline-rename-input"
            />
            <button type="submit" className="rename-save-btn" title="Save">
              <Check size={11} />
            </button>
            <button
              type="button"
              className="rename-cancel-btn"
              title="Cancel"
              onClick={() => setEditingConvoId(null)}
            >
              <X size={11} />
            </button>
          </form>
        ) : (
          <span className="history-chat-title">{convo.title || 'Career Session'}</span>
        )}

        {!isEditing && (
          <div className="history-item-actions" onClick={(e) => e.stopPropagation()}>
            <button
              type="button"
              className={`history-more-btn ${isMenuOpen ? 'active' : ''}`}
              onClick={(e) => {
                e.stopPropagation();
                setActiveMenuConvoId(isMenuOpen ? null : convo.id);
              }}
              title="Chat options"
              aria-label="Chat options"
            >
              <MoreHorizontal size={14} />
            </button>

            {isMenuOpen && (
              <div className="convo-dropdown-menu" ref={menuRef}>
                <button
                  type="button"
                  className="convo-dropdown-item"
                  onClick={() => {
                    if (togglePinConversation) {
                      togglePinConversation(convo.id, !convo.is_pinned);
                    }
                    setActiveMenuConvoId(null);
                  }}
                >
                  {convo.is_pinned ? (
                    <>
                      <PinOff size={13} />
                      <span>Unpin</span>
                    </>
                  ) : (
                    <>
                      <Pin size={13} />
                      <span>Pin</span>
                    </>
                  )}
                </button>
                <button
                  type="button"
                  className="convo-dropdown-item"
                  onClick={() => {
                    setEditingConvoId(convo.id);
                    setEditingTitle(convo.title || '');
                    setActiveMenuConvoId(null);
                  }}
                >
                  <Edit2 size={13} />
                  <span>Rename</span>
                </button>
                <button
                  type="button"
                  className="convo-dropdown-item text-danger"
                  onClick={(e) => {
                    if (deleteConversation) {
                      deleteConversation(convo.id, e);
                    }
                    setActiveMenuConvoId(null);
                  }}
                >
                  <Trash2 size={13} />
                  <span>Delete</span>
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <aside
      className={`app-sidebar ${isCollapsed ? 'sidebar-collapsed' : ''}`}
      aria-label="Sidebar Navigation"
    >
      {/* Top Header Group */}
      <div className="sidebar-top-group">
        {/* Brand Header Row with Collapse Toggle on the Right when Expanded */}
        <div className="sidebar-brand-row">
          {isCollapsed ? (
            <button
              type="button"
              className="sidebar-collapse-toggle-btn collapsed-toggle-btn"
              onClick={onToggleCollapse}
              title="Expand sidebar (⌘\)"
              aria-label="Expand sidebar"
            >
              <div className="brand-icon-box">
                <Sparkles className="icon-sparkles brand-icon-normal" />
                <PanelLeftOpen className="icon-toggle brand-icon-hover" size={18} />
              </div>
            </button>
          ) : (
            <>
              <div className="sidebar-brand">
                <div className="brand-icon-box">
                  <Sparkles className="icon-sparkles" />
                </div>
                <div className="brand-meta">
                  <h1 className="brand-title">JobEazy</h1>
                  <span className={`brand-account ${isSuperadmin && !isImpersonating ? 'text-emerald' : ''}`}>
                    {isSuperadmin && !isImpersonating ? 'SuperAdmin Ops Plane' : 'Autonomous Job Agent'}
                  </span>
                </div>
              </div>
              <button
                type="button"
                className="sidebar-collapse-toggle-btn"
                onClick={onToggleCollapse}
                title="Collapse sidebar (⌘\)"
                aria-label="Collapse sidebar"
              >
                <PanelLeftClose size={18} />
              </button>
            </>
          )}
        </div>

        {/* Global Command Palette Launcher Button (Clean borderless/backgroundless with Search icon) */}
        <button
          className={`sidebar-quick-search-btn ${isCollapsed ? 'btn-collapsed' : ''}`}
          onClick={onOpenCommandPalette}
          title={isCollapsed ? 'Search (⌘K)' : 'Search views, opportunities and actions'}
          aria-label="Open command palette"
        >
          <Search size={16} className="quick-search-icon" />
          {!isCollapsed && <span className="quick-search-label">Search...</span>}
        </button>

        {/* New Application Button (Unified New Chat + Career Copilot, ChatGPT/Claude style) */}
        {!isSuperadmin && (
          <button
            type="button"
            className={`sidebar-new-chat-top-btn ${isCollapsed ? 'btn-collapsed' : ''} ${activeSection === 'copilot' && !activeConversationId ? 'active' : ''}`}
            onClick={() => {
              if (onNewApplication) onNewApplication();
              resetConversation();
              setActiveSection('copilot');
            }}
            title={isCollapsed ? 'New Application (⌘N)' : 'Start new application'}
            aria-label="New Application"
          >
            <SquarePen size={16} className="new-chat-icon" />
            {!isCollapsed && <span className="new-chat-label">New Application</span>}
          </button>
        )}
      </div>

      {/* Scrollable Middle Content: Nav Items + Pinned + Recent directly below STAR Coach */}
      <div className="sidebar-middle-scroll">
        <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = item.isAdminTab
            ? (activeSection === 'admin' && adminTab === item.id)
            : (activeSection === item.id);
          return (
            <button
              key={item.id}
              onClick={() => {
                if (item.isAdminTab) {
                  setActiveSection('admin');
                  if (setAdminTab) setAdminTab(item.id);
                } else {
                  setActiveSection(item.id);
                }
              }}
              className={`nav-item-btn ${isActive ? 'active' : ''} ${isCollapsed ? 'nav-collapsed' : ''}`}
              id={`nav-btn-${item.id}`}
              title={isCollapsed ? item.label : undefined}
            >
              <div className="nav-item-left">
                <Icon className="nav-icon" />
                {!isCollapsed && <span className="nav-label">{item.label}</span>}
                {item.badge && (
                  <span className={isCollapsed ? 'nav-badge-dot' : 'nav-badge-pill'}>
                    {isCollapsed ? '' : item.badge}
                  </span>
                )}
              </div>
            </button>
          );
        })}
      </nav>

      {/* Pinned & Recent Accordion Sections (Candidate Mode) */}
      {!isSuperadmin && !isCollapsed && (
        <div className="sidebar-history-sections-wrap">
          {/* 1. Pinned Section */}
          <div className="sidebar-accordion-section">
            <button
              type="button"
              className="accordion-section-header"
              onClick={togglePinnedSection}
              aria-expanded={isPinnedExpanded}
            >
              <div className="section-header-left">
                {isPinnedExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                <span className="section-header-title">Pinned</span>
              </div>
              {pinnedList.length > 0 && (
                <span className="section-count-pill">{pinnedList.length}</span>
              )}
            </button>

            {isPinnedExpanded && (
              <div className="accordion-section-body">
                {pinnedList.length === 0 ? (
                  <div className="history-empty-hint">No pinned chats</div>
                ) : (
                  pinnedList.map(renderConvoItem)
                )}
              </div>
            )}
          </div>

          {/* 2. Recent Section */}
          <div className="sidebar-accordion-section">
            <button
              type="button"
              className="accordion-section-header"
              onClick={toggleRecentSection}
              aria-expanded={isRecentExpanded}
            >
              <div className="section-header-left">
                {isRecentExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                <span className="section-header-title">Recent</span>
              </div>
              {recentList.length > 0 && (
                <span className="section-count-pill">{recentList.length}</span>
              )}
            </button>

            {isRecentExpanded && (
              <div className="accordion-section-body">
                {recentList.length === 0 ? (
                  <div className="history-empty-hint">No recent chats</div>
                ) : (
                  recentList.slice(0, 15).map(renderConvoItem)
                )}
              </div>
            )}
          </div>
        </div>
      )}
      </div>

      {/* Profile & Account Section at Bottom Left */}
      <div className="sidebar-profile-footer" ref={profileMenuRef}>
        <div
          className={`sidebar-profile-card ${showProfileMenu ? 'menu-open' : ''} ${activeSection === 'profile' ? 'active-profile' : ''}`}
          onClick={() => setShowProfileMenu((prev) => !prev)}
          title={isCollapsed ? `${profileName} (${tenantEmail})` : 'Account settings & theme'}
          role="button"
          tabIndex={0}
          aria-haspopup="menu"
          aria-expanded={showProfileMenu}
        >
          <div className="profile-avatar-wrap">
            <div className="profile-avatar">{initials}</div>
            <span className="profile-online-dot" />
          </div>

          {!isCollapsed && (
            <>
              <div className="profile-meta">
                <span className="profile-name">{profileName}</span>
                <span className="profile-email">{tenantEmail}</span>
              </div>
              <ChevronUp
                className={`profile-chevron ${showProfileMenu ? 'rotate-180' : ''}`}
              />
            </>
          )}
        </div>

        {/* Profile Popover Menu */}
        {showProfileMenu && (
          <div className={`profile-popover-menu ${isCollapsed ? 'popover-collapsed-pos' : ''}`}>
            <div className="popover-header">
              <div className="popover-avatar">{initials}</div>
              <div className="popover-user-info">
                <strong>{profileName}</strong>
                <span>{tenantEmail}</span>
              </div>
            </div>

            <div className="popover-divider" />

            {/* Theme Toggle Inside Popover - Modern Segmented Control */}
            <div className="popover-theme-row">
              <span className="popover-theme-label">Theme</span>
              <div className="theme-toggle-group">
                <button
                  type="button"
                  className={`theme-toggle-btn ${theme === 'dark' ? 'active' : ''}`}
                  onClick={() => setTheme('dark')}
                  title="Obsidian Dark theme"
                >
                  <Moon size={13} className="theme-btn-icon" />
                  <span>Dark</span>
                </button>
                <button
                  type="button"
                  className={`theme-toggle-btn ${theme === 'light' ? 'active' : ''}`}
                  onClick={() => setTheme('light')}
                  title="Studio Light theme"
                >
                  <Sun size={13} className="theme-btn-icon" />
                  <span>Light</span>
                </button>
              </div>
            </div>

            <div className="popover-divider" />

            <button
              type="button"
              className={`popover-item ${activeSection === 'profile' ? 'active' : ''}`}
              onClick={() => handleSelectOption('profile')}
            >
              <User className="popover-icon" />
              <span>Career Profile</span>
            </button>

            <button
              type="button"
              className={`popover-item ${activeSection === 'settings' ? 'active' : ''}`}
              onClick={() => handleSelectOption('settings')}
            >
              <Mail className="popover-icon" />
              <span>Email & Integrations</span>
            </button>

            {isSuperadmin && (
              <button
                type="button"
                className={`popover-item ${activeSection === 'admin' ? 'active' : ''}`}
                onClick={() => handleSelectOption('admin', 'Switched to SuperAdmin Ops Center.')}
              >
                <ShieldCheck className="popover-icon" />
                <span>Superadmin Ops</span>
              </button>
            )}

            <div className="popover-divider" />

            <button
              type="button"
              className="popover-item popover-logout"
              onClick={handleLogoutClick}
            >
              <LogOut className="popover-icon" />
              <span>Sign Out</span>
            </button>
          </div>
        )}
      </div>
    </aside>
  );
}
