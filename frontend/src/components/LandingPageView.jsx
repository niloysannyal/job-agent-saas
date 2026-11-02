import React, { useState } from 'react';
import {
  Sparkles,
  Shield,
  Send,
  FileText,
  Search,
  CheckCircle,
  ArrowRight,
  ChevronDown,
  Layers,
  Terminal,
  Zap,
  Lock,
  Cpu,
  BarChart3,
  Moon,
  Sun,
  Laptop,
  Menu,
  X,
  ExternalLink,
  SlidersHorizontal,
  Check,
  Compass,
  MessageSquareCode,
  Building2,
  UserCheck,
  CheckSquare,
  Award,
} from 'lucide-react';
import { getTheme, setTheme } from '../utils/theme';

export default function LandingPageView({ onOpenLogin, onEnterApp, isAuthenticated, user }) {
  const [currentTheme, setCurrentThemeState] = useState(() => getTheme());
  const [openFaqIndex, setOpenFaqIndex] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [activeDemoTab, setActiveDemoTab] = useState('radar'); // 'radar' | 'studio' | 'outreach' | 'coach'
  const [outreachTone, setOutreachTone] = useState('direct'); // 'direct' | 'warm'

  const handleToggleTheme = () => {
    const next = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    setCurrentThemeState(next);
  };

  const toggleFaq = (idx) => {
    setOpenFaqIndex(openFaqIndex === idx ? null : idx);
  };

  const scrollToDemo = () => {
    const el = document.getElementById('interactive-demo');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const faqItems = [
    {
      q: 'Will JobEazy automatically send applications without my permission?',
      a: 'Never. Human-in-the-loop review on Send is a locked, non-negotiable architectural rule. Every single application pauses strictly at Draft until you inspect, review, and manually approve it.',
    },
    {
      q: 'Will the AI fabricate or hallucinate facts on my resume?',
      a: 'Never. The system uses a strict Verified Fact Ledger grounded in your Master CV. The AI only reorders, rewords, and emphasizes your genuine accomplishments to match role keywords—it will never invent a skill, company, metric, or credential.',
    },
    {
      q: 'Is JobEazy only for AI engineers, or does it support all tech and private jobs?',
      a: 'JobEazy is built for all technical professionals—Software Engineers, Cloud/DevOps Architects, Data Scientists, Full-Stack Developers, QA/SDETs, Engineering Leads, Product Managers, and private corporate technical roles. Sourcing filters allow you to tailor the radar precisely to your domain.',
    },
    {
      q: 'Is job sourcing legal, and will my LinkedIn account get banned?',
      a: 'JobEazy performs zero LinkedIn or Facebook web scraping and stores no third-party passwords. All opportunities are ingested directly from official, legal APIs (Adzuna, Remotive, RemoteOK, Greenhouse, Lever, Freehire), eliminating any ToS violation or ban risk.',
    },
    {
      q: 'How does the Overleaf LaTeX tailoring engine work?',
      a: 'It compiles your Master LaTeX template into pixel-perfect A4/Letter PDFs. It dynamically adjusts whitespace, bullet padding, and section margins to guarantee optimal 1-page or 2-page page budgets without awkward page overflow or ATS parsing errors.',
    },
    {
      q: 'Can I practice interviews with the STAR Interview Coach?',
      a: 'Yes. The STAR coach analyzes the specific job description, predicts likely technical and behavioral questions, and grades your answers against your real experience using the Situation, Task, Action, Result framework.',
    },
  ];

  const atsPlatforms = [
    'Greenhouse',
    'Lever',
    'Workday',
    'Ashby',
    'Taleo',
    'SmartRecruiters',
    'BambooHR',
  ];

  return (
    <div className="landing-page-root">
      {/* Sticky Top Navigation */}
      <nav className="landing-nav">
        <div className="landing-nav-container">
          <div className="landing-brand">
            <div className="landing-logo-icon">
              <Sparkles className="icon-sparkles" />
            </div>
            <div className="landing-brand-text">
              <span className="brand-title">JobEazy</span>
              <span className="brand-tag">Career OS</span>
            </div>
          </div>

          <div className="landing-nav-links desktop-only">
            <a href="#features">Features</a>
            <a href="#interactive-demo">Live Demo</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#trust">Trust & Compliance</a>
            <a href="#pricing">Pricing</a>
            <a href="#faq">FAQ</a>
          </div>

          <div className="landing-nav-actions">
            <button
              onClick={handleToggleTheme}
              className="landing-theme-btn"
              title="Toggle Light/Dark Theme"
            >
              {currentTheme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
            </button>

            {isAuthenticated ? (
              <button onClick={onEnterApp} className="action-btn-primary landing-cta-btn">
                <span>Enter Workspace</span>
                <ArrowRight size={15} />
              </button>
            ) : (
              <div className="auth-btn-group desktop-only">
                <button
                  onClick={() => onOpenLogin('login')}
                  className="landing-btn-secondary"
                >
                  Sign In
                </button>
                <button
                  onClick={() => onOpenLogin('register')}
                  className="action-btn-primary landing-cta-btn"
                >
                  <span>Signup</span>
                  <ArrowRight size={15} />
                </button>
              </div>
            )}

            {/* Mobile Hamburger Button */}
            <button
              className="mobile-menu-toggle mobile-only"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              aria-label="Toggle Navigation Menu"
            >
              {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Collapsible Mobile Navigation Drawer */}
        {isMobileMenuOpen && (
          <div className="mobile-nav-drawer">
            <div className="mobile-nav-links">
              <a href="#features" onClick={() => setIsMobileMenuOpen(false)}>Features</a>
              <a href="#interactive-demo" onClick={() => setIsMobileMenuOpen(false)}>Live Demo</a>
              <a href="#how-it-works" onClick={() => setIsMobileMenuOpen(false)}>How It Works</a>
              <a href="#trust" onClick={() => setIsMobileMenuOpen(false)}>Trust & Compliance</a>
              <a href="#pricing" onClick={() => setIsMobileMenuOpen(false)}>Pricing</a>
              <a href="#faq" onClick={() => setIsMobileMenuOpen(false)}>FAQ</a>
            </div>

            <div className="mobile-nav-actions">
              {isAuthenticated ? (
                <button
                  onClick={() => {
                    setIsMobileMenuOpen(false);
                    onEnterApp();
                  }}
                  className="action-btn-primary full-width"
                >
                  <span>Enter Workspace</span>
                  <ArrowRight size={16} />
                </button>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', width: '100%' }}>
                  <button
                    onClick={() => {
                      setIsMobileMenuOpen(false);
                      onOpenLogin('login');
                    }}
                    className="landing-btn-secondary full-width"
                  >
                    Sign In
                  </button>
                  <button
                    onClick={() => {
                      setIsMobileMenuOpen(false);
                      onOpenLogin('register');
                    }}
                    className="action-btn-primary full-width"
                  >
                    <span>Signup Free</span>
                    <ArrowRight size={16} />
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <header className="landing-hero-section">
        <div className="landing-hero-container">
          <div className="landing-hero-badge">
            <Shield size={14} className="emerald-accent" />
            <span>Autonomous Career OS • Strict Human-in-the-Loop Send Gate</span>
          </div>

          <h1 className="landing-hero-title">
            Land Your Next Tech Role Faster — <br />
            <span className="landing-hero-gradient">With Zero Fabricated Hallucinations.</span>
          </h1>

          <p className="landing-hero-subtitle">
            The autonomous career operating system for software engineers, cloud architects, data professionals, and private sector talent. Radar discovery across 6 official legal APIs, Overleaf-grade LaTeX CV tailoring, and strict verified career fact protection.
          </p>

          <div className="landing-hero-cta-group">
            <button
              onClick={() => (isAuthenticated ? onEnterApp() : onOpenLogin('register'))}
              className="action-btn-primary landing-hero-main-cta"
            >
              <span>Launch Your Career Radar</span>
              <ArrowRight size={18} />
            </button>
            <button
              onClick={scrollToDemo}
              className="landing-hero-secondary-cta"
            >
              <span>Explore Interactive Demo</span>
            </button>
          </div>

          {/* CRO Reassurance Micro-copy */}
          <div className="landing-cta-reassurance">
            <span>✓ Free Account</span>
            <span className="reassurance-dot">•</span>
            <span>✓ No Credit Card Required</span>
            <span className="reassurance-dot">•</span>
            <span>✓ 60-Second CV Onboarding</span>
            <span className="reassurance-dot">•</span>
            <span>✓ You Always Approve Send</span>
          </div>

          {/* Key Trust Metrics */}
          <div className="landing-metrics-strip">
            <div className="metric-strip-item">
              <strong>6+ Legal Feeds</strong>
              <span>Official APIs Only</span>
            </div>
            <div className="metric-strip-divider" />
            <div className="metric-strip-item">
              <strong>100% ATS Parsable</strong>
              <span>Standard LaTeX Layer</span>
            </div>
            <div className="metric-strip-divider" />
            <div className="metric-strip-item">
              <strong>0 Hallucinations</strong>
              <span>Grounded Career Fact Ledger</span>
            </div>
            <div className="metric-strip-divider" />
            <div className="metric-strip-item">
              <strong>1-Click Human Gate</strong>
              <span>You Always Click Send</span>
            </div>
          </div>

          {/* ATS Compatibility Strip */}
          <div className="landing-ats-strip">
            <span className="ats-strip-label">Engineered for 100% ATS compatibility across:</span>
            <div className="ats-badges-row">
              {atsPlatforms.map((name) => (
                <span key={name} className="ats-badge-pill">
                  <Check size={12} className="ats-check-icon" />
                  <span>{name}</span>
                </span>
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* Interactive 4-Pillar Live Demo Showcase */}
      <section id="interactive-demo" className="landing-demo-section">
        <div className="landing-section-container">
          <div className="section-header-centered">
            <div className="section-pill">Interactive Product Tour</div>
            <h2 className="section-title">Experience The 4 Pillars in Action</h2>
            <p className="section-subtitle">
              Click through the live tabs below to see how JobEazy automates discovery, tailoring, outreach, and interview prep.
            </p>
          </div>

          <div className="landing-preview-window">
            {/* Topbar with Tab Navigation */}
            <div className="preview-window-topbar">
              <div className="window-dots desktop-only">
                <span className="dot red" />
                <span className="dot yellow" />
                <span className="dot green" />
              </div>

              {/* Interactive Demo Tabs */}
              <div className="demo-tab-switcher">
                <button
                  type="button"
                  className={`demo-tab-btn ${activeDemoTab === 'radar' ? 'active' : ''}`}
                  onClick={() => setActiveDemoTab('radar')}
                >
                  <Search size={14} />
                  <span>1. Radar Feed</span>
                </button>
                <button
                  type="button"
                  className={`demo-tab-btn ${activeDemoTab === 'studio' ? 'active' : ''}`}
                  onClick={() => setActiveDemoTab('studio')}
                >
                  <FileText size={14} />
                  <span>2. LaTeX Studio</span>
                </button>
                <button
                  type="button"
                  className={`demo-tab-btn ${activeDemoTab === 'outreach' ? 'active' : ''}`}
                  onClick={() => setActiveDemoTab('outreach')}
                >
                  <Send size={14} />
                  <span>3. Outreach</span>
                </button>
                <button
                  type="button"
                  className={`demo-tab-btn ${activeDemoTab === 'coach' ? 'active' : ''}`}
                  onClick={() => setActiveDemoTab('coach')}
                >
                  <Zap size={14} />
                  <span>4. STAR Coach</span>
                </button>
              </div>

              <div className="window-tag desktop-only">
                {activeDemoTab === 'radar' && 'Vector Qdrant Radar'}
                {activeDemoTab === 'studio' && 'Overleaf LaTeX Engine'}
                {activeDemoTab === 'outreach' && 'Human Gate on Send'}
                {activeDemoTab === 'coach' && 'STAR Method Coach'}
              </div>
            </div>

            {/* TAB 1: RADAR SOURCING PREVIEW */}
            {activeDemoTab === 'radar' && (
              <div className="demo-panel demo-radar-panel">
                <div className="demo-radar-header">
                  <div className="demo-radar-search-mock">
                    <Search size={14} />
                    <span>Searching: "Senior Software Engineer" • Remote / Hybrid • Last 7 Days</span>
                  </div>
                  <div className="demo-radar-badge">
                    <span>Legal API Feed: Adzuna Verified</span>
                  </div>
                </div>

                <div className="demo-job-card-mock">
                  <div className="demo-job-card-top">
                    <div>
                      <div className="demo-job-company">Stripe • Platform Infrastructure</div>
                      <h4 className="demo-job-title">Staff / Senior Backend Systems Engineer</h4>
                      <div className="demo-job-meta">
                        <span>Remote (US/EU/Global)</span>
                        <span>•</span>
                        <span>$185k – $240k USD</span>
                        <span>•</span>
                        <span>Posted 2 days ago</span>
                      </div>
                    </div>
                    <div className="demo-match-score-pill">
                      <Sparkles size={14} />
                      <span>96% Vector Match</span>
                    </div>
                  </div>

                  <p className="demo-job-desc">
                    Looking for a systems engineer with deep expertise in Python, Go, distributed consensus, high-throughput message streaming, and PostgreSQL/Redis at scale.
                  </p>

                  <div className="demo-match-breakdown">
                    <div className="match-trait-badge hit">✓ Distributed Systems (100%)</div>
                    <div className="match-trait-badge hit">✓ Python & FastAPI (100%)</div>
                    <div className="match-trait-badge hit">✓ Redis & Postgres (95%)</div>
                    <div className="match-trait-badge hit">✓ Docker & K8s (92%)</div>
                  </div>

                  <div className="demo-job-card-actions">
                    <button
                      onClick={() => (isAuthenticated ? onEnterApp() : onOpenLogin('register'))}
                      className="action-btn-primary small-btn"
                    >
                      <span>Tailor LaTeX CV for This Role</span>
                      <ArrowRight size={14} />
                    </button>
                    <span className="demo-fact-status">🛡️ 0 Fact Hallucinations Enforced</span>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: LATEX STUDIO PREVIEW */}
            {activeDemoTab === 'studio' && (
              <div className="preview-window-body">
                <div className="preview-mock-editor">
                  <div className="mock-toolbar">
                    <span className="mock-tab active">main.tex (LaTeX Template)</span>
                    <span className="mock-badge">Verified Fact Audit: Passed</span>
                  </div>
                  <div className="mock-code-area">
                    <span className="code-line comment">% Autonomous Tailored CV for Senior Systems Engineer</span>
                    <span className="code-line kw">\documentclass[a4paper,11pt]{'{article}'}</span>
                    <span className="code-line kw">\usepackage{'{sourcesanspro, hyperref}'}</span>
                    <span className="code-line">\section{'{CORE TECHNICAL COMPETENCIES}'}</span>
                    <span className="code-line string">• Languages: Python, Go, TypeScript, SQL</span>
                    <span className="code-line string">• Backend & Cloud: FastAPI, Docker, Kubernetes, AWS, Redis</span>
                    <span className="code-line string">• Architecture: Distributed Systems, REST/gRPC APIs, High Throughput</span>
                    <span className="code-line">\section{'{VERIFIED PROFESSIONAL EXPERIENCE}'}</span>
                    <span className="code-line string">\textbf{'{Lead Platform Architect}'} • Scale Engineering</span>
                    <span className="code-line comment">% Reordered bullet for job keyword alignment:</span>
                    <span className="code-line string">• Reduced API latency by 62% across 45M daily database queries.</span>
                  </div>
                </div>

                <div className="preview-mock-pdf">
                  <div className="mock-pdf-header">
                    <div className="mock-pdf-title">Jordan Vance</div>
                    <div className="mock-pdf-contact">Senior Platform Engineer • San Francisco, CA • jordan.vance@example.com</div>
                  </div>
                  <div className="mock-pdf-line" />
                  <div className="mock-pdf-section-title">CORE TECHNICAL EXPERTISE</div>
                  <div className="mock-pdf-skills-row">
                    <span className="mock-pill">Python</span>
                    <span className="mock-pill">Go</span>
                    <span className="mock-pill">FastAPI</span>
                    <span className="mock-pill">Distributed Systems</span>
                    <span className="mock-pill">PostgreSQL</span>
                  </div>
                  <div className="mock-pdf-section-title" style={{ marginTop: '12px' }}>PROFESSIONAL EXPERIENCE</div>
                  <div className="mock-pdf-para" />
                  <div className="mock-pdf-para short" />
                  <div className="mock-match-badge">
                    <CheckCircle size={13} />
                    <span>Strict 1-Page Budget • 100% ATS Passed</span>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 3: OMNICHANNEL OUTREACH PREVIEW */}
            {activeDemoTab === 'outreach' && (
              <div className="demo-panel demo-outreach-panel">
                <div className="outreach-controls-strip">
                  <div className="outreach-tone-selector">
                    <span>Outreach Tone:</span>
                    <button
                      type="button"
                      className={`tone-btn ${outreachTone === 'direct' ? 'active' : ''}`}
                      onClick={() => setOutreachTone('direct')}
                    >
                      Direct & Technical
                    </button>
                    <button
                      type="button"
                      className={`tone-btn ${outreachTone === 'warm' ? 'active' : ''}`}
                      onClick={() => setOutreachTone('warm')}
                    >
                      Warm & Narrative
                    </button>
                  </div>
                  <div className="outreach-gate-badge">
                    <Lock size={12} />
                    <span>Status: Draft (Awaiting Your Review)</span>
                  </div>
                </div>

                <div className="demo-outreach-body">
                  <div className="outreach-field-row">
                    <span className="outreach-label">To:</span>
                    <span className="outreach-val">hiring-team@stripe.com (Hiring Manager)</span>
                  </div>
                  <div className="outreach-field-row">
                    <span className="outreach-label">Subject:</span>
                    <span className="outreach-val">Senior Platform Engineer — Scaling Distributed Systems at Stripe</span>
                  </div>
                  <div className="outreach-text-content">
                    {outreachTone === 'direct' ? (
                      <p>
                        Hi Alex,<br /><br />
                        I noticed your team is expanding Stripe’s core platform infrastructure to support high-throughput API traffic. Over the past 4 years, I engineered distributed backend services that scaled from 5M to 45M daily transactions, reducing p99 response times by 62% using asynchronous Redis queues and optimized Postgres indexing.<br /><br />
                        I tailored my 1-page LaTeX CV specifically to your team's tech stack (Python, Go, Distributed Systems). I'd welcome 15 minutes to share how my experience directly aligns with your current scaling roadmap.
                      </p>
                    ) : (
                      <p>
                        Hello Alex,<br /><br />
                        I’ve followed Stripe’s developer-first engineering culture for years, especially your recent work on global payment reliability. As a platform engineer passionate about high-concurrency systems, I recently led the architecture of a fault-tolerant transaction pipeline handling peak bursts of 12k req/sec.<br /><br />
                        I’ve attached my tailored LaTeX CV with genuine verified metrics. Looking forward to discussing how I can contribute to your infrastructure team’s goals this quarter.
                      </p>
                    )}
                  </div>
                  <div className="outreach-footer-banner">
                    <span className="human-gate-notice">🛡️ Human-in-the-Loop Send Gate: Nothing is sent until you review and click Send.</span>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 4: STAR INTERVIEW COACH PREVIEW */}
            {activeDemoTab === 'coach' && (
              <div className="demo-panel demo-coach-panel">
                <div className="coach-question-box">
                  <div className="coach-tag">Predicted Technical Behavioral Question</div>
                  <h3>"Tell me about a high-concurrency bottleneck you diagnosed and resolved."</h3>
                </div>

                <div className="coach-star-grid">
                  <div className="star-card">
                    <span className="star-letter">S</span>
                    <strong>Situation</strong>
                    <p>API endpoints experienced 400ms latency spikes during peak morning transactions due to database connection exhaustion.</p>
                  </div>
                  <div className="star-card">
                    <span className="star-letter">T</span>
                    <strong>Task</strong>
                    <p>Maintain sub-50ms p99 latency without inflating cloud node infrastructure budget.</p>
                  </div>
                  <div className="star-card">
                    <span className="star-letter">A</span>
                    <strong>Action</strong>
                    <p>Profiled slow queries, implemented async connection pooling, and introduced Redis read-through caching with proactive invalidation.</p>
                  </div>
                  <div className="star-card">
                    <span className="star-letter">R</span>
                    <strong>Result</strong>
                    <p>Reduced p99 latency to 38ms, cut database load by 54%, and achieved zero dropped requests during peak traffic.</p>
                  </div>
                </div>

                <div className="coach-feedback-strip">
                  <Award size={18} className="emerald-accent" />
                  <div>
                    <strong>Coach Evaluation: 94/100 (Strong High-Signal Answer)</strong>
                    <p>Excellent quantification of metrics ($54\%$ DB load reduction, $38\text{ms}$ latency). Demonstrates high technical ownership.</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Problem vs. Solution Section */}
      <section className="landing-comparison-section">
        <div className="landing-section-container">
          <div className="section-header-centered">
            <h2 className="section-title">Why Job Hunting in 2026 Requires a New Operating System</h2>
            <p className="section-subtitle">
              Generic blast applications get filtered by ATS scanners. Manually tailoring resumes wastes 20+ hours a week.
            </p>
          </div>

          <div className="comparison-grid">
            <div className="comparison-card broken">
              <div className="comparison-header">
                <h3>The Traditional Manual Nightmare</h3>
                <span className="card-badge red">Broken Flow</span>
              </div>
              <ul className="comparison-list">
                <li>❌ Spending 2 hours hand-tailoring Word/LaTeX files per application</li>
                <li>❌ Blindly guessing keywords and getting filtered out by automated ATS parsers</li>
                <li>❌ Risky LinkedIn scraping bots that get your professional profile permanently banned</li>
                <li>❌ Hallucinating AI tools that invent fake jobs, metrics, and credentials</li>
                <li>❌ Losing track of follow-ups across messy spreadsheets and inbox tabs</li>
              </ul>
            </div>

            <div className="comparison-card solution">
              <div className="comparison-header">
                <h3>The JobEazy Career OS</h3>
                <span className="card-badge emerald">The New Standard</span>
              </div>
              <ul className="comparison-list">
                <li>✅ <strong>Autonomous Radar</strong> scans vetted legal APIs (Adzuna, Greenhouse, Lever, Freehire, Remotive)</li>
                <li>✅ <strong>Vector Match Scoring</strong> calculates deep semantic alignment using Qdrant</li>
                <li>✅ <strong>Overleaf-Style LaTeX Compiler</strong> compacts dynamically to strict 1 or 2 pages</li>
                <li>✅ <strong>Fact-Verification Ledger</strong> strictly enforces zero invented experience</li>
                <li>✅ <strong>Strict Human Gate</strong> puts you in control—every outreach pauses for your approval</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Core Features Bento Grid */}
      <section id="features" className="landing-features-section">
        <div className="landing-section-container">
          <div className="section-header-centered">
            <div className="section-pill">Architectural Highlights</div>
            <h2 className="section-title">Engineered For High-Signal Job Seekers</h2>
            <p className="section-subtitle">
              Built for Software Engineers, Cloud/DevOps, Data, Product, and Technical professionals seeking top-tier roles.
            </p>
          </div>

          <div className="landing-bento-grid">
            {/* Bento 1: Radar Sourcing */}
            <div className="bento-box feature-large">
              <div className="bento-icon-wrapper emerald">
                <Search size={22} />
              </div>
              <h3>Autonomous Sourcing & Semantic Radar</h3>
              <p>
                Ingests thousands of verified live postings via legal partner feeds. Computes high-dimensional vector embeddings with Qdrant to rank roles by true semantic fit, ignoring noisy buzzwords.
              </p>
              <div className="bento-footer-tag">6 Legal Integrations • 0 Web Scraping</div>
            </div>

            {/* Bento 2: Overleaf Studio */}
            <div className="bento-box feature-large">
              <div className="bento-icon-wrapper cyan">
                <FileText size={22} />
              </div>
              <h3>Interactive Overleaf-Grade LaTeX Studio</h3>
              <p>
                Live dual-column LaTeX source and visual A4 PDF renderer. Compacts dynamically to 1-page or 2-page page budgets with full ATS text-layer compliance. Download ready-to-compile `.tex` or raw PDFs in seconds.
              </p>
              <div className="bento-footer-tag">Dynamic Page Budgeting • ATS Verified</div>
            </div>

            {/* Bento 3: Fact Ledger */}
            <div className="bento-box">
              <div className="bento-icon-wrapper indigo">
                <Shield size={20} />
              </div>
              <h4>Verified Fact Ledger</h4>
              <p>
                Your Master CV is the single source of truth. The agent reorders and refines genuine experience without fabricating facts.
              </p>
            </div>

            {/* Bento 4: Omnichannel Outreach */}
            <div className="bento-box">
              <div className="bento-icon-wrapper purple">
                <Send size={20} />
              </div>
              <h4>Omnichannel Outreach</h4>
              <p>
                Drafts tailored cold emails, portal cover letters, and concise LinkedIn DMs matching the hiring team's tone.
              </p>
            </div>

            {/* Bento 5: STAR Coach */}
            <div className="bento-box">
              <div className="bento-icon-wrapper amber">
                <Zap size={20} />
              </div>
              <h4>STAR Interview Coach</h4>
              <p>
                Simulates interview sessions for matched postings, generating tailored technical questions and actionable STAR feedback.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 3-Step Lifecycle */}
      <section id="how-it-works" className="landing-lifecycle-section">
        <div className="landing-section-container">
          <div className="section-header-centered">
            <div className="section-pill">The 3-Step Cycle</div>
            <h2 className="section-title">How You Land Your Next Role</h2>
            <p className="section-subtitle">A streamlined workflow that replaces hours of repetitive manual toil.</p>
          </div>

          <div className="lifecycle-steps-grid">
            <div className="lifecycle-step-card">
              <div className="step-number">01</div>
              <h3>Find & Score</h3>
              <p>
                Radar discovers verified openings from official API feeds and calculates your semantic vector match percentage.
              </p>
            </div>
            <div className="lifecycle-step-card">
              <div className="step-number">02</div>
              <h3>Tailor in Studio</h3>
              <p>
                The Overleaf engine tailors your LaTeX CV and drafts targeted outreach while verifying every career fact.
              </p>
            </div>
            <div className="lifecycle-step-card">
              <div className="step-number">03</div>
              <h3>Review & Send</h3>
              <p>
                You inspect the drafted package and click approve. Track your progression and automated follow-ups in the Kanban pipeline.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Compliance & Trust */}
      <section id="trust" className="landing-trust-section">
        <div className="landing-section-container">
          <div className="trust-banner-card">
            <div className="trust-badge-row">
              <Shield size={24} className="emerald-accent" />
              <h3>The Non-Negotiable Human-in-the-Loop Guarantee</h3>
            </div>
            <p>
              JobEazy was built to solve the ethical and legal dilemmas of automated job applications. We permanently reject robotic auto-apply bots that flood recruiters with spam. Every submission ends at Draft, requiring your explicit, conscious approval.
            </p>
            <div className="trust-pills-row">
              <span className="trust-pill">🛡️ 100% Legal Official APIs</span>
              <span className="trust-pill">🔒 Zero Password Storage</span>
              <span className="trust-pill">✅ Strictly Verified Fact Audit</span>
              <span className="trust-pill">👤 Human Gate On Send</span>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Tiers */}
      <section id="pricing" className="landing-pricing-section">
        <div className="landing-section-container">
          <div className="section-header-centered">
            <div className="section-pill">Transparent Pricing</div>
            <h2 className="section-title">Invest in Your Career Acceleration</h2>
            <p className="section-subtitle">Start free today during personal validation. No credit card required.</p>
          </div>

          <div className="pricing-cards-grid">
            {/* Free Tier */}
            <div className="pricing-card">
              <div className="pricing-badge">Personal Validation</div>
              <h3>Free Candidate</h3>
              <div className="pricing-price">
                <span className="currency">$</span>
                <span className="amount">0</span>
                <span className="period">/ month</span>
              </div>
              <p className="pricing-desc">Everything you need to run your personal job search.</p>
              <ul className="pricing-features">
                <li><CheckCircle size={15} /> 50 Ingested Radar Opportunities/mo</li>
                <li><CheckCircle size={15} /> Overleaf-Style Master CV Tailoring</li>
                <li><CheckCircle size={15} /> Cover Letter & Outreach Drafting</li>
                <li><CheckCircle size={15} /> Kanban Application Tracking</li>
                <li><CheckCircle size={15} /> Grounded Fact Ledger Audit</li>
              </ul>
              <button
                onClick={() => onOpenLogin('register')}
                className="action-btn-primary pricing-btn"
              >
                Signup
              </button>
            </div>

            {/* Pro Career Hunter Tier */}
            <div className="pricing-card featured">
              <div className="pricing-badge-popular">Most Popular</div>
              <div className="pricing-badge">Power User</div>
              <h3>Pro Career Hunter</h3>
              <div className="pricing-price">
                <span className="currency">$</span>
                <span className="amount">29</span>
                <span className="period">/ month</span>
              </div>
              <p className="pricing-desc">For serious candidates targeting competitive technical & private sector roles.</p>
              <ul className="pricing-features">
                <li><CheckCircle size={15} /> Unlimited Radar Sourcing</li>
                <li><CheckCircle size={15} /> Multi-Template LaTeX Curated Styles</li>
                <li><CheckCircle size={15} /> STAR Interview Simulator & Critique</li>
                <li><CheckCircle size={15} /> High-Priority Failover LLM Routing</li>
                <li><CheckCircle size={15} /> Automated 10-day Follow-Up Reminders</li>
              </ul>
              <button
                onClick={() => onOpenLogin('register')}
                className="action-btn-primary pricing-btn"
              >
                Join Pro Waitlist
              </button>
            </div>

            {/* Enterprise Tier */}
            <div className="pricing-card">
              <div className="pricing-badge">Teams & Agencies</div>
              <h3>Enterprise OS</h3>
              <div className="pricing-price">
                <span className="currency">$</span>
                <span className="amount">99</span>
                <span className="period">/ month</span>
              </div>
              <p className="pricing-desc">For career coaching agencies and multi-candidate managers.</p>
              <ul className="pricing-features">
                <li><CheckCircle size={15} /> Multi-Tenant Workspace Management</li>
                <li><CheckCircle size={15} /> Custom Dedicated Vector Namespace</li>
                <li><CheckCircle size={15} /> Custom API Adapters (Greenhouse, Lever)</li>
                <li><CheckCircle size={15} /> Priority Support & Audit Logs</li>
              </ul>
              <button
                onClick={() => onOpenLogin('register')}
                className="landing-btn-secondary pricing-btn"
              >
                Contact Team
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive FAQ Accordion */}
      <section id="faq" className="landing-faq-section">
        <div className="landing-section-container">
          <div className="section-header-centered">
            <div className="section-pill">Got Questions?</div>
            <h2 className="section-title">Frequently Asked Questions</h2>
            <p className="section-subtitle">Everything you need to know about our technology and philosophy.</p>
          </div>

          <div className="faq-accordion-list">
            {faqItems.map((item, idx) => (
              <div
                key={idx}
                className={`faq-accordion-item ${openFaqIndex === idx ? 'open' : ''}`}
                onClick={() => toggleFaq(idx)}
              >
                <div className="faq-question">
                  <h4>{item.q}</h4>
                  <ChevronDown
                    size={18}
                    className={`faq-icon ${openFaqIndex === idx ? 'rotate' : ''}`}
                  />
                </div>
                {openFaqIndex === idx && <p className="faq-answer">{item.a}</p>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="landing-final-cta-section">
        <div className="landing-section-container">
          <div className="final-cta-card">
            <h2>Ready to Automate Your Job Hunt the Right Way?</h2>
            <p>
              Experience the power of semantic radar sourcing, Overleaf-style LaTeX tailoring, and zero-hallucination fact protection.
            </p>
            <button
              onClick={() => (isAuthenticated ? onEnterApp() : onOpenLogin('register'))}
              className="action-btn-primary final-cta-btn"
            >
              <span>Signup for JobEazy</span>
              <ArrowRight size={18} />
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="landing-footer-container">
          <div className="footer-left">
            <div className="landing-brand">
              <div className="landing-logo-icon">
                <Sparkles className="icon-sparkles" />
              </div>
              <span className="brand-title">JobEazy</span>
            </div>
            <p className="footer-copyright">
              © {new Date().getFullYear()} JobEazy. Built for high-leverage career automation.
            </p>
          </div>

          <div className="footer-links">
            <a href="#features">Features</a>
            <a href="#interactive-demo">Live Demo</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#trust">Compliance</a>
            <a href="#pricing">Pricing</a>
            <a href="#faq">FAQ</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
