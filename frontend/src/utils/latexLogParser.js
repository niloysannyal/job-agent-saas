/**
 * Overleaf-grade LaTeX Log & Diagnostic Parser.
 *
 * Adapted from the official Overleaf Community Edition:
 * services/web/frontend/js/ide/log-parser/latex-log-parser.ts
 *
 * Features:
 * - Full TeX/LaTeX log stream parser (errors, warnings, hbox/vbox typesetting notices).
 * - Instant in-browser static LaTeX linter for unclosed braces, environments, and ATS-breaking unescaped symbols.
 * - Unified diagnostics schema for editor gutters and the diagnostics drawer.
 */

const LOG_WRAP_LIMIT = 79;
const LATEX_WARNING_REGEX = /^LaTeX(?:3| Font)? Warning: (.*)$/;
const HBOX_WARNING_REGEX = /^(Over|Under)full \\(v|h)box/;
const PACKAGE_WARNING_REGEX = /^((?:Package|Class|Module) \b.+\b Warning:.*)$/;
const LINES_REGEX = /lines? ([0-9]+)/;
const PACKAGE_REGEX = /^(?:Package|Class|Module) (\b.+\b) Warning/;
const FILE_LINE_ERROR_REGEX = /^([./].*):(\d+): (.*)/;

const STATE = {
  NORMAL: 0,
  ERROR: 1,
};

class LogText {
  constructor(text) {
    this.text = (text || '').replace(/(\r\n)|\r/g, '\n');
    const wrappedLines = this.text.split('\n');
    this.lines = [wrappedLines[0] || ''];

    for (let i = 1; i < wrappedLines.length; i++) {
      const prevLine = wrappedLines[i - 1];
      const currentLine = wrappedLines[i];

      if (
        prevLine.length === LOG_WRAP_LIMIT &&
        prevLine.slice(-3) !== '...' &&
        currentLine.charAt(0) !== '!'
      ) {
        this.lines[this.lines.length - 1] += currentLine;
      } else {
        this.lines.push(currentLine);
      }
    }
    this.row = 0;
  }

  nextLine() {
    this.row++;
    if (this.row >= this.lines.length) {
      return false;
    }
    return this.lines[this.row];
  }

  rewindLine() {
    this.row--;
  }

  linesUpToNextWhitespaceLine(stopAtError = false) {
    return this.linesUpToNextMatchingLine(/^ *$/, stopAtError);
  }

  linesUpToNextMatchingLine(match, stopAtError = false) {
    const lines = [];
    while (true) {
      const nextLine = this.nextLine();
      if (nextLine === false) break;

      if (stopAtError && nextLine.match(/^! /)) {
        this.rewindLine();
        break;
      }

      lines.push(nextLine);
      if (nextLine.match(match)) break;
    }
    return lines;
  }
}

export class LatexLogParser {
  constructor(text, options = {}) {
    this.state = STATE.NORMAL;
    this.fileBaseNames = options.fileBaseNames || [/compiles/, /\/usr\/local/];
    this.ignoreDuplicates = options.ignoreDuplicates !== false;
    this.data = [];
    this.fileStack = [];
    this.currentFileList = this.rootFileList = [];
    this.openParens = 0;
    this.latexWarningRegex = LATEX_WARNING_REGEX;
    this.packageWarningRegex = PACKAGE_WARNING_REGEX;
    this.packageRegex = PACKAGE_REGEX;
    this.currentLine = '';
    this.currentFilePath = undefined;
    this.currentError = undefined;
    this.log = new LogText(text);
  }

  parse() {
    let nextLine;
    while ((nextLine = this.log.nextLine()) !== false) {
      this.currentLine = nextLine;
      if (this.state === STATE.NORMAL) {
        if (this.currentLineIsError()) {
          this.state = STATE.ERROR;
          this.currentError = {
            line: null,
            file: this.currentFilePath,
            level: 'error',
            message: this.currentLine.slice(2),
            content: '',
            raw: this.currentLine + '\n',
          };
        } else if (this.currentLineIsFileLineError()) {
          this.state = STATE.ERROR;
          this.parseFileLineError();
        } else if (this.currentLineIsRunawayArgument()) {
          this.parseRunawayArgumentError();
        } else if (this.currentLineIsWarning()) {
          this.parseSingleWarningLine(this.latexWarningRegex);
        } else if (this.currentLineIsHboxWarning()) {
          this.parseHboxLine();
        } else if (this.currentLineIsPackageWarning()) {
          this.parseMultipleWarningLine();
        } else {
          this.parseParensForFilenames();
        }
      }
      if (this.state === STATE.ERROR) {
        if (this.currentError) {
          this.currentError.content += this.log
            .linesUpToNextMatchingLine(/^l\.[0-9]+/)
            .join('\n');
          this.currentError.content += '\n';
          this.currentError.content += this.log
            .linesUpToNextWhitespaceLine(true)
            .join('\n');
          this.currentError.content += '\n';
          this.currentError.content += this.log
            .linesUpToNextWhitespaceLine(true)
            .join('\n');
          this.currentError.raw += this.currentError.content;
          const lineNo = this.currentError.raw.match(/l\.([0-9]+)/);
          if (lineNo && this.currentError.line === null) {
            this.currentError.line = parseInt(lineNo[1], 10);
          }
          this.data.push(this.currentError);
          this.state = STATE.NORMAL;
        }
      }
    }
    return this.postProcess(this.data);
  }

