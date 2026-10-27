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
} from 'lucide-react';

export default function Sidebar({
  activeSection,
  setActiveSection,
  profileName = 'Niloy Sannyal',
  tenantEmail = 'niloy@example.com',
  onLogout,
  showToast,
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

  const navItems = [
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
  ];

  // Derive user initials (e.g., "NS" for Niloy Sannyal)
  const initials = profileName
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

      {/* Nav Menu (Clean, No badge counters, Profile moved to bottom) */}
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

            <button
              className="popover-item"
              onClick={() => handleSelectOption(null, 'Switching accounts (Multi-tenant mode ready)')}
            >
              <Users className="popover-icon" />
              <span>Switch Account</span>
            </button>

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
          title="Account settings & profile"
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
