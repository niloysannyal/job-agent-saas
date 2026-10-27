import React from 'react';
import {
  LayoutDashboard,
  User,
  Briefcase,
  FileEdit,
  Kanban,
  GraduationCap,
  Sparkles,
  ShieldCheck,
} from 'lucide-react';

export default function Sidebar({
  activeSection,
  setActiveSection,
  counts = {},
  profileName = 'Niloy Sannyal',
  tenantEmail = 'niloy@example.com',
}) {
  const navItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard,
      badge: null,
    },
    {
      id: 'profile',
      label: 'Profile & Grounding',
      icon: User,
      badge: counts.designations ? `${counts.designations} Roles` : null,
    },
    {
      id: 'jobs',
      label: 'Jobs & Radar',
      icon: Briefcase,
      badge: counts.jobs != null ? String(counts.jobs) : null,
    },
    {
      id: 'studio',
      label: 'Application Studio',
      icon: FileEdit,
      badge: counts.tailoredDrafts ? `${counts.tailoredDrafts} Draft` : null,
    },
    {
      id: 'pipeline',
      label: 'Application Pipeline',
      icon: Kanban,
      badge: counts.pipeline != null ? String(counts.pipeline) : null,
      alertBadge: counts.followUpsDue > 0 ? `${counts.followUpsDue} Due` : null,
    },
    {
      id: 'interview',
      label: 'STAR Interview Coach',
      icon: GraduationCap,
      badge: counts.stories ? `${counts.stories} Stories` : null,
    },
  ];

  return (
    <aside className="app-sidebar" aria-label="Sidebar Navigation">
      {/* Brand Header */}
      <div className="sidebar-brand">
        <div className="brand-icon-box">
          <Sparkles className="icon-sparkles" />
        </div>
        <div className="brand-meta">
          <h1 className="brand-title">AI Career OS</h1>
          <span className="brand-account">{profileName}</span>
        </div>
      </div>

      {/* Tenant Pill */}
      <div className="sidebar-tenant-badge">
        <span className="tenant-status-dot"></span>
        <span className="tenant-email">{tenantEmail}</span>
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
              <div className="nav-item-badges">
                {item.alertBadge && (
                  <span className="badge-alert" title={`${item.alertBadge} follow-ups scheduled`}>
                    ⏰ {item.alertBadge}
                  </span>
                )}
                {item.badge && !item.alertBadge && (
                  <span className="badge-counter">{item.badge}</span>
                )}
              </div>
            </button>
          );
        })}
      </nav>

      {/* System Status Footer */}
      <div className="sidebar-footer">
        <div className="engine-indicator">
          <div className="indicator-dot"></div>
          <div className="indicator-text">
            <strong>OpenAI Embeddings</strong>
            <span>text-embedding-3-small</span>
          </div>
        </div>
        <div className="human-gate-tag">
          <ShieldCheck className="gate-icon" />
          <span>Strict Human-in-the-Loop Gate</span>
        </div>
      </div>
    </aside>
  );
}