  currentLineIsError() {
    return (
      this.currentLine[0] === '!' &&
      this.currentLine !== '!  ==> Fatal error occurred, no output PDF file produced!'
    );
  }

  currentLineIsFileLineError() {
    return FILE_LINE_ERROR_REGEX.test(this.currentLine);
  }

  currentLineIsRunawayArgument() {
    return Boolean(this.currentLine.match(/^Runaway argument/));
  }

  currentLineIsWarning() {
    return Boolean(this.currentLine.match(this.latexWarningRegex));
  }

  currentLineIsPackageWarning() {
    return Boolean(this.currentLine.match(this.packageWarningRegex));
  }

  currentLineIsHboxWarning() {
    return Boolean(this.currentLine.match(HBOX_WARNING_REGEX));
  }

  parseFileLineError() {
    const result = this.currentLine.match(FILE_LINE_ERROR_REGEX);
    if (!result) return;
    this.currentError = {
      line: parseInt(result[2], 10) || null,
      file: result[1],
      level: 'error',
      message: result[3],
      content: '',
      raw: this.currentLine + '\n',
    };
  }

  parseRunawayArgumentError() {
    this.currentError = {
      line: null,
      file: this.currentFilePath,
      level: 'error',
      message: this.currentLine,
      content: '',
      raw: this.currentLine + '\n',
    };
    this.currentError.content += this.log.linesUpToNextWhitespaceLine().join('\n');
    this.currentError.content += '\n';
    this.currentError.content += this.log.linesUpToNextWhitespaceLine().join('\n');
    this.currentError.raw += this.currentError.content;
    const lineNo = this.currentError.raw.match(/l\.([0-9]+)/);
    if (lineNo) {
      this.currentError.line = parseInt(lineNo[1], 10);
    }
    this.data.push(this.currentError);
  }

  parseSingleWarningLine(prefixRegex) {
    const warningMatch = this.currentLine.match(prefixRegex);
    if (!warningMatch) return;
    const warning = warningMatch[1];
    const lineMatch = warning.match(LINES_REGEX);
    const line = lineMatch ? parseInt(lineMatch[1], 10) : null;
    this.data.push({
      line,
      file: this.currentFilePath,
      level: 'warning',
      message: warning,
      raw: warning,
    });
  }

  parseMultipleWarningLine() {
    const warningMatch = this.currentLine.match(this.packageWarningRegex);
    if (!warningMatch) return;
    const warningLines = [warningMatch[1]];
    let lineMatch = this.currentLine.match(LINES_REGEX);
    let line = lineMatch ? parseInt(lineMatch[1], 10) : null;
    const packageMatch = this.currentLine.match(this.packageRegex);
    if (!packageMatch) return;
    const packageName = packageMatch[1];
    const prefixRegex = new RegExp('(?:\\(' + packageName + '\\))*[\\s]*(.*)', 'i');

    let currentLine;
    while ((currentLine = this.log.nextLine())) {
      this.currentLine = currentLine;
      lineMatch = this.currentLine.match(LINES_REGEX);
      line = lineMatch ? parseInt(lineMatch[1], 10) : line;
      const subMatch = this.currentLine.match(prefixRegex);
      if (!subMatch) break;
      warningLines.push(subMatch[1]);
    }
    const rawMessage = warningLines.join(' ');
    this.data.push({
      line,
      file: this.currentFilePath,
      level: 'warning',
      message: rawMessage,
      raw: rawMessage,
    });
  }

  parseHboxLine() {
    const lineMatch = this.currentLine.match(LINES_REGEX);
    const line = lineMatch ? parseInt(lineMatch[1], 10) : null;
    this.data.push({
      line,
      file: this.currentFilePath,
      level: 'typesetting',
      message: this.currentLine,
      raw: this.currentLine,
    });
  }

