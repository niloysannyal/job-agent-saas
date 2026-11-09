import React, { useState } from 'react';
import { AlertCircle, AlertTriangle, Info, CheckCircle2, ChevronUp, ChevronDown, CornerDownRight } from 'lucide-react';

export default function CompilerDiagnosticsDrawer({ diagnostics, onJumpToLine }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!diagnostics) return null;

  const { errors = [], warnings = [], typesetting = [], clean = true } = diagnostics;
  const totalIssues = errors.length + warnings.length + typesetting.length;

  return (
    <div className={`compiler-diagnostics-drawer ${isOpen ? 'is-open' : 'is-collapsed'}`}>
      {/* Top Status Bar Toggle */}
      <div
        className="diagnostics-toggle-bar"
        onClick={() => setIsOpen(!isOpen)}
        title="Toggle Overleaf Compiler Logs & Diagnostics"
      >
        <div className="diagnostics-status-left">
          {clean && totalIssues === 0 ? (
            <div className="status-pill status-clean">
              <CheckCircle2 size={13} className="text-emerald-400" />
              <span>TeX Live Engine: Clean</span>
            </div>
          ) : (
            <div className="status-pills-row">
              {errors.length > 0 && (
                <div className="status-pill status-error">
                  <AlertCircle size={13} />
                  <span>{errors.length} {errors.length === 1 ? 'Error' : 'Errors'}</span>
                </div>
              )}
              {warnings.length > 0 && (
                <div className="status-pill status-warning">
                  <AlertTriangle size={13} />
                  <span>{warnings.length} {warnings.length === 1 ? 'Warning' : 'Warnings'}</span>
                </div>
              )}
              {typesetting.length > 0 && (
                <div className="status-pill status-typesetting">
                  <Info size={13} />
                  <span>{typesetting.length} Layout</span>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="diagnostics-toggle-right">
          <span className="diagnostics-toggle-label">
            {isOpen ? 'Hide Logs & Issues' : totalIssues > 0 ? `Show ${totalIssues} Issues` : 'Compiler Logs'}
          </span>
          {isOpen ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
        </div>
      </div>

      {/* Expanded Logs & Issues List */}
      {isOpen && (
        <div className="diagnostics-panel-body">
          {totalIssues === 0 ? (
            <div className="diagnostics-empty-state">
              <CheckCircle2 size={24} className="text-emerald-500 mb-1" />
              <p className="font-semibold text-sm">No Compilation or Syntax Issues Detected</p>
              <span className="text-xs text-muted">Document syntax is verified against Overleaf LaTeX specifications.</span>
            </div>
          ) : (
            <div className="diagnostics-entries-list">
              {/* Errors First */}
              {errors.map((entry, idx) => (
                <div
                  key={`err-${idx}`}
                  className="diagnostic-entry-card entry-error"
                  onClick={() => entry.line && onJumpToLine?.(entry.line)}
                >
                  <div className="entry-header">
                    <span className="entry-badge badge-error">
                      <AlertCircle size={12} />
                      Error
                    </span>
                    {entry.line && (
                      <span className="entry-line-badge">
                        Line {entry.line}
                      </span>
                    )}
                    {entry.line && onJumpToLine && (
                      <span className="entry-jump-hint">
                        <CornerDownRight size={11} /> Jump to source
                      </span>
                    )}
                  </div>
                  <div className="entry-message">{entry.message}</div>
                  {entry.content && (
                    <pre className="entry-raw-snippet">{entry.content.trim()}</pre>
                  )}
                </div>
              ))}

              {/* Warnings Second */}
              {warnings.map((entry, idx) => (
                <div
                  key={`warn-${idx}`}
                  className="diagnostic-entry-card entry-warning"
                  onClick={() => entry.line && onJumpToLine?.(entry.line)}
                >
                  <div className="entry-header">
                    <span className="entry-badge badge-warning">
                      <AlertTriangle size={12} />
                      Warning
                    </span>
                    {entry.line && (
                      <span className="entry-line-badge">
                        Line {entry.line}
                      </span>
                    )}
                    {entry.line && onJumpToLine && (
                      <span className="entry-jump-hint">
                        <CornerDownRight size={11} /> Jump to source
                      </span>
                    )}
                  </div>
                  <div className="entry-message">{entry.message}</div>
                </div>
              ))}

              {/* Typesetting / Budget Issues */}
              {typesetting.map((entry, idx) => (
                <div
                  key={`type-${idx}`}
                  className="diagnostic-entry-card entry-typesetting"
                  onClick={() => entry.line && onJumpToLine?.(entry.line)}
                >
                  <div className="entry-header">
                    <span className="entry-badge badge-typesetting">
                      <Info size={12} />
                      Typesetting
                    </span>
                    {entry.line && (
                      <span className="entry-line-badge">
                        Line {entry.line}
                      </span>
                    )}
                  </div>
                  <div className="entry-message">{entry.message}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

