import { jsPDF } from 'jspdf';

/**
 * Robustly parses LaTeX macro arguments with balanced curly braces.
 * Handles arbitrarily nested braces without regex depth issues or catastrophic backtracking.
 */
export function extractMacroArgs(text, macroName, argCount) {
  if (!text || !macroName) return [];
  const results = [];
  let searchIdx = 0;

  while (searchIdx < text.length) {
    const idx = text.indexOf(macroName, searchIdx);
    if (idx === -1) break;

    let curr = idx + macroName.length;
    // Skip whitespace or empty brackets/parentheses if any
    while (curr < text.length && /\s/.test(text[curr])) curr++;

    const args = [];
    let valid = true;

    for (let a = 0; a < argCount; a++) {
      if (curr >= text.length || text[curr] !== '{') {
        valid = false;
        break;
      }

      let depth = 0;
      let start = curr + 1;
      let end = start;
      let inEscape = false;

      while (end < text.length) {
        const ch = text[end];
        if (inEscape) {
          inEscape = false;
          end++;
          continue;
        }
        if (ch === '\\') {
          inEscape = true;
          end++;
          continue;
        }
        if (ch === '{') depth++;
        if (ch === '}') {
          if (depth === 0) break;
          depth--;
        }
        end++;
      }

      if (end >= text.length || text[end] !== '}') {
        valid = false;
        break;
      }

      args.push(text.slice(start, end));
      curr = end + 1;
      while (curr < text.length && /\s/.test(text[curr])) curr++;
    }

    if (valid && args.length === argCount) {
      results.push({ args, index: idx, length: curr - idx });
    }

    searchIdx = idx + macroName.length;
  }

  return results;
}

/**
 * Robustly decodes HTML entities into clean plain text / unicode symbols.
 */
export function decodeHtmlEntities(str) {
  if (!str) return '';
  return str
    .replace(/&amp;/g, '&')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ');
}

/**
 * Robustly cleans LaTeX inline markup into styled HTML.
 * Converts \href, \textbf, \textit, \uline, and unescapes LaTeX special chars.
 */
export function cleanLatexInline(text) {
  if (!text) return '';
  let str = text;

  // Remove LaTeX comments (% not preceded by backslash)
  str = str.replace(/(?<!\\)%.*$/gm, '');

  // Normalize single newlines inside paragraph/macro text to spaces so lines
  // flow naturally across the page width without premature breaks
  str = str.replace(/(?<!\n)\r?\n(?!\r?\n)/g, ' ');

  // Convert \href{url}{label} using extractMacroArgs
  const hrefMatches = extractMacroArgs(str, '\\href', 2);
  // Replace in reverse order so indices remain valid
  for (let i = hrefMatches.length - 1; i >= 0; i--) {
    const m = hrefMatches[i];
    const url = m.args[0].trim();
    let rawLabel = m.args[1];
    let cleanLabel = rawLabel
      .replace(/\\uline\{([^}]+)\}/g, '$1')
      .replace(/\\textnormal\{([^}]+)\}/g, '$1')
      .replace(/\\normalsize\s*/g, '')
      .replace(/\\[a-zA-Z]+\s*/g, '')
      .replace(/[{}]/g, '')
      .trim();

    const linkHtml = `<a href="${url}" target="_blank" rel="noopener noreferrer" class="cv-link">${cleanLabel}</a>`;
    str = str.slice(0, m.index) + linkHtml + str.slice(m.index + m.length);
  }

  // Convert \textbf{content} -> <strong>content</strong>
  str = str.replace(/\\textbf\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}/g, '<strong>$1</strong>');
  // Convert \textit{content} -> <em>content</em>
  str = str.replace(/\\textit\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}/g, '<em>$1</em>');
  // Convert \uline{content} -> <u>content</u>
  str = str.replace(/\\uline\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}/g, '<u>$1</u>');

  // Replace symbols and spacing
  str = str.replace(/\\textbullet/g, '•');
  str = str.replace(/\\vspace\{[^}]*\}/g, ' ');
  str = str.replace(/\\hspace\{[^}]*\}/g, ' ');

  // Strip formatting/sizing commands
  str = str.replace(/\\(?:normalsize|small|footnotesize|large|Huge|scshape)\b\s*/g, '');

  // Unescape LaTeX special characters
  str = str.replace(/\\&/g, '&');
  str = str.replace(/\\%/g, '%');
  str = str.replace(/\\\$/g, '$');
  str = str.replace(/\\_/g, '_');
  str = str.replace(/\\#/g, '#');
  str = str.replace(/~/g, ' ');

  // Clean remaining stray unescaped braces outside HTML tags
  str = str.replace(/(?<!<[^>]*)[{}]/g, '');

  return str.trim();
}

/**
 * Extracts pure plain text from LaTeX inline markup (strips HTML and formatting).
 */
