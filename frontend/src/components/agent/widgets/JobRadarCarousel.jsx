import React from 'react';
import { Briefcase, Sparkles, MapPin, DollarSign, ExternalLink, ArrowRight } from 'lucide-react';
import { useAgent } from '../../../hooks/useAgent';

export default function JobRadarCarousel({ props, actions }) {
  const { sendMessage } = useAgent();
  const jobs = props?.jobs || [];
  const title = props?.title || 'Top Opportunities';

  if (!jobs.length) {
    return (
      <div className="agent-widget-empty">
        <Briefcase size={20} className="text-muted" />
        <span>No jobs matched the current criteria.</span>
      </div>
    );
  }

  const handleTailor = (job) => {
    sendMessage(`Auto-tailor my CV and draft outreach for ${job.role} at ${job.company}`, {
      job_id: job.job_id,
      company: job.company,
      role: job.role,
      targetJob: { company: job.company, role: job.role },
    });
  };

  return (
    <div className="agent-widget job-radar-carousel">
      <div className="widget-header">
        <div className="widget-title-group">
          <Sparkles size={16} className="text-emerald" />
          <span className="widget-title">{title}</span>
        </div>
        <span className="widget-badge">{jobs.length} Recommended</span>
      </div>

      <div className="carousel-track">
        {jobs.map((job) => {
          const score = job.match_score || 75;
          const isHighFit = score >= 85;

          return (
            <div key={job.job_id} className="job-radar-card">
              <div className="job-card-top">
                <div className="job-card-titles">
                  <h4 className="job-role">{job.role}</h4>
                  <span className="job-company">{job.company}</span>
                </div>
                <div className={`score-pill ${isHighFit ? 'high-fit' : 'medium-fit'}`}>
                  {score}% Fit
                </div>
              </div>

              <div className="job-card-meta">
                <div className="meta-item">
                  <MapPin size={12} />
                  <span>{job.location}</span>
                </div>
                {job.salary && job.salary !== 'Not disclosed' && (
                  <div className="meta-item">
                    <DollarSign size={12} />
                    <span>{job.salary}</span>
                  </div>
                )}
              </div>

              <div className="job-card-actions">
                {job.apply_link && (
                  <a
                    href={job.apply_link}
                    target="_blank"
                    rel="noreferrer"
                    className="btn-icon-link"
                    title="View posting"
                  >
                    <ExternalLink size={13} />
                  </a>
                )}
                <button
                  type="button"
                  className="btn-tailor-mini"
                  onClick={() => handleTailor(job)}
                >
                  <span>Auto-Tailor</span>
                  <ArrowRight size={12} />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