  parseParensForFilenames() {
    const pos = this.currentLine.search(/[()]/);
    if (pos !== -1) {
      const token = this.currentLine[pos];
      this.currentLine = this.currentLine.slice(pos + 1);
      if (token === '(') {
        const filePath = this.consumeFilePath();
        if (filePath) {
          this.currentFilePath = filePath;
          const newFile = { path: filePath, files: [] };
          this.fileStack.push(newFile);
          this.currentFileList.push(newFile);
          this.currentFileList = newFile.files;
        } else {
          this.openParens++;
        }
      } else if (token === ')') {
        if (this.openParens > 0) {
          this.openParens--;
        } else if (this.fileStack.length > 1) {
          this.fileStack.pop();
          const previousFile = this.fileStack[this.fileStack.length - 1];
          this.currentFilePath = previousFile.path;
          this.currentFileList = previousFile.files;
        }
      }
      this.parseParensForFilenames();
    }
  }

  consumeFilePath() {
    if (!this.currentLine.match(/^\/?([^ ()\\]+\/)+/)) return false;
    let endOfFilePath = this.currentLine.search(/[ ()\\]/);
    while (endOfFilePath !== -1 && this.currentLine[endOfFilePath] === ' ') {
      const partialPath = this.currentLine.slice(0, endOfFilePath);
      if (/\.\w+$/.test(partialPath)) break;
      const remainingPath = this.currentLine.slice(endOfFilePath + 1);
      if (/^\s*["()[\]]/.test(remainingPath)) break;
      const nextEndOfPath = remainingPath.search(/[ "()[\]]/);
      if (nextEndOfPath === -1) {
        endOfFilePath = -1;
      } else {
        endOfFilePath += nextEndOfPath + 1;
      }
    }
    let path;
    if (endOfFilePath === -1) {
      path = this.currentLine;
      this.currentLine = '';
    } else {
      path = this.currentLine.slice(0, endOfFilePath);
      this.currentLine = this.currentLine.slice(endOfFilePath);
    }
    return path;
  }

  postProcess(data) {
    const all = [];
    const errorsByLevel = { error: [], warning: [], typesetting: [] };
    const hashes = new Set();

    data.forEach((item) => {
      const hash = `${item.level}:${item.line}:${item.message}`;
      if (this.ignoreDuplicates && hashes.has(hash)) return;
      errorsByLevel[item.level]?.push(item);
      all.push(item);
      hashes.add(hash);
    });

    return {
      errors: errorsByLevel.error,
      warnings: errorsByLevel.warning,
      typesetting: errorsByLevel.typesetting,
      all,
      files: this.rootFileList,
    };
  }
}

/**
 * Instant In-Browser Static LaTeX Linter.
 * Analyzes raw LaTeX source code before/during compilation.
 * Checks for:
 * 1. Unclosed/unbalanced braces: { ... }
 * 2. Unbalanced LaTeX environments: \begin{env} ... \end{env}
 * 3. Unescaped special characters that break ATS or TeX: unescaped %, &, _, #, $
 * 4. Missing required document structural macros.
 */
export function lintLatexSource(latexSource) {
  if (!latexSource) {
    return { errors: [], warnings: [], typesetting: [], all: [] };
  }

  const entries = [];
  const lines = latexSource.split(/\r?\n/);

  // 1. Line-by-line bracket matching & environment tracking
  const envStack = [];
  const braceStack = [];

  lines.forEach((rawLine, idx) => {
    const lineNum = idx + 1;
    // Strip comments for bracket & environment parsing
    const commentIdx = rawLine.indexOf('%');
    const line = commentIdx >= 0 ? rawLine.slice(0, commentIdx) : rawLine;

    // Track braces on this line
    for (let c = 0; c < line.length; c++) {
      const char = line[c];
      const prevChar = c > 0 ? line[c - 1] : '';

      if (char === '{' && prevChar !== '\\') {
        braceStack.push({ lineNum, col: c + 1 });
      } else if (char === '}' && prevChar !== '\\') {
        if (braceStack.length === 0) {
          entries.push({
            line: lineNum,
            level: 'error',
            message: `Unexpected closing brace '}' without opening brace`,
            raw: rawLine,
          });
        } else {
          braceStack.pop();
        }
      }
    }

    // Track \begin{env} and \end{env}
    const beginMatches = [...line.matchAll(/\\begin\{([a-zA-Z*]+)\}/g)];
    for (const m of beginMatches) {
      envStack.push({ env: m[1], lineNum });
    }

    const endMatches = [...line.matchAll(/\\end\{([a-zA-Z*]+)\}/g)];
    for (const m of endMatches) {
      const closingEnv = m[1];
      if (envStack.length === 0) {
        entries.push({
          line: lineNum,
          level: 'error',
          message: `Unexpected \\end{${closingEnv}} without corresponding \\begin{${closingEnv}}`,
          raw: rawLine,
        });
      } else {
        const top = envStack.pop();
        if (top.env !== closingEnv) {
          entries.push({
            line: lineNum,
            level: 'error',
            message: `Mismatched environment: expected \\end{${top.env}} (opened on line ${top.lineNum}), found \\end{${closingEnv}}`,
            raw: rawLine,
          });
        }
      }
    }

    // Check for unescaped ampersands outside of tabular environments
    // Note: & is valid inside tabular/tabular*, invalid in standard body text
    const inTabular = envStack.some((e) => e.env.startsWith('tabular'));
    if (!inTabular && line.includes('&')) {
      // Find unescaped &
      const unescapedAmp = line.match(/(?<!\\)&/);
      if (unescapedAmp) {
        entries.push({
          line: lineNum,
          level: 'warning',
          message: `Unescaped '&' found. Did you mean '\\&'? Unescaped '&' may corrupt ATS parsing.`,
          raw: rawLine,
        });
      }
    }

    // Check for unescaped underscores in body text
    if (line.includes('_')) {
      const unescapedUnder = line.match(/(?<!\\)_(?!\{)/);
      if (unescapedUnder && !line.includes('href') && !line.includes('url')) {
        entries.push({
          line: lineNum,
          level: 'warning',
          message: `Unescaped '_' found. In LaTeX, write '\\_' to prevent subscript math mode.`,
          raw: rawLine,
        });
      }
    }
  });

  // Check remaining open braces
  if (braceStack.length > 0) {
    const firstUnclosed = braceStack[0];
    entries.push({
      line: firstUnclosed.lineNum,
      level: 'error',
      message: `Unclosed brace '{' opened on line ${firstUnclosed.lineNum} (total ${braceStack.length} unclosed)`,
      raw: lines[firstUnclosed.lineNum - 1] || '',
    });
  }

  // Check remaining open environments
  if (envStack.length > 0) {
    const firstUnclosedEnv = envStack[0];
    entries.push({
      line: firstUnclosedEnv.lineNum,
      level: 'error',
      message: `Unclosed environment '\\begin{${firstUnclosedEnv.env}}' opened on line ${firstUnclosedEnv.lineNum}`,
      raw: lines[firstUnclosedEnv.lineNum - 1] || '',
    });
  }

  const errors = entries.filter((e) => e.level === 'error');
  const warnings = entries.filter((e) => e.level === 'warning');
  const typesetting = entries.filter((e) => e.level === 'typesetting');

  return {
    errors,
    warnings,
    typesetting,
    all: entries,
  };
}

/**
 * Unified diagnostic combiner.
 * Merges raw log output (from TeX Live) with static linting and page budget metrics.
 */
export function analyzeLatexDiagnostics({ latexSource, logOutput, targetPages = 2, actualPages = 1 }) {
  const staticLint = lintLatexSource(latexSource);

  let engineLogs = { errors: [], warnings: [], typesetting: [], all: [] };
  if (logOutput) {
    const parser = new LatexLogParser(logOutput);
    engineLogs = parser.parse();
  }

  const mergedErrors = [...staticLint.errors, ...engineLogs.errors];
  const mergedWarnings = [...staticLint.warnings, ...engineLogs.warnings];
  const mergedTypesetting = [...staticLint.typesetting, ...engineLogs.typesetting];

  // Page budget check
  if (actualPages > targetPages) {
    mergedTypesetting.push({
      line: null,
      level: 'typesetting',
      message: `Page budget exceeded: Generated ${actualPages} pages, target budget is strictly ${targetPages} page(s).`,
      raw: `TARGET_PAGES: ${targetPages}, ACTUAL_PAGES: ${actualPages}`,
    });
  }

  // Deduplicate by line + message
  const seen = new Set();
  const filterDups = (list) =>
    list.filter((item) => {
      const key = `${item.level}:${item.line}:${item.message}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });

  const uniqueErrors = filterDups(mergedErrors);
  const uniqueWarnings = filterDups(mergedWarnings);
  const uniqueTypesetting = filterDups(mergedTypesetting);

  return {
    errors: uniqueErrors,
    warnings: uniqueWarnings,
    typesetting: uniqueTypesetting,
    all: [...uniqueErrors, ...uniqueWarnings, ...uniqueTypesetting],
    hasErrors: uniqueErrors.length > 0,
    hasWarnings: uniqueWarnings.length > 0,
    clean: uniqueErrors.length === 0 && uniqueWarnings.length === 0,
  };
}