export function latexToPlainText(latexInline) {
  if (!latexInline) return '';
  const html = cleanLatexInline(latexInline);
  return html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

/**
 * Extracts links from LaTeX text using balanced brace parsing: returns [{ url, label }].
 */
export function extractLinksFromLatex(latexText) {
  if (!latexText) return [];
  const links = [];
  const matches = extractMacroArgs(latexText, '\\href', 2);
  for (const m of matches) {
    const url = m.args[0].trim();
    let rawLabel = m.args[1];
    let cleanLabel = rawLabel
      .replace(/\\uline\{([^}]+)\}/g, '$1')
      .replace(/\\textnormal\{([^}]+)\}/g, '$1')
      .replace(/\\[a-zA-Z]+/g, '')
      .replace(/[{}]/g, '')
      .trim();
    links.push({ url, label: cleanLabel });
  }
  return links;
}

/**
 * Checks curly brace balance in LaTeX code.
 */
export function validateLatexBraces(latexCode) {
  let depth = 0;
  let inEscape = false;
  let line = 1;
  const errors = [];

  for (let i = 0; i < latexCode.length; i++) {
    const c = latexCode[i];
    if (c === '\n') line++;
    if (inEscape) {
      inEscape = false;
      continue;
    }
    if (c === '\\') {
      inEscape = true;
      continue;
    }
    if (c === '%') {
      while (i < latexCode.length && latexCode[i] !== '\n') i++;
      line++;
      continue;
    }
    if (c === '{') depth++;
    if (c === '}') {
      depth--;
      if (depth < 0) {
        errors.push(`Unmatched closing brace '}' around line ${line}`);
        depth = 0;
      }
    }
  }

  if (depth > 0) {
    errors.push(`Unclosed opening brace '{' (missing ${depth} closing brace(s))`);
  }

  return { isValid: errors.length === 0, errors };
}

/**
 * Comprehensive Overleaf / LaTeX CV Parser.
 */
