import React, { useMemo, useRef, useImperativeHandle, forwardRef, useCallback, useState, useEffect } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { StreamLanguage } from '@codemirror/language';
import { stex } from '@codemirror/legacy-modes/mode/stex';
import { EditorView, keymap } from '@codemirror/view';
import { closeBrackets } from '@codemirror/autocomplete';
import { bracketMatching } from '@codemirror/language';
import { FileCode, Bold, List, Hash, Link as LinkIcon, Sparkles } from 'lucide-react';

const stexLanguage = StreamLanguage.define(stex);

// Obsidian Dark Theme for CodeMirror 6
const obsidianDarkTheme = EditorView.theme(
  {
    '&': {
      backgroundColor: '#0b0f17',
      color: '#e2e8f0',
      fontSize: '13px',
      fontFamily: 'JetBrains Mono, Fira Code, Menlo, Monaco, Consolas, monospace',
      height: '100%',
    },
    '.cm-scroller': {
      fontFamily: 'inherit',
      lineHeight: '1.6',
      overflow: 'auto',
    },
    '.cm-content': {
      padding: '16px 0',
      caretColor: '#10b981',
    },
    '.cm-cursor': {
      borderLeftColor: '#10b981',
      borderLeftWidth: '2px',
    },
    '&.cm-focused .cm-cursor': {
      borderLeftColor: '#34d399',
    },
    '.cm-gutters': {
      backgroundColor: '#080c14',
      color: '#475569',
      borderRight: '1px solid rgba(255, 255, 255, 0.08)',
      paddingRight: '6px',
    },
    '.cm-activeLineGutter': {
      backgroundColor: 'rgba(16, 185, 129, 0.12)',
      color: '#34d399',
      fontWeight: '600',
    },
    '.cm-activeLine': {
      backgroundColor: 'rgba(255, 255, 255, 0.03)',
    },
    '.cm-selectionMatch': {
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
    },
    '&.cm-focused .cm-selectionBackground, .cm-selectionBackground': {
      backgroundColor: 'rgba(16, 185, 129, 0.3) !important',
    },
    '.cm-matchingBracket': {
      backgroundColor: 'rgba(16, 185, 129, 0.3)',
      color: '#6ee7b7 !important',
      outline: '1px solid #10b981',
    },
    '.cm-nonmatchingBracket': {
      backgroundColor: 'rgba(239, 68, 68, 0.3)',
      color: '#f87171 !important',
    },
    // Syntax highlight classes from stex mode
    '.cm-keyword': { color: '#ec4899', fontWeight: '600' }, // \begin, \end, \section
    '.cm-atom': { color: '#8b5cf6' },
    '.cm-number': { color: '#f59e0b' },
    '.cm-def': { color: '#38bdf8' },
    '.cm-variable': { color: '#e2e8f0' },
    '.cm-variable-2': { color: '#10b981' }, // arguments
    '.cm-string': { color: '#34d399' },
    '.cm-comment': { color: '#64748b', fontStyle: 'italic' }, // % comments
    '.cm-tag': { color: '#f43f5e' },
    '.cm-bracket': { color: '#94a3b8' },
  },
  { dark: true }
);

