import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  Search,
  LayoutDashboard,
  Briefcase,
  FileEdit,
  Kanban,
  GraduationCap,
  User,
  ShieldCheck,
  Moon,
  Sun,
  Laptop,
  Sparkles,
  ArrowRight,
  ExternalLink,
  Building2,
  X,
  Command,
} from 'lucide-react';

export default function CommandPalette({
  isOpen,
  onClose,
  activeSection,
  onNavigate,
  theme,
  setTheme,
  jobs = [],
  onSelectJobForStudio,
  showToast,
}) {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);
  const listRef = useRef(null);

  // Auto-focus input on open and reset state
  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => {
        if (inputRef.current) inputRef.current.focus();
      }, 50);
    }
  }, [isOpen]);

  // Command items definitions
  const commands = useMemo(() => {
    const list = [
      // Navigation
      {
        id: 'nav-dashboard',
        category: 'Navigation',
        label: 'Go to Dashboard',
        icon: LayoutDashboard,
        shortcut: 'Alt+1',
        action: () => {
          onNavigate('dashboard');
          onClose();
        },
      },
      {
        id: 'nav-jobs',
        category: 'Navigation',
        label: 'Go to Jobs & Radar',
        icon: Briefcase,
        shortcut: 'Alt+2',
        action: () => {
          onNavigate('jobs');
          onClose();
        },
      },
      {
        id: 'nav-studio',
        category: 'Navigation',
        label: 'Go to Application Studio',
        icon: FileEdit,
        shortcut: 'Alt+3',
        action: () => {
          onNavigate('studio');
          onClose();
        },
      },
      {
        id: 'nav-pipeline',
        category: 'Navigation',
        label: 'Go to Application Pipeline',
        icon: Kanban,
        shortcut: 'Alt+4',
        action: () => {
          onNavigate('pipeline');
          onClose();
        },
      },
      {
        id: 'nav-interview',
        category: 'Navigation',
        label: 'Go to STAR Interview Coach',
        icon: GraduationCap,
        shortcut: 'Alt+5',
        action: () => {
          onNavigate('interview');
          onClose();
        },
      },
      {
        id: 'nav-profile',
        category: 'Navigation',
        label: 'Go to Profile & Master CV',
        icon: User,
        shortcut: 'Alt+6',
        action: () => {
          onNavigate('profile');
          onClose();
        },
      },
      // Theme options
      {
        id: 'theme-dark',
        category: 'Appearance',
        label: 'Switch to Obsidian Dark Mode',
        icon: Moon,
        current: theme === 'dark',
        action: () => {
          setTheme('dark');
          if (showToast) showToast('Switched to Obsidian Dark theme');
          onClose();
        },
      },
      {
        id: 'theme-light',
        category: 'Appearance',
        label: 'Switch to Studio Light Mode',
        icon: Sun,
        current: theme === 'light',
        action: () => {
          setTheme('light');
          if (showToast) showToast('Switched to Studio Light theme');
          onClose();
        },
      },
      {
        id: 'theme-system',
        category: 'Appearance',
        label: 'Match System OS Theme',
        icon: Laptop,
        current: theme === 'system',
        action: () => {
          setTheme('system');
          if (showToast) showToast('Theme set to Match System');
          onClose();
        },
      },
      // Quick Actions
      {
        id: 'act-ingest',
        category: 'Actions',
        label: 'Ingest Job Feeds (Remotive, Adzuna, RemoteOK)',
        icon: Sparkles,
        action: () => {
          onNavigate('jobs');
          onClose();
        },
      },
    ];

    // Add matching jobs from the current radar
    if (jobs && jobs.length > 0) {
      jobs.slice(0, 15).forEach((job) => {
        const title = job.title || job.role || 'Job Opportunity';
        const company = job.company || 'Company';
        list.push({
          id: `job-${job.id}`,
          category: 'Opportunities',
          label: `${title} at ${company}`,
          sublabel: `Match: ${job.match_score ?? 'N/A'}% | ${job.location || 'Remote'}`,
          icon: Building2,
          action: () => {
            if (onSelectJobForStudio) {
              onSelectJobForStudio(job);
            } else {
              onNavigate('studio');
            }
            onClose();
          },
        });
      });
    }

    return list;
  }, [theme, jobs, onNavigate, onClose, setTheme, onSelectJobForStudio, showToast]);

  // Filter commands by search query
  const filteredCommands = useMemo(() => {
    if (!query.trim()) return commands;
    const q = query.toLowerCase();
    return commands.filter(
      (cmd) =>
        cmd.label.toLowerCase().includes(q) ||
        (cmd.sublabel && cmd.sublabel.toLowerCase().includes(q)) ||
        cmd.category.toLowerCase().includes(q)
    );
  }, [commands, query]);

  // Keep selected index within bounds
  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  // Keyboard navigation
  const handleKeyDown = (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev < filteredCommands.length - 1 ? prev + 1 : 0));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : filteredCommands.length - 1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredCommands[selectedIndex]) {
        filteredCommands[selectedIndex].action();
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      onClose();
    }
  };

  // Scroll active item into view
  useEffect(() => {
    if (listRef.current) {
      const activeEl = listRef.current.querySelector('.cmd-item.selected');
      if (activeEl) {
        activeEl.scrollIntoView({ block: 'nearest' });
      }
    }
  }, [selectedIndex]);

  if (!isOpen) return null;

  return (
    <div className="cmd-palette-backdrop" onClick={onClose} role="dialog" aria-modal="true">
      <div
        className="cmd-palette-modal animate-modalIn"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        {/* Search Input Bar */}
        <div className="cmd-input-bar">
          <Search className="cmd-search-icon" />
          <input
            ref={inputRef}
            type="text"
            className="cmd-input"
            placeholder="Type a command, job title, or search views..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <span className="cmd-esc-chip" onClick={onClose}>
            ESC
          </span>
        </div>

        {/* Results List */}
        <div className="cmd-list-wrap" ref={listRef}>
          {filteredCommands.length === 0 ? (
            <div className="cmd-empty-state">
              <Command className="cmd-empty-icon" />
              <p>No matching commands or opportunities found for &quot;{query}&quot;</p>
            </div>
          ) : (
            filteredCommands.map((cmd, idx) => {
              const Icon = cmd.icon;
              const isSelected = idx === selectedIndex;
              return (
                <div
                  key={cmd.id}
                  className={`cmd-item ${isSelected ? 'selected' : ''}`}
                  onClick={cmd.action}
                  onMouseEnter={() => setSelectedIndex(idx)}
                >
                  <div className="cmd-item-left">
                    <div className="cmd-icon-box">
                      <Icon className="cmd-icon" />
                    </div>
                    <div className="cmd-text-block">
                      <div className="cmd-label-row">
                        <span className="cmd-label">{cmd.label}</span>
                        {cmd.current && <span className="cmd-badge-active">Active</span>}
                      </div>
                      {cmd.sublabel && <span className="cmd-sublabel">{cmd.sublabel}</span>}
                    </div>
                  </div>

                  <div className="cmd-item-right">
                    <span className="cmd-category-tag">{cmd.category}</span>
                    {cmd.shortcut && <kbd className="cmd-kbd">{cmd.shortcut}</kbd>}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer Navigation Hints */}
        <div className="cmd-footer-hints">
          <div className="cmd-hint">
            <kbd className="cmd-mini-kbd">↑</kbd>
            <kbd className="cmd-mini-kbd">↓</kbd>
            <span>Navigate</span>
          </div>
          <div className="cmd-hint">
            <kbd className="cmd-mini-kbd">↵</kbd>
            <span>Select</span>
          </div>
          <div className="cmd-hint">
            <kbd className="cmd-mini-kbd">ESC</kbd>
            <span>Dismiss</span>
          </div>
        </div>
      </div>
    </div>
  );
}