export function parseLatexDocument(latexSource) {
  if (!latexSource) {
    return {
      header: {
        name: 'NILOY SANNYAL',
        location: 'Dhaka, Bangladesh',
        leftLinks: [],
        rightLinks: [],
        allLinks: [],
      },
      sections: [],
      stats: { wordCount: 0, lineCount: 0, sectionCount: 0 },
      errors: [],
    };
  }

  const { isValid, errors } = validateLatexBraces(latexSource);

  // Clean top %% control comments
  const lines = latexSource.split(/\r?\n/);
  const cleanedLines = [];
  let foundDocClass = false;

  for (const line of lines) {
    if (line.trim().startsWith('\\documentclass')) {
      foundDocClass = true;
    }
    if (foundDocClass && !line.trim().startsWith('%%')) {
      cleanedLines.push(line);
    }
  }

  const cleanSource = cleanedLines.length > 0 ? cleanedLines.join('\n') : latexSource;

  // Extract content between \begin{document} and \end{document}
  let bodySource = cleanSource;
  if (cleanSource.includes('\\begin{document}')) {
    bodySource = cleanSource.split('\\begin{document}')[1].split('\\end{document}')[0];
  }

  // 1. Header parsing (text before first \section)
  const firstSectionIdx = bodySource.indexOf('\\section');
  const headerBlock = firstSectionIdx !== -1 ? bodySource.slice(0, firstSectionIdx) : '';

  let name = 'NILOY SANNYAL';
  const nameMatch = headerBlock.match(/\\textbf\{(?:\\[a-zA-Z]+\s*)?([A-Za-z\s]+?)(?:\\vspace\{[^}]*\})?\}/i);
  if (nameMatch) {
    name = nameMatch[1].trim();
  }

  let location = 'Dhaka, Bangladesh';
  const locMatch = headerBlock.match(/Location:\s*([^\\|\n\r&]+)/i);
  if (locMatch) {
    location = locMatch[1].trim();
  }

  // Extract all href links in header
  const headerLinks = extractLinksFromLatex(headerBlock);
  const leftLinks = [];
  const rightLinks = [];

  for (const l of headerLinks) {
    if (l.url.startsWith('mailto:') || l.url.startsWith('tel:') || l.label.toLowerCase().includes('mail') || l.label.toLowerCase().includes('phone') || l.label.startsWith('+')) {
      rightLinks.push(l);
    } else {
      leftLinks.push(l);
    }
  }

  // 2. Section parsing
  const sections = [];
  const sectionSplitRegex = /\\section\{([^}]+)\}/g;
  const sectionTitles = [];
  const sectionBodies = [];

  let lastIdx = 0;
  let match;
  while ((match = sectionSplitRegex.exec(bodySource)) !== null) {
    if (sectionTitles.length > 0) {
      sectionBodies.push(bodySource.slice(lastIdx, match.index));
    }
    sectionTitles.push(match[1]);
    lastIdx = match.index + match[0].length;
  }
  if (sectionTitles.length > 0) {
    sectionBodies.push(bodySource.slice(lastIdx));
  }

  for (let s = 0; s < sectionTitles.length; s++) {
    const rawTitle = sectionTitles[s];
    const cleanTitle = cleanLatexInline(rawTitle).toUpperCase();
    const sBody = sectionBodies[s] || '';

    // Extract all macros with balanced braces
    const rawItems = [];

    // Quad Headings (4 args: role, location, company, dates)
    const quadMatches = extractMacroArgs(sBody, '\\resumeQuadHeading', 4);
    for (const q of quadMatches) {
      rawItems.push({
        type: 'heading',
        index: q.index,
        role: cleanLatexInline(q.args[0]),
        locationOrDate: cleanLatexInline(q.args[1]), // Location
        companyOrDegree: cleanLatexInline(q.args[2]), // Company
        submeta: cleanLatexInline(q.args[3]), // Dates
      });
    }

    // Trio Headings (3 args: title, sub, right)
    const trioMatches = extractMacroArgs(sBody, '\\resumeTrioHeading', 3);
    for (const tr of trioMatches) {
      const rawTrioTitle = tr.args[0];
      rawItems.push({
        type: 'trio_heading',
        index: tr.index,
        title: cleanLatexInline(rawTrioTitle),
        sub: cleanLatexInline(tr.args[1]),
        right: cleanLatexInline(tr.args[2]),
        contentHtml: cleanLatexInline(rawTrioTitle),
        plainText: latexToPlainText(rawTrioTitle),
        links: extractLinksFromLatex(rawTrioTitle),
      });
    }

    // Section Types (3 args: cat, sep, items)
    const sectionTypeMatches = extractMacroArgs(sBody, '\\resumeSectionType', 3);
    for (const st of sectionTypeMatches) {
      const rawCat = st.args[0];
      const rawContent = st.args[2];
      const catPlain = latexToPlainText(rawCat);
      const catHtml = cleanLatexInline(rawCat);
      const contentPlain = latexToPlainText(rawContent);
      const contentHtml = cleanLatexInline(rawContent);
      const catLinks = extractLinksFromLatex(rawCat);
      const contentLinks = extractLinksFromLatex(rawContent);

      rawItems.push({
        type: 'skills_line',
        index: st.index,
        category: catPlain, // pure plain text (e.g. "LeetCode", "Languages", "AI & ML")
        categoryPlain: catPlain,
        categoryHtml: catHtml, // styled HTML (with <a> links for web preview)
        contentHtml: contentHtml,
        plainText: contentPlain,
        links: [...catLinks, ...contentLinks],
      });
    }

    // Course Types (3 args: title, sep, link)
    const courseTypeMatches = extractMacroArgs(sBody, '\\resumeCourseType', 3);
    for (const ct of courseTypeMatches) {
      const rawTitle = ct.args[0];
      const rawLink = ct.args[2];
      const titlePlain = latexToPlainText(rawTitle);
      const titleHtml = cleanLatexInline(rawTitle);
      const linkPlain = latexToPlainText(rawLink);
      const linkHtml = cleanLatexInline(rawLink);

      rawItems.push({
        type: 'skills_line',
        index: ct.index,
        category: titlePlain,
        categoryPlain: titlePlain,
        categoryHtml: titleHtml,
        contentHtml: linkHtml,
        plainText: linkPlain,
        links: extractLinksFromLatex(rawLink),
      });
    }

    // Resume Items (1 arg: content)
    const itemMatches = extractMacroArgs(sBody, '\\resumeItem', 1);
    for (const it of itemMatches) {
      const rawItem = it.args[0];
      rawItems.push({
        type: 'bullet',
        index: it.index,
        contentHtml: cleanLatexInline(rawItem),
        plainText: latexToPlainText(rawItem),
        links: extractLinksFromLatex(rawItem),
      });
    }

    // Sort items by index to preserve exact chronological document order
    rawItems.sort((a, b) => a.index - b.index);

    // Fallback if no macros matched
    if (rawItems.length === 0) {
      const cleanBodyText = cleanLatexInline(sBody);
      if (cleanBodyText) {
        rawItems.push({
          type: 'prose',
          index: 0,
          contentHtml: cleanBodyText,
          plainText: latexToPlainText(sBody),
          links: extractLinksFromLatex(sBody),
        });
      }
    }

    sections.push({
      title: cleanTitle,
      items: rawItems,
    });
  }

  const wordCount = bodySource.replace(/<[^>]+>/g, '').split(/\s+/).filter(Boolean).length;
  const lineCount = lines.length;
  const projectSec = sections.find(s => s.title.includes('PROJECT'));
  const isOnePage = Boolean(projectSec && projectSec.items.length <= 4 && lineCount <= 235);

  return {
    header: {
      name,
      location,
      leftLinks: leftLinks.length > 0 ? leftLinks : [
        { label: 'Portfolio', url: 'https://www.niloysannyal.me/' },
        { label: 'LinkedIn', url: 'https://www.linkedin.com/in/niloysannyal/' },
        { label: 'GitHub', url: 'https://github.com/niloysannyal' },
        { label: 'LeetCode', url: 'https://leetcode.com/NiloySannyal/' },
      ],
      rightLinks: rightLinks.length > 0 ? rightLinks : [
        { label: 'niloysannyal@gmail.com', url: 'mailto:niloysannyal@gmail.com' },
        { label: '+8801783445245', url: 'tel:+8801783445245' },
      ],
      allLinks: headerLinks,
    },
    sections,
    isOnePage,
    stats: {
      wordCount,
      lineCount,
      sectionCount: sections.length,
    },
    errors,
  };
}

