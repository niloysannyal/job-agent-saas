import React, { useState, useRef, useEffect } from 'react';
import {
  LayoutDashboard,
  Briefcase,
  FileEdit,
  Kanban,
  GraduationCap,
  Sparkles,
  User,
  FileText,
  Sliders,
  LogOut,
  ChevronUp,
  Users,
  ShieldCheck,
  Search,
  Moon,
  Sun,
  Laptop,
} from 'lucide-react';

export default function Sidebar({
  activeSection,
  setActiveSection,
  profileName = 'Niloy Sannyal',
  tenantEmail = 'niloy@example.com',
  isSuperadmin = true,
  onLogout,
  showToast,
  theme = 'dark',
  setTheme,
  toggleTheme,
  onOpenCommandPalette,
}) {
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

  if (isSuperadmin) {
    navItems.push({
      id: 'admin',
      label: 'Admin Control Center',
      icon: ShieldCheck,
      badge: 'Ops',
      shortcut: 'Alt+0',
    });
  }

  navItems.push(
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
    <aside className="app-sidebar" aria-label="Sidebar Navigation">
      {/* Top Header Group */}
      <div className="sidebar-top-group">
        {/* Brand Header */}
        <div className="sidebar-brand">
          <div className="brand-icon-box">
            <Sparkles className="icon-sparkles" />
          </div>
          <div className="brand-meta">
            <h1 className="brand-title">JobEazy</h1>
            <span className="brand-account">Autonomous Job Agent</span>
          </div>
        </div>

        {/* Global Command Palette Launcher Button (Linear / Raycast Style) */}
        <button
          className="sidebar-quick-search-btn"
          onClick={onOpenCommandPalette}
          title="Search views, opportunities and actions (Ctrl+K)"
          aria-label="Open command palette"
        >
          <Search className="quick-search-icon" />
          <span className="quick-search-label">Quick Search...</span>
          <kbd className="quick-search-kbd">⌘K</kbd>
        </button>
      </div>

      {/* Nav Menu */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeSection === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveSection(item.id)}
              className={`nav-item-btn ${isActive ? 'active' : ''}`}
              id={`nav-btn-${item.id}`}
            >
              <div className="nav-item-left">
                <Icon className="nav-icon" />
                <span className="nav-label">{item.label}</span>
              </div>
              <span className="nav-shortcut-hint">{item.shortcut}</span>
            </button>
          );
        })}
      </nav>

      {/* Profile & Account Section at Bottom Left */}
      <div className="sidebar-profile-footer" ref={profileMenuRef}>
        {/* Popover Menu */}
        {showProfileMenu && (
          <div className="profile-popover-menu animate-fadeIn">
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
              <span>Profile & Grounding</span>
            </button>

            <button
              className="popover-item"
              onClick={() => handleSelectOption('profile', 'Opened Master LaTeX CV')}
            >
              <FileText className="popover-icon" />
              <span>Master CV & LaTeX</span>
            </button>

            <button
              className="popover-item"
              onClick={() => handleSelectOption('profile', 'Opened Career Preferences')}
            >
              <Sliders className="popover-icon" />
              <span>Grounding & Tone</span>
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
          }`}
          onClick={() => setShowProfileMenu((prev) => !prev)}
          title="Account settings & theme"
          aria-haspopup="true"
          aria-expanded={showProfileMenu}
        >
          <div className="profile-avatar-wrap">
            <div className="profile-avatar">{initials}</div>
            <span className="profile-online-dot" />
          </div>

          <div className="profile-meta-text">
            <strong className="profile-name">{profileName}</strong>
            <span className="profile-email">{tenantEmail}</span>
          </div>

          <ChevronUp className={`profile-chevron ${showProfileMenu ? 'rotate-180' : ''}`} />
        </button>
      </div>
    </aside>
  );
}