// Cyber Light Theme for CodeMirror 6
const cyberLightTheme = EditorView.theme(
  {
    '&': {
      backgroundColor: '#ffffff',
      color: '#1e293b',
      fontSize: '13px',
      fontFamily: 'JetBrains Mono, Fira Code, Menlo, Monaco, Consolas, monospace',
      height: '100%',
    },
    '.cm-scroller': {
      fontFamily: 'inherit',
      lineHeight: '1.6',
      overflow: 'auto',
    },
    '.cm-content': {
      padding: '16px 0',
      caretColor: '#059669',
    },
    '.cm-cursor': {
      borderLeftColor: '#059669',
      borderLeftWidth: '2px',
    },
    '&.cm-focused .cm-cursor': {
      borderLeftColor: '#059669',
    },
    '.cm-gutters': {
      backgroundColor: '#f8fafc',
      color: '#94a3b8',
      borderRight: '1px solid #e2e8f0',
      paddingRight: '6px',
    },
    '.cm-activeLineGutter': {
      backgroundColor: '#ecfdf5',
      color: '#059669',
      fontWeight: '600',
    },
    '.cm-activeLine': {
      backgroundColor: '#f1f5f9',
    },
    '.cm-selectionMatch': {
      backgroundColor: 'rgba(16, 185, 129, 0.15)',
    },
    '&.cm-focused .cm-selectionBackground, .cm-selectionBackground': {
      backgroundColor: 'rgba(16, 185, 129, 0.22) !important',
    },
    '.cm-matchingBracket': {
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
      color: '#047857 !important',
      outline: '1px solid #059669',
    },
    // Syntax highlight classes
    '.cm-keyword': { color: '#be185d', fontWeight: '600' },
    '.cm-atom': { color: '#7c3aed' },
    '.cm-number': { color: '#d97706' },
    '.cm-def': { color: '#0284c7' },
    '.cm-variable': { color: '#334155' },
    '.cm-variable-2': { color: '#059669' },
    '.cm-string': { color: '#059669' },
    '.cm-comment': { color: '#94a3b8', fontStyle: 'italic' },
    '.cm-tag': { color: '#e11d48' },
    '.cm-bracket': { color: '#64748b' },
  },
  { dark: false }
);

