import React from 'react';
import {
  ShieldCheck,
  AlertTriangle,
  Building2,
  MapPin,
  ExternalLink,
  Target,
  ArrowRight,
  Banknote,
} from 'lucide-react';
import { formatSalary } from './JobsView';

export default function JobDetailModal({
  job,
  onClose,
  onApplyInStudio,
}) {
  if (!job) return null;

  const rawScore = job.match_score != null ? (job.match_score <= 1.0 ? job.match_score * 100 : job.match_score) : null;
  const matchScore = rawScore != null ? Math.round(rawScore) : null;
  const isClean = job.posting_integrity_verdict !== 'FLAGGED';
  const salaryInfo = formatSalary(job);

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card panel-card job-detail-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-header-left">
            <span className="source-tag">
              {job.source?.toLowerCase().includes('linkedin') && 'via LinkedIn'}
              {job.source?.toLowerCase().includes('remoteok') && 'via RemoteOK'}
              {job.source?.toLowerCase().includes('freehire') && 'via freehire.me'}
              {!job.source?.toLowerCase().includes('linkedin') && !job.source?.toLowerCase().includes('remoteok') && !job.source?.toLowerCase().includes('freehire') && job.source}
            </span>
            <span className={isClean ? 'guard-tag-clean' : 'guard-tag-flagged'}>
              {isClean ? <ShieldCheck className="icon-xxs" /> : <AlertTriangle className="icon-xxs" />}
              <span>{isClean ? 'Posting Guard Verified Clean' : 'Flagged by Posting Guard'}</span>
            </span>
          </div>
          <button className="close-modal-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-job-title-row">
          <div>
            <h3 className="modal-job-title">{job.title || job.role}</h3>
            <p className="modal-job-company">
              <Building2 className="icon-xs" />
              <span>{job.company}</span>
              <span className="bullet-sep">•</span>
              <MapPin className="icon-xs" />
              <span>{job.location || 'Remote'}</span>
            </p>
            <div className="modal-salary-pill">
              <Banknote className="icon-xs" />
              <span>{salaryInfo.text}</span>
            </div>
          </div>

          <div className="modal-score-badge">
            <span className="score-val">{matchScore != null ? `${matchScore}%` : '--'}</span>
            <span className="score-lbl">Vector Fit</span>
          </div>
        </div>

        {/* Semantic Match Reasoning */}
        {job.match_reasoning && (
          <div className="modal-reasoning-card">
            <Target className="reasoning-icon" />
            <div>
              <strong>Vector Matching Diagnostic:</strong>
              <p>{job.match_reasoning}</p>
            </div>
          </div>
        )}

        {/* Full Job Description */}
        <div className="modal-description-body">
          <h4>Full Job Posting Requirements</h4>
          <div
            className="posting-html-content"
            dangerouslySetInnerHTML={{
              __html: job.description || 'No job description provided.',
            }}
          />
        </div>

        {/* Modal Footer CTA */}
        <div className="modal-footer">
          {job.url && (
            <a
              href={job.url}
              target="_blank"
              rel="noreferrer"
              className="action-btn-secondary"
            >
              <span>View Original Posting</span>
              <ExternalLink className="btn-icon-xs" />
            </a>
          )}

          <button
            className="action-btn-primary"
            onClick={() => {
              onClose();
              onApplyInStudio(job);
            }}
          >
            <span>Open in Application Studio</span>
            <ArrowRight className="btn-icon" />
          </button>
        </div>
      </div>
    </div>
  );
}
