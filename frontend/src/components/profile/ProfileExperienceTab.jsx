import React from 'react';
import { Briefcase, Plus, Edit2, Trash2 } from 'lucide-react';

export default function ProfileExperienceTab({
  profile,
  handleOpenAddExp,
  handleOpenEditExp,
  handleDeleteExp,
}) {
  return (
    <div className="panel-card">
      <div className="panel-header">
        <div>
          <h3>Work Experience History</h3>
          <p className="subtext">Chronological career milestones used as ground truth for CV tailoring.</p>
        </div>
        <button className="action-btn-primary" onClick={handleOpenAddExp}>
          <Plus size={16} /> Add Position
        </button>
      </div>

      <div className="experience-list">
        {(!profile?.work_experiences || profile.work_experiences.length === 0) ? (
          <div className="empty-panel-state">
            <Briefcase size={36} className="dim-icon" />
            <h4>No work experiences recorded yet</h4>
            <p>Click "Add Position" above or upload your CV to auto-fill your career history.</p>
          </div>
        ) : (
          profile.work_experiences.map((exp) => (
            <div key={exp.id} className="career-card">
              <div className="career-card-header">
                <div>
                  <div className="role-company-line">
                    <h4 className="card-title">{exp.title}</h4>
                    <span className="card-at">at</span>
                    <h4 className="card-company">{exp.company}</h4>
                    {exp.is_current && <span className="badge-active">Current</span>}
                  </div>
                  <div className="card-meta">
                    <span>{exp.start_date} -- {exp.is_current ? 'Present' : exp.end_date}</span>
                    {exp.location && <span> &bull; {exp.location} ({exp.location_type})</span>}
                  </div>
                </div>
                <div className="card-actions">
                  <button className="btn-icon-subtle" title="Edit Position" onClick={() => handleOpenEditExp(exp)}>
                    <Edit2 size={15} />
                  </button>
                  <button className="btn-icon-danger" title="Remove Position" onClick={() => handleDeleteExp(exp.id)}>
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>

              {exp.description && <p className="card-desc">{exp.description}</p>}

              {exp.highlights && (
                <ul className="card-highlights">
                  {(typeof exp.highlights === 'string' && exp.highlights.startsWith('[')
                    ? JSON.parse(exp.highlights)
                    : exp.highlights.split('\n')
                  ).map((bullet, idx) => (
                    <li key={idx}>{bullet}</li>
                  ))}
                </ul>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