/**
 * Estimates vertical height for an item on an A4 page in points (total page height = 841.89 pt).
 */
export function estimateItemHeight(item) {
  if (item.type === 'skills_line') {
    const textLen = (item.plainText || item.contentHtml || '').length;
    return textLen > 95 ? 26 : 16;
  }
  if (item.type === 'heading') {
    return 26;
  }
  if (item.type === 'trio_heading') {
    return 20;
  }
  if (item.type === 'bullet') {
    const textLen = (item.plainText || '').length;
    if (textLen > 180) return 38;
    if (textLen > 90) return 26;
    return 16;
  }
  if (item.type === 'prose') {
    const textLen = (item.plainText || '').length;
    return Math.max(18, Math.ceil(textLen / 90) * 14);
  }
  return 16;
}

/**
 * Paginate parsed document items into discrete authentic A4 sheets (max height ~770 pt).
 */
export function paginateParsedDocument(parsedDoc, maxPageHeight = 770) {
  if (!parsedDoc || !parsedDoc.sections) return [];

  const pages = [];
  let currentPage = { pageNumber: 1, hasHeader: true, sections: [] };
  let currentHeight = 75; // Header occupies ~75pt
  let renderedExperience = false;

  for (const sec of parsedDoc.sections) {
    const secHeaderHeight = 26;

    // Senior Recruiter 2-page split: Page 1 holds Header + Summary + Professional Experience + Technical Skills.
    // Start Page 2 cleanly with Selected Flagship Projects for perfect visual balance (if multi-page)!
    const shouldBreakBeforeProjects = (
      !parsedDoc.isOnePage &&
      currentPage.pageNumber === 1 &&
      sec.title.includes('PROJECT') &&
      renderedExperience
    );

    if (shouldBreakBeforeProjects || (currentHeight + secHeaderHeight > maxPageHeight)) {
      pages.push(currentPage);
      currentPage = { pageNumber: pages.length + 1, hasHeader: false, sections: [] };
      currentHeight = 0;
    }

    if (sec.title.includes('EXPERIENCE')) {
      renderedExperience = true;
    }

    let currentSecOnPage = { title: sec.title, items: [] };
    currentHeight += secHeaderHeight;
    currentPage.sections.push(currentSecOnPage);

    for (const item of sec.items) {
      const h = estimateItemHeight(item);
      // Orphan heading protection: require at least 50pt for headings so initial bullets don't get detached
      const minRequired = (item.type === 'trio_heading' || item.type === 'heading') ? 50 : h;

      if (currentHeight + minRequired > maxPageHeight) {
        pages.push(currentPage);
        currentPage = { pageNumber: pages.length + 1, hasHeader: false, sections: [] };
        currentHeight = 0;
        currentSecOnPage = { title: `${sec.title} (cont.)`, items: [] };
        currentPage.sections.push(currentSecOnPage);
      }
      currentSecOnPage.items.push(item);
      currentHeight += h;
    }
  }

  if (currentPage.sections.length > 0) {
    pages.push(currentPage);
  }

  return pages;
}

/**
 * Compacts and budgets raw LaTeX to strictly 1 or 2 pages matching senior recruiter guidelines.
 */
