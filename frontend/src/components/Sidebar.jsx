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
  Search,
  Moon,
  Sun,
  Laptop,
  PanelLeftClose,
  PanelLeftOpen,
  Plus,
  MessageSquare,
  Trash2,
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
}) {
  const {
    conversations = [],
    activeConversationId,
    selectConversation,
    deleteConversation,
    resetConversation,
    proposalsCount = 0,
  } = useAgent();

  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef(null);

  // Close profile menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setShowProfileMenu(false);
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
        shortcut: 'Alt+1',
        isAdminTab: true,
      },
      {
        id: 'tenants',
        label: 'Tenants & Workspaces',
        icon: Users,
        shortcut: 'Alt+2',
        isAdminTab: true,
      },
      {
        id: 'providers',
        label: 'Dynamic LLM Providers',
        icon: Server,
        shortcut: 'Alt+3',
        isAdminTab: true,
      },
      {
        id: 'sources',
        label: 'Job Sources & Feeds',
        icon: Layers,
        shortcut: 'Alt+4',
        isAdminTab: true,
      },
      {
        id: 'templates',
        label: 'Curated LaTeX Templates',
        icon: FileCode,
        shortcut: 'Alt+5',
        isAdminTab: true,
      },
      {
        id: 'flagged',
        label: 'Posting Guard Flags',
        icon: ShieldAlert,
        shortcut: 'Alt+6',
        isAdminTab: true,
      },
    );
  } else {
    navItems.push(
      {
        id: 'copilot',
        label: 'Career Copilot',
        icon: Bot,
        shortcut: '⌘J',
        badge: proposalsCount > 0 ? `${proposalsCount}` : null,
      },
      {
        id: 'dashboard',
        label: 'Dashboard',
        icon: LayoutDashboard,
        shortcut: 'Alt+1',
      },
      {
        id: 'jobs',
        label: 'Jobs & Radar',
        icon: Briefcase,
        shortcut: 'Alt+2',
      },
      {
        id: 'studio',
        label: 'Application Studio',
        icon: FileEdit,
        shortcut: 'Alt+3',
      },
      {
        id: 'pipeline',
        label: 'Application Pipeline',
        icon: Kanban,
        shortcut: 'Alt+4',
      },
      {
        id: 'interview',
        label: 'STAR Interview Coach',
        icon: GraduationCap,
        shortcut: 'Alt+5',
      },
    );
  }

  // Derive user initials (e.g., "NS" for Niloy Sannyal)
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

  return (
    <aside
      className={`app-sidebar ${isCollapsed ? 'sidebar-collapsed' : ''}`}
      aria-label="Sidebar Navigation"
    >
      {/* Top Header Group */}
      <div className="sidebar-top-group">
        {/* Brand Header Row */}
        <div className="sidebar-brand-row">
          <div
            className="sidebar-brand"
            onClick={isCollapsed ? onToggleCollapse : undefined}
            style={{ cursor: isCollapsed ? 'pointer' : 'default' }}
            title={isCollapsed ? 'JobEazy — Click to expand sidebar (⌘\\)' : undefined}
          >
            <div className="brand-icon-box">
              <Sparkles className="icon-sparkles" />
            </div>
            {!isCollapsed && (
              <div className="brand-meta">
                <h1 className="brand-title">JobEazy</h1>
                <span className={`brand-account ${isSuperadmin && !isImpersonating ? 'text-emerald' : ''}`}>
                  {isSuperadmin && !isImpersonating ? 'SuperAdmin Ops Plane' : 'Autonomous Job Agent'}
                </span>
              </div>
            )}
          </div>

          {/* Sidebar Collapse/Expand Toggle Button */}
          {onToggleCollapse && (
            <button
              type="button"
              className="sidebar-collapse-toggle-btn"
              onClick={onToggleCollapse}
              title={isCollapsed ? 'Expand sidebar (⌘\\)' : 'Collapse sidebar (⌘\\)'}
              aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              {isCollapsed ? <PanelLeftOpen size={16} /> : <PanelLeftClose size={16} />}
            </button>
          )}
        </div>

        {/* Global Command Palette Launcher Button (Linear / Raycast Style) */}
        <button
          className={`sidebar-quick-search-btn ${isCollapsed ? 'btn-collapsed' : ''}`}
          onClick={onOpenCommandPalette}
          title={isCollapsed ? 'Quick Search (⌘K)' : 'Search views, opportunities and actions (Ctrl+K)'}
          aria-label="Open command palette"
        >
          <Search className="quick-search-icon" />
          {!isCollapsed && (
            <>
              <span className="quick-search-label">Quick Search...</span>
              <kbd className="quick-search-kbd">⌘K</kbd>
            </>
          )}
        </button>
      </div>

      {/* Nav Menu */}
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
              title={isCollapsed ? `${item.label} (${item.shortcut})` : undefined}
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
              {!isCollapsed && <span className="nav-shortcut-hint">{item.shortcut}</span>}
            </button>
          );
        })}
      </nav>

      {/* Recent Chats / History Section (Candidate Mode) */}
      {!isSuperadmin && !isCollapsed && (
        <div className="sidebar-history-group">
          <div className="history-group-header">
            <span className="history-group-title">Recent Chats</span>
            <button
              type="button"
              className="btn-new-chat-mini"
              onClick={() => {
                resetConversation();
                setActiveSection('copilot');
              }}
              title="Start fresh new chat session (⌘J)"
            >
              <Plus size={13} />
              <span>New</span>
            </button>
          </div>

          <div className="history-items-list">
            {conversations.length === 0 ? (
              <div className="history-empty-hint">
                <span>No saved chats yet</span>
              </div>
            ) : (
              conversations.slice(0, 15).map((convo) => {
                const isSelected = activeSection === 'copilot' && activeConversationId === convo.id;
                return (
                  <div
                    key={convo.id}
                    className={`history-chat-item ${isSelected ? 'active' : ''}`}
                    onClick={() => {
                      selectConversation(convo.id);
                      setActiveSection('copilot');
                    }}
                    title={convo.title || 'Career Session'}
                  >
                    <MessageSquare size={13} className="history-chat-icon" />
                    <span className="history-chat-title">{convo.title || 'Career Session'}</span>
                    <button
                      type="button"
                      className="history-delete-btn"
                      onClick={(e) => deleteConversation(convo.id, e)}
                      title="Delete chat session"
                      aria-label="Delete chat"
                    >
                      <Trash2 size={12} />
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}

      {/* Collapsed New Chat Quick Action */}
      {!isSuperadmin && isCollapsed && (
        <div className="sidebar-collapsed-history-action">
          <button
            type="button"
            className="collapsed-new-chat-btn"
            onClick={() => {
              resetConversation();
              setActiveSection('copilot');
            }}
            title="Start new chat session (⌘J)"
            aria-label="New Chat"
          >
            <Plus size={16} />
          </button>
        </div>
      )}

      {/* Profile & Account Section at Bottom Left */}
      <div className="sidebar-profile-footer" ref={profileMenuRef}>
        {/* Popover Menu */}
        {showProfileMenu && (
          <div className={`profile-popover-menu animate-fadeIn ${isCollapsed ? 'popover-collapsed-anchor' : ''}`}>
            <div className="popover-user-header">
              <div className="popover-avatar">{initials}</div>
              <div className="popover-user-info">
                <strong>{profileName}</strong>
                <span>{tenantEmail}</span>
              </div>
            </div>

            <div className="popover-divider" />

            {/* Theme Selector Segmented Control */}
            <div className="popover-theme-row">
              <span className="popover-theme-label">Theme</span>
              <div className="theme-toggle-group" role="radiogroup" aria-label="Theme selection">
                <button
                  className={`theme-toggle-btn ${theme === 'dark' ? 'active' : ''}`}
                  onClick={() => setTheme && setTheme('dark')}
                  title="Obsidian Dark Mode"
                  aria-checked={theme === 'dark'}
                  role="radio"
                >
                  <Moon className="theme-icon" />
                  <span>Dark</span>
                </button>
                <button
                  className={`theme-toggle-btn ${theme === 'light' ? 'active' : ''}`}
                  onClick={() => setTheme && setTheme('light')}
                  title="Studio Light Mode"
                  aria-checked={theme === 'light'}
                  role="radio"
                >
                  <Sun className="theme-icon" />
                  <span>Light</span>
                </button>
                <button
                  className={`theme-toggle-btn ${theme === 'system' ? 'active' : ''}`}
                  onClick={() => setTheme && setTheme('system')}
                  title="Match System OS"
                  aria-checked={theme === 'system'}
                  role="radio"
                >
                  <Laptop className="theme-icon" />
                  <span>Auto</span>
                </button>
              </div>
            </div>

            <div className="popover-divider" />

            <button
              className={`popover-item ${activeSection === 'profile' ? 'active' : ''}`}
              onClick={() => handleSelectOption('profile')}
            >
              <User className="popover-icon" />
              <span>Profile</span>
            </button>

            <div className="popover-divider" />

            {isSuperadmin && (
              <>
                <button
                  className={`popover-item popover-admin-btn ${activeSection === 'admin' ? 'active' : ''}`}
                  onClick={() => handleSelectOption('admin', 'Switched to Superadmin Control Center')}
                >
                  <ShieldCheck className="popover-icon text-emerald-500" />
                  <span>Admin Control Center</span>
                  <span className="popover-badge-superadmin">OPS</span>
                </button>
                <div className="popover-divider" />
              </>
            )}

            <button
              className="popover-item popover-logout"
              onClick={handleLogoutClick}
            >
              <LogOut className="popover-icon" />
              <span>Sign Out</span>
            </button>
          </div>
        )}

        {/* Profile Card Button */}
        <button
          className={`sidebar-profile-card ${showProfileMenu ? 'menu-open' : ''} ${
            activeSection === 'profile' ? 'active-profile' : ''
          } ${isCollapsed ? 'profile-collapsed' : ''}`}
          onClick={() => setShowProfileMenu((prev) => !prev)}
          title={isCollapsed ? `${profileName} (${tenantEmail})` : 'Account settings & theme'}
          aria-haspopup="true"
          aria-expanded={showProfileMenu}
        >
          <div className="profile-avatar-wrap">
            <div className="profile-avatar">{initials}</div>
            <span className="profile-online-dot" />
          </div>

          {!isCollapsed && (
            <>
              <div className="profile-meta-text">
                <strong className="profile-name">{profileName}</strong>
                <span className="profile-email">{tenantEmail}</span>
              </div>
              <ChevronUp className={`profile-chevron ${showProfileMenu ? 'rotate-180' : ''}`} />
            </>
          )}
        </button>
      </div>
    </aside>
  );
}
