import React from 'react';
import { GraduationCap, Plus, Edit2, Trash2 } from 'lucide-react';

export default function ProfileEducationTab({
  profile,
  handleOpenAddEdu,
  handleOpenEditEdu,
  handleDeleteEdu,
}) {
  return (
    <div className="panel-card">
      <div className="panel-header">
        <div>
          <h3>Education & Credentials</h3>
          <p className="subtext">Academic degrees, institutions, locations, and honors.</p>
        </div>
        <button className="action-btn-primary" onClick={handleOpenAddEdu}>
          <Plus size={16} /> Add Education
        </button>
      </div>

      <div className="education-list">
        {(!profile?.educations || profile.educations.length === 0) ? (
          <div className="empty-panel-state">
            <GraduationCap size={36} className="dim-icon" />
            <h4>No education entries recorded</h4>
            <p>Click "Add Education" to add degrees or coursework.</p>
          </div>
        ) : (
          profile.educations.map((edu) => (
            <div key={edu.id} className="career-card">
              <div className="career-card-header">
                <div>
                  <h4 className="card-title">{edu.degree} {edu.field_of_study && `in ${edu.field_of_study}`}</h4>
                  <h5 className="card-company">{edu.institution}</h5>
                  <div className="card-meta">
                    <span>{edu.start_date} -- {edu.end_date}</span>
                    {edu.location && <span> &bull; {edu.location}</span>}
                    {edu.grade && <span> &bull; Grade: {edu.grade}</span>}
                  </div>
                </div>
                <div className="card-actions">
                  <button className="btn-icon-subtle" title="Edit Education" onClick={() => handleOpenEditEdu(edu)}>
                    <Edit2 size={15} />
                  </button>
                  <button className="btn-icon-danger" title="Remove Education" onClick={() => handleDeleteEdu(edu.id)}>
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