const LatexCodeEditor = forwardRef(function LatexCodeEditor(
  {
    value,
    onChange,
    onCompile,
    themeMode = 'auto',
    readOnly = false,
    placeholder = '% Enter Overleaf LaTeX source code...',
    extraActions = null,
    hideSubtoolbar = false,
    filename = 'main.tex',
  },
  ref
) {
  const editorViewRef = useRef(null);

  // Dynamic theme detection (auto-syncs with html[data-theme] in real-time)
  const [resolvedTheme, setResolvedTheme] = useState(() => {
    if (themeMode && themeMode !== 'auto') return themeMode;
    if (typeof document !== 'undefined') {
      return document.documentElement.getAttribute('data-theme') || 'dark';
    }
    return 'dark';
  });

  useEffect(() => {
    if (themeMode && themeMode !== 'auto') {
      setResolvedTheme(themeMode);
      return;
    }
    if (typeof MutationObserver === 'undefined') return;
    const observer = new MutationObserver(() => {
      const active = document.documentElement.getAttribute('data-theme') || 'dark';
      setResolvedTheme(active);
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => observer.disconnect();
  }, [themeMode]);

  const activeTheme = resolvedTheme === 'light' ? 'light' : 'dark';

  // Expose imperative API for jump-to-line navigation
  useImperativeHandle(ref, () => ({
    jumpToLine: (lineNum) => {
      const view = editorViewRef.current?.view;
      if (!view) return;

      const doc = view.state.doc;
      const targetLine = Math.min(Math.max(1, lineNum), doc.lines);
      const linePos = doc.line(targetLine);

      view.dispatch({
        selection: { anchor: linePos.from, head: linePos.to },
        scrollIntoView: true,
      });
      view.focus();
    },
    insertText: (text) => {
      const view = editorViewRef.current?.view;
      if (!view) return;

      const { state } = view;
      const range = state.selection.main;
      view.dispatch({
        changes: { from: range.from, to: range.to, insert: text },
        selection: { anchor: range.from + text.length },
      });
      view.focus();
    },
    wrapSelection: (prefix, suffix) => {
      const view = editorViewRef.current?.view;
      if (!view) return;

      const { state } = view;
      const range = state.selection.main;
      const selected = state.sliceDoc(range.from, range.to);
      const replacement = `${prefix}${selected}${suffix}`;

      view.dispatch({
        changes: { from: range.from, to: range.to, insert: replacement },
        selection: {
          anchor: range.from + prefix.length,
          head: range.from + prefix.length + selected.length,
        },
      });
      view.focus();
    },
    focus: () => {
      editorViewRef.current?.view?.focus();
    },
  }));

  // Quick insertion helpers
  const handleWrapBold = useCallback(() => {
    const view = editorViewRef.current?.view;
    if (!view) return;
    const { state } = view;
    const range = state.selection.main;
    const selected = state.sliceDoc(range.from, range.to);
    view.dispatch({
      changes: { from: range.from, to: range.to, insert: `\\textbf{${selected}}` },
      selection: {
        anchor: range.from + 8,
        head: range.from + 8 + selected.length,
      },
    });
    view.focus();
  }, []);

  const handleInsertBullet = useCallback(() => {
    const view = editorViewRef.current?.view;
    if (!view) return;
    const { state } = view;
    const range = state.selection.main;
    view.dispatch({
      changes: { from: range.from, to: range.to, insert: '\n  \\item ' },
      selection: { anchor: range.from + 9 },
    });
    view.focus();
  }, []);

  const handleInsertSection = useCallback(() => {
    const view = editorViewRef.current?.view;
    if (!view) return;
    const { state } = view;
    const range = state.selection.main;
    const text = '\n\\section{NEW SECTION}\n';
    view.dispatch({
      changes: { from: range.from, to: range.to, insert: text },
      selection: { anchor: range.from + 10, head: range.from + 21 },
    });
    view.focus();
  }, []);

  // Keyboard shortcut: Mod-Enter to compile
  const extensions = useMemo(() => {
    const baseExtensions = [
      stexLanguage,
      EditorView.lineWrapping,
      bracketMatching(),
      closeBrackets(),
      activeTheme === 'light' ? cyberLightTheme : obsidianDarkTheme,
    ];

    if (onCompile) {
      baseExtensions.push(
        keymap.of([
          {
            key: 'Mod-Enter',
            run: () => {
              onCompile();
              return true;
            },
          },
        ])
      );
    }

    return baseExtensions;
  }, [activeTheme, onCompile]);

  // Document stats
  const lineCount = (value || '').split(/\r?\n/).length;
  const wordCount = (value || '').trim().split(/\s+/).filter(Boolean).length;

  return (
    <div className={`latex-code-editor-container theme-${activeTheme}`}>
      {/* Editor Sub-Header Toolbar */}
      {!hideSubtoolbar && (
        <div className="editor-subtoolbar">
          <div className="editor-file-info">
            <FileCode size={14} className="text-emerald-400" />
            <span className="editor-filename">{filename}</span>
            <span className="editor-stat-pill">{lineCount} lines</span>
            <span className="editor-stat-pill">{wordCount} words</span>
          </div>

          <div className="editor-action-tools">
            <button
              type="button"
              className="editor-tool-btn"
              onClick={handleWrapBold}
              title="Bold: \textbf{...}"
            >
              <Bold size={13} />
            </button>
            <button
              type="button"
              className="editor-tool-btn"
              onClick={handleInsertBullet}
              title="Bullet Item: \item"
            >
              <List size={13} />
            </button>
            <button
              type="button"
              className="editor-tool-btn"
              onClick={handleInsertSection}
              title="New Section: \section{...}"
            >
              <Hash size={13} />
            </button>

            {extraActions}
          </div>
        </div>
      )}

      {/* CodeMirror 6 Active Workspace */}
      <div className="codemirror-wrapper">
        <CodeMirror
          ref={editorViewRef}
          value={value}
          onChange={onChange}
          extensions={extensions}
          readOnly={readOnly}
          placeholder={placeholder}
          height="100%"
          basicSetup={{
            lineNumbers: true,
            highlightActiveLineGutter: true,
            highlightActiveLine: true,
            foldGutter: true,
            searchKeymap: true,
            autocompletion: true,
            bracketMatching: true,
            closeBrackets: true,
          }}
        />
      </div>
    </div>
  );
});

export default LatexCodeEditor;

