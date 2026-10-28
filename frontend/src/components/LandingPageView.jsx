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
} from 'lucide-react';
import { getTheme, setTheme } from '../utils/theme';

export default function LandingPageView({ onOpenLogin, onEnterApp, isAuthenticated, user }) {
  const [currentTheme, setCurrentThemeState] = useState(() => getTheme());
  const [openFaqIndex, setOpenFaqIndex] = useState(null);

  const handleToggleTheme = () => {
    const next = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    setCurrentThemeState(next);
  };

  const toggleFaq = (idx) => {
    setOpenFaqIndex(openFaqIndex === idx ? null : idx);
  };

  const faqItems = [
    {
      q: 'Will JobEazy automatically send applications without my permission?',
      a: 'Never. Human-in-the-loop review on Send is a locked, non-negotiable architectural rule. Every single application pauses strictly at Draft until you inspect, review, and manually approve it.',
    },
    {
      q: 'Will the AI fabricate or hallucinate facts on my resume?',
      a: 'Never. The system uses a strict Verified Fact Ledger grounded in your Master CV. The AI only reorders, rewords, and emphasizes your genuine accomplishments to match role keywords—it will never invent a skill, company, or metric that is not in your grounding data.',
    },
    {
      q: 'Is job sourcing legal, and will my LinkedIn account get banned?',
      a: 'JobEazy does zero LinkedIn or Facebook web scraping and stores no third-party passwords. All opportunities are ingested directly from official, legal APIs (Adzuna, Remotive, RemoteOK, Greenhouse, Lever, Freehire), eliminating any ToS violation or ban risk.',
    },
    {
      q: 'How does the Overleaf LaTeX tailoring engine work?',
      a: 'It compiles your Master LaTeX template into pixel-perfect A4/Letter PDFs. It dynamically adjusts whitespace, bullet padding, and section margins to guarantee optimal 1-page or 2-page page budgets without awkward page overflow.',
    },
    {
      q: 'Can I practice interviews with the STAR Interview Coach?',
      a: 'Yes. The STAR coach analyzes the specific job description, predicts likely technical and behavioral questions, and grades your answers against your real experience using the Situation, Task, Action, Result framework.',
    },
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

          <div className="landing-nav-links">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#trust">Compliance & Trust</a>
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
              <>
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
                  <span>Get Started Free</span>
                  <ArrowRight size={15} />
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="landing-hero-section">
        <div className="landing-hero-container">
          <div className="landing-hero-badge">
            <Shield size={14} className="emerald-accent" />
            <span>Production Ready v1.0 • Strict Human-in-the-Loop Send Gate</span>
          </div>

          <h1 className="landing-hero-title">
            Land Your Dream AI Role 10x Faster — <br />
            <span className="landing-hero-gradient">With Zero Fabricated Hallucinations.</span>
          </h1>

          <p className="landing-hero-subtitle">
            Autonomous radar sourcing across 6 legal APIs, Overleaf-grade LaTeX CV tailoring, and strict verified career fact protection. No spam, no robotic auto-sending, no account bans.
          </p>

          <div className="landing-hero-cta-group">
            <button
              onClick={() => (isAuthenticated ? onEnterApp() : onOpenLogin('register'))}
              className="action-btn-primary landing-hero-main-cta"
            >
              <span>Launch Your Autonomous Job Radar</span>
              <ArrowRight size={18} />
            </button>
            <button
              onClick={() => (isAuthenticated ? onEnterApp() : onOpenLogin('login'))}
              className="landing-hero-secondary-cta"
            >
              <span>Explore Interactive Demo</span>
            </button>
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

          {/* App Visual Preview Card */}
          <div className="landing-preview-window">
            <div className="preview-window-topbar">
              <div className="window-dots">
                <span className="dot red" />
                <span className="dot yellow" />
                <span className="dot green" />
              </div>
              <div className="window-address">
                <Lock size={12} />
                <span>jobeazy.app / application-studio</span>
              </div>
              <div className="window-tag">Live A4 LaTeX Engine</div>
            </div>

            <div className="preview-window-body">
              <div className="preview-mock-editor">
                <div className="mock-toolbar">
                  <span className="mock-tab active">main.tex (LaTeX Source)</span>
                  <span className="mock-badge">Verified Fact Audit: Passed</span>
                </div>
                <div className="mock-code-area">
                  <span className="code-line comment">% Autonomous Tailored CV for Senior AI Engineer</span>
                  <span className="code-line kw">\documentclass[a4paper,11pt]{'{article}'}</span>
                  <span className="code-line kw">\usepackage{'{sourcesanspro, hyperref}'}</span>
                  <span className="code-line">\section{'{TECHNICAL SKILLS}'}</span>
                  <span className="code-line string">• Languages: Python, SQL, TypeScript, C++</span>
                  <span className="code-line string">• AI & ML: PyTorch, FastAPI, Qdrant, RAG, LangChain</span>
                  <span className="code-line">\section{'{SELECTED FLAGSHIP PROJECTS}'}</span>
                  <span className="code-line string">\textbf{'{UFC Fight Prediction Platform}'} • Live on iOS</span>
                </div>
              </div>

              <div className="preview-mock-pdf">
                <div className="mock-pdf-header">
                  <div className="mock-pdf-title">Niloy Sannyal</div>
                  <div className="mock-pdf-contact">AI/ML Engineer • Dhaka • niloysannyal@gmail.com</div>
                </div>
                <div className="mock-pdf-line" />
                <div className="mock-pdf-section-title">TECHNICAL EXPERTISE & RAG PIPELINES</div>
                <div className="mock-pdf-para" />
                <div className="mock-pdf-para short" />
                <div className="mock-match-badge">
                  <Sparkles size={13} />
                  <span>94% Semantic Match Score</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

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
                <li>❌ Blindly guessing keywords and getting rejected by automated ATS parsers</li>
                <li>❌ Risky LinkedIn scraping bots that get your professional account banned</li>
                <li>❌ Hallucinating AI tools that invent fake jobs, metrics, and degrees</li>
                <li>❌ Losing track of follow-ups across messy spreadsheets and emails</li>
              </ul>
            </div>

            <div className="comparison-card solution">
              <div className="comparison-header">
                <h3>The JobEazy Career OS</h3>
                <span className="card-badge emerald">The New Standard</span>
              </div>
              <ul className="comparison-list">
                <li>✅ <strong>Autonomous Radar</strong> scans vetted legal APIs (Adzuna, Greenhouse, Lever, Freehire)</li>
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
              Every feature is built around privacy, precision, and compliance with modern recruitment software.
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
              JobEazy was built to solve the ethical and legal dilemmas of AI job applications. We permanently reject robotic auto-apply bots that flood recruiters with spam. Every submission ends at Draft, requiring your explicit, conscious approval.
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
            <p className="section-subtitle">Start free today during personal validation. No hidden credit card required.</p>
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
                Get Started Free
              </button>
            </div>

            {/* Pro Hunter Tier */}
            <div className="pricing-card featured">
              <div className="pricing-badge-popular">Most Popular</div>
              <div className="pricing-badge">Power User</div>
              <h3>Pro AI Hunter</h3>
              <div className="pricing-price">
                <span className="currency">$</span>
                <span className="amount">29</span>
                <span className="period">/ month</span>
              </div>
              <p className="pricing-desc">For serious candidates targeting competitive AI & tech roles.</p>
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
              <span>Get Started Free on JobEazy</span>
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
              © {new Date().getFullYear()} JobEazy. Built with pride by Niloy Sannyal.
            </p>
          </div>

          <div className="footer-links">
            <a href="#features">Features</a>
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