export function compactLatex(rawLatex, targetPages = 2, role = 'AI Engineer', description = '') {
  if (!rawLatex) return rawLatex;

  let text = rawLatex;

  // Track target page count in LaTeX comment
  text = text.replace(/% TARGET_PAGES: \d+\n?/g, '');
  if (text.includes('\\begin{document}')) {
    text = text.replace('\\begin{document}', `\\begin{document}\n% TARGET_PAGES: ${targetPages}`);
  } else {
    text = `% TARGET_PAGES: ${targetPages}\n` + text;
  }

  // Remove duplicate/overlapping sections
  const removeSection = (src, secTitle) => {
    const escaped = secTitle.replace(/&/g, '(&|\\\\&)');
    const pat = new RegExp(`\\\\section\\{${escaped}\\}[\\s\\S]*?(?=(\\\\section\\{|\\\\end\\{document\\}|$))`, 'g');
    return src.replace(pat, '');
  };

  text = removeSection(text, 'Career Highlights');
  text = removeSection(text, 'Enterprise AI Systems & Initiatives');
  text = removeSection(text, 'Technical Leadership & Ownership');
  text = removeSection(text, 'Certifications & Courses');

  // Check if target job mentions robotics
  const jobText = `${role} ${description}`.toLowerCase();
  const needsRobotics = /(robot|embedded|hardware|arduino|drone|iot|firmware)/i.test(jobText);

  if (targetPages === 1) {
    // 1-PAGE CV BUDGET:
    // 1. Condense Professional Experience to top high-impact bullets
    const condensedExperience = `\\section{Professional Experience}
\\resumeHeadingListStart{}

\\resumeQuadHeading{AI Engineer}{Dhaka, Bangladesh}{Betopia Limited -- Betopia Group}{Apr 2026 -- Present}
\\vspace{-6pt}
\\resumeItemListStart{}
  \\resumeItem{Architected and own \\textbf{Betopia Sales Agent}, a production agentic AI system embedded directly in \\textbf{Odoo CRM}, serving \\textbf{600+ salespersons} with psychological profiling and autonomous lead-closing logic.}
  \\resumeItem{Designed a \\textbf{multi-provider LLM chain} (OpenAI, Anthropic, Gemini) with dynamic provider routing and \\textbf{Qdrant}-backed \\textbf{RAG} for context-aware response generation.}
  \\resumeItem{Delivered a \\textbf{Next.js 15} admin dashboard for real-time sales monitoring and LLM observability; established CI/CD pipelines via GitHub Actions.}
  \\resumeItem{Full-stack ownership -- requirement analysis, architecture, deployment, and server administration for the Dockerized stack (FastAPI, Postgres, Redis, Qdrant).}
\\resumeItemListEnd{}

\\resumeQuadHeading{AI Developer}{Dhaka, Bangladesh}{Softvence Agency -- Betopia Group}{Nov 2025 -- Mar 2026}
\\vspace{-6pt}
\\resumeItemListStart{}
  \\resumeItem{Built and deployed \\textbf{production-grade AI APIs} using FastAPI with \\textbf{sub-100ms inference latency} for real-time ML prediction endpoints.}
  \\resumeItem{Implemented \\textbf{RAG pipelines} with vector databases and integrated LLM APIs (OpenAI, Anthropic) with structured prompting and Dockerized AWS deployment.}
\\resumeItemListEnd{}

\\resumeHeadingListEnd{}
`;

    text = text.replace(
      /\\section\{Professional Experience\}[\s\S]*?(?=(\\section\{|\\end\{document\}|$))/,
      condensedExperience
    );

    // 2. Curate to 1 top flagship project for 1-page fit
    const singleFlagshipProject = `\\section{Selected Flagship Projects}
\\resumeHeadingListStart{}

\\resumeTrioHeading{Full Send Sports AI -- UFC Prediction Platform \\hspace{2pt} \\textbullet \\hspace{2pt}
{\\normalsize \\textnormal{\\href{https://apps.apple.com/us/app/full-send-sports-ai/id6751740118}{\\uline{App Store}}}}}{}{}
\\vspace{-6pt}
\\resumeItemListStart{}
  \\resumeItem{End-to-end ML pipeline trained on \\textbf{10,000+ UFC fights} with \\textbf{80+ engineered features}; ensemble models deployed as a FastAPI service with \\textbf{sub-100ms latency} for real-time predictions.}
  \\resumeItem{Live on the iOS App Store, serving production traffic with high-availability cloud deployment.}
  \\resumeItem{\\textbf{Tech Stack:} Python, XGBoost, LightGBM, Scikit-learn, FastAPI, AWS.}
\\resumeItemListEnd{}

\\resumeHeadingListEnd{}
`;

    text = text.replace(
      /\\section\{Projects\}[\s\S]*?(?=(\\section\{Problem Solving\}|\\section\{Education\}|\\end\{document\}|$))/,
      singleFlagshipProject
    );

  } else {
    // 2-PAGE CV BUDGET: Top 3 flagship projects + full experience
    const flagshipProjects = `\\section{Selected Flagship Projects}
\\resumeHeadingListStart{}

\\resumeTrioHeading{Full Send Sports AI -- UFC Prediction Platform \\hspace{2pt} \\textbullet \\hspace{2pt}
{\\normalsize \\textnormal{\\href{https://apps.apple.com/us/app/full-send-sports-ai/id6751740118}{\\uline{App Store}}}}}{}{}
\\vspace{-6pt}
\\resumeItemListStart{}
  \\resumeItem{End-to-end ML pipeline trained on \\textbf{10,000+ UFC fights} with \\textbf{80+ engineered features}; ensemble models deployed as a FastAPI service with \\textbf{sub-100ms latency} for real-time predictions.}
  \\resumeItem{Live on the iOS App Store, serving production traffic with high-availability cloud deployment.}
  \\resumeItem{\\textbf{Tech Stack:} Python, XGBoost, LightGBM, Scikit-learn, FastAPI, AWS.}
\\resumeItemListEnd{}

\\resumeTrioHeading{FIFA World Cup 2026 Forecast \\hspace{2pt} \\textbullet \\hspace{2pt}
{\\normalsize \\textnormal{\\href{https://fifawc2026-simulator.netlify.app/}{\\uline{Live Demo}}}}}{}{}
\\vspace{-6pt}
\\resumeItemListStart{}
  \\resumeItem{Built and deployed a football forecasting platform using \\textbf{32,247 international matches (1990--2025)}, featuring custom Elo ratings, probabilistic match prediction, and tournament simulation.}
  \\resumeItem{\\textbf{Tech Stack:} Python, Scikit-learn, FastAPI, React, Vite, Tailwind CSS, SQLite, AWS, Pandas, NumPy.}
\\resumeItemListEnd{}

\\resumeTrioHeading{Company Policy Chatbot \\hspace{2pt} \\textbullet \\hspace{2pt}
{\\normalsize \\textnormal{\\href{https://github.com/niloysannyal/Company_Policy_Chatbot}{\\uline{GitHub}} \\hspace{2pt} \\textbar{} \\hspace{2pt}
\\href{https://company-policy-chatbot.vercel.app/}{\\uline{Live Demo}}}}}{}{}
\\vspace{-6pt}
\\resumeItemListStart{}
  \\resumeItem{RAG-based chatbot answering HR and IT policy questions with context-aware responses, using vector similarity search and persisted conversation memory.}
  \\resumeItem{\\textbf{Tech Stack:} Python, Streamlit, Gemini API, FAISS, LangChain, HTML, CSS, JavaScript.}
\\resumeItemListEnd{}
${needsRobotics ? `
\\resumeTrioHeading{Arduino Robo-Car \\hspace{2pt} \\textbullet \\hspace{2pt}
{\\normalsize \\textnormal{\\href{https://github.com/niloysannyal/Robo-Car}{\\uline{GitHub}}}}}{}{}
\\vspace{-6pt}
\\resumeItemListStart{}
  \\resumeItem{Multifunctional Bluetooth-controlled robot car with custom Android app, supporting Manual, Line Following, Obstacle Avoidance via IR and ESP32-CAM sensor integration.}
  \\resumeItem{\\textbf{Tech Stack:} Arduino, C++, MIT App Inventor, Bluetooth HC-05, ESP32-CAM.}
\\resumeItemListEnd{}
` : ''}
\\resumeHeadingListEnd{}
`;

    text = text.replace(
      /\\section\{Projects\}[\s\S]*?(?=(\\section\{Problem Solving\}|\\section\{Education\}|\\end\{document\}|$))/,
      flagshipProjects
    );
  }

  text = text.replace(/\n{3,}/g, '\n\n').trim();
  return text;
}

/**
 * Backward-compatible alias for compacting to 2 pages.
 */
export function compactLatexToTwoPages(rawLatex, role = 'AI Engineer', description = '') {
  return compactLatex(rawLatex, 2, role, description);
}

/**
 * Compiles parsed LaTeX document into an Overleaf-identical publication-quality A4 PDF
 * with fully active clickable hyperlinks and precise Overleaf geometry.
 */
export function compileParsedLatexToPdf(parsedDoc, targetFilename = 'Tailored_CV.pdf') {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'pt',
    format: 'a4',
  });

  const pageWidth = 595.28;
  const pageHeight = 841.89;
  const margin = 36;
  const contentWidth = pageWidth - margin * 2;
  const maxY = pageHeight - margin - 15;
  let y = margin + 18;

  const LINK_COLOR = [37, 99, 235]; // Tailwind blue-600
  const TEXT_DARK = [17, 24, 39];
  const TEXT_MUTED = [75, 85, 99];
  const LINE_COLOR = [31, 41, 55];

  // Helper to add a new page with header reset
  const checkNewPage = (neededHeight) => {
    if (y + neededHeight > maxY) {
      doc.addPage();
      y = margin + 20;
      return true;
    }
    return false;
  };

  // 1. HEADER (Overleaf 2-column tabular layout)
  // Left Column: Candidate Name
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(18);
  doc.setTextColor(...TEXT_DARK);
  doc.text((parsedDoc.header.name || 'NILOY SANNYAL').toUpperCase(), margin, y);

  // Right Column: Location
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(...TEXT_MUTED);
  const locStr = `Location: ${parsedDoc.header.location || 'Dhaka, Bangladesh'}`;
  doc.text(locStr, pageWidth - margin, y - 2, { align: 'right' });

  // Header Line 2: Links on Left, Contact on Right
  y += 14;
  let linkX = margin;
  doc.setFontSize(8.5);

  const leftLinks = parsedDoc.header.leftLinks || [
    { label: 'Portfolio', url: 'https://www.niloysannyal.me/' },
    { label: 'LinkedIn', url: 'https://www.linkedin.com/in/niloysannyal/' },
    { label: 'GitHub', url: 'https://github.com/niloysannyal' },
    { label: 'LeetCode', url: 'https://leetcode.com/NiloySannyal/' },
  ];

  leftLinks.forEach((item, idx) => {
    doc.setTextColor(...LINK_COLOR);
    doc.textWithLink(item.label, linkX, y, { url: item.url });
    const tw = doc.getTextWidth(item.label);

    // Clickable link underline
    doc.setDrawColor(...LINK_COLOR);
    doc.setLineWidth(0.5);
    doc.line(linkX, y + 1.5, linkX + tw, y + 1.5);
    linkX += tw + 4;

    if (idx < leftLinks.length - 1) {
      doc.setTextColor(...TEXT_MUTED);
      doc.text('|', linkX, y);
      linkX += 8;
    }
  });

  // Right Column: Email | Mobile
  const rightLinks = parsedDoc.header.rightLinks || [
    { label: 'niloysannyal@gmail.com', url: 'mailto:niloysannyal@gmail.com' },
    { label: '+8801783445245', url: 'tel:+8801783445245' },
  ];

  let rightEnd = pageWidth - margin;
  for (let i = rightLinks.length - 1; i >= 0; i--) {
    const item = rightLinks[i];
    const prefix = item.url.startsWith('mailto:') ? 'Email: ' : 'Mobile: ';
    const prefixW = doc.getTextWidth(prefix);
    const labelW = doc.getTextWidth(item.label);
    const totalW = prefixW + labelW;
    const startX = rightEnd - totalW;

    doc.setFont('helvetica', 'normal');
    doc.setTextColor(...TEXT_MUTED);
    doc.text(prefix, startX, y);

    doc.setTextColor(...LINK_COLOR);
    doc.textWithLink(item.label, startX + prefixW, y, { url: item.url });
    doc.setDrawColor(...LINK_COLOR);
    doc.setLineWidth(0.5);
    doc.line(startX + prefixW, y + 1.5, startX + prefixW + labelW, y + 1.5);

    rightEnd = startX - 6;
    if (i > 0) {
      doc.setTextColor(...TEXT_MUTED);
      doc.text('|', rightEnd - 4, y);
      rightEnd -= 10;
    }
  }

  // Header Dividing Line
  y += 9;
  doc.setDrawColor(...LINE_COLOR);
  doc.setLineWidth(1.1);
  doc.line(margin, y, pageWidth - margin, y);
  y += 13;

  // 2. SECTIONS
  let renderedExperience = false;
  for (const sec of parsedDoc.sections) {
    // Senior Recruiter 2-page split: Page 1 holds Header + Summary + Professional Experience + Technical Skills.
    // Start Page 2 cleanly with Selected Flagship Projects for perfect visual balance (if multi-page)!
    if (!parsedDoc.isOnePage && doc.getNumberOfPages() === 1 && sec.title.includes('PROJECT') && renderedExperience) {
      doc.addPage();
      y = margin + 20;
    }

    if (sec.title.includes('EXPERIENCE')) {
      renderedExperience = true;
    }

    checkNewPage(45);

    // Section title (Overleaf small-caps style)
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(10.5);
    doc.setTextColor(...TEXT_DARK);
    doc.text(sec.title.toUpperCase(), margin, y);

    // Section horizontal rule (titlerule)
    y += 3;
    doc.setDrawColor(200, 205, 215);
    doc.setLineWidth(0.75);
    doc.line(margin, y, pageWidth - margin, y);
    y += 11;

    for (const item of sec.items) {
      if (item.type === 'skills_line') {
        checkNewPage(18);
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8.5);

        const cleanCat = item.categoryPlain || latexToPlainText(item.category) || '';

        // If category itself has links (e.g. Problem Solving LeetCode / Codeforces)
        const catLink = item.links?.find(lk => cleanCat.toLowerCase().includes(lk.label.toLowerCase()));
        if (catLink) {
          doc.setFont('helvetica', 'bold');
          doc.setFontSize(8.5);
          doc.setTextColor(...LINK_COLOR);
          doc.textWithLink(catLink.label, margin, y, { url: catLink.url });
          const tw = doc.getTextWidth(catLink.label);

          doc.setDrawColor(...LINK_COLOR);
          doc.setLineWidth(0.5);
          doc.line(margin, y + 1.5, margin + tw, y + 1.5);

          doc.setFont('helvetica', 'bold');
          doc.setTextColor(...TEXT_DARK);
          doc.text(':', margin + tw, y);
        } else {
          doc.setFont('helvetica', 'bold');
          doc.setFontSize(8.5);
          doc.setTextColor(...TEXT_DARK);
          doc.text(`${cleanCat}:`, margin, y);
        }

        // Skills / Problem solved count
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8.5);
        doc.setTextColor(55, 65, 81);
        const splitContent = doc.splitTextToSize(item.plainText, contentWidth - 110);
        doc.text(splitContent, margin + 110, y);
        y += Math.max(12, splitContent.length * 10.5 + 2);

      } else if (item.type === 'heading') {
        // Quad Heading: Role & Location (Line 1), Company & Dates (Line 2)
        // Orphan protection: ensure heading + space for bullets fits
        checkNewPage(45);

        // Line 1: Role (left bold) & Location (right)
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(9.5);
        doc.setTextColor(...TEXT_DARK);
        doc.text(item.role || '', margin, y);

        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8.5);
        doc.setTextColor(...TEXT_MUTED);
        doc.text(item.locationOrDate || '', pageWidth - margin, y, { align: 'right' });
        y += 11;

        // Line 2: Company / Degree (left italic) & Dates (right italic)
        doc.setFont('helvetica', 'italic');
        doc.setFontSize(9);
        doc.setTextColor(55, 65, 81);
        doc.text(item.companyOrDegree || '', margin, y);

        if (item.submeta) {
          doc.setFontSize(8.5);
          doc.setTextColor(...TEXT_MUTED);
          doc.text(item.submeta, pageWidth - margin, y, { align: 'right' });
        }
        y += 11;

      } else if (item.type === 'trio_heading') {
        // Orphan protection: require at least 55 pt so title and initial bullet stay together
        checkNewPage(55);

        doc.setFont('helvetica', 'bold');
        doc.setFontSize(9.5);
        doc.setTextColor(...TEXT_DARK);

        // Check if trio title contains embedded hyperlinks (e.g. App Store, Live Demo, GitHub)
        if (item.links && item.links.length > 0) {
          let currX = margin;
          const mainTitle = item.title.split('•')[0].trim();
          doc.text(mainTitle, currX, y);
          currX += doc.getTextWidth(mainTitle) + 4;

          doc.setFont('helvetica', 'normal');
          doc.setTextColor(...TEXT_MUTED);
          doc.text('•', currX, y);
          currX += 8;

          item.links.forEach((lk, lIdx) => {
            doc.setTextColor(...LINK_COLOR);
            doc.textWithLink(lk.label, currX, y, { url: lk.url });
            const lw = doc.getTextWidth(lk.label);
            doc.setDrawColor(...LINK_COLOR);
            doc.setLineWidth(0.5);
            doc.line(currX, y + 1.5, currX + lw, y + 1.5);
            currX += lw + 4;

            if (lIdx < item.links.length - 1) {
              doc.setTextColor(...TEXT_MUTED);
              doc.text('|', currX, y);
              currX += 8;
            }
          });
        } else {
          doc.text(item.title || '', margin, y);
        }

        if (item.right) {
          doc.setFont('helvetica', 'normal');
          doc.setFontSize(8.5);
          doc.setTextColor(...TEXT_MUTED);
          doc.text(item.right, pageWidth - margin, y, { align: 'right' });
        }
        y += 11;

      } else if (item.type === 'bullet') {
        // Bullet with hanging indent aligned with right margin rule
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8.5);
        doc.setTextColor(55, 65, 81);

        const cleanText = item.plainText || latexToPlainText(item.contentHtml);
        const splitBullet = doc.splitTextToSize(cleanText, contentWidth - 14);
        checkNewPage(splitBullet.length * 10.5 + 4);

        doc.text('•', margin + 3, y);
        doc.text(splitBullet, margin + 14, y);
        y += splitBullet.length * 10.5 + 2;

      } else if (item.type === 'prose') {
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8.5);
        doc.setTextColor(55, 65, 81);

        const cleanProse = item.plainText || latexToPlainText(item.contentHtml);
        const splitProse = doc.splitTextToSize(cleanProse, contentWidth);
        checkNewPage(splitProse.length * 10.5 + 4);

        doc.text(splitProse, margin, y);
        y += splitProse.length * 10.5 + 4;
      }
    }

    y += 7; // spacing between sections
  }

  // 3. PAGE NUMBERS (Footer at bottom center of each page)
  const totalPages = doc.getNumberOfPages();
  for (let p = 1; p <= totalPages; p++) {
    doc.setPage(p);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.setTextColor(156, 163, 175);
    const footerStr = `Page ${p} of ${totalPages}`;
    doc.text(footerStr, pageWidth / 2, pageHeight - 20, { align: 'center' });
  }

  return doc;
}
