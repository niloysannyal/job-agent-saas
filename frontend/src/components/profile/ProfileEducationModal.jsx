import React from 'react';
import { X } from 'lucide-react';

export default function ProfileEducationModal({
  isOpen,
  onClose,
  editingEdu,
  eduForm,
  setEduForm,
  handleSaveEdu,
}) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="modal-content modal-medium">
        <div className="modal-header">
          <h3>{editingEdu ? 'Edit Education Background' : 'Add Education Background'}</h3>
          <button className="btn-icon-close" onClick={onClose}>
            <X size={18} />
          </button>
        </div>
        <form onSubmit={handleSaveEdu} className="modal-form">
          <div className="form-grid-2">
            <div className="form-group">
              <label>Institution / University *</label>
              <input
                type="text"
                value={eduForm.institution}
                onChange={(e) => setEduForm({ ...eduForm, institution: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Degree *</label>
              <input
                type="text"
                value={eduForm.degree}
                onChange={(e) => setEduForm({ ...eduForm, degree: e.target.value })}
                placeholder="e.g. B.Sc., M.Sc., High School"
                required
              />
            </div>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Field of Study</label>
              <input
                type="text"
                value={eduForm.field_of_study}
                onChange={(e) => setEduForm({ ...eduForm, field_of_study: e.target.value })}
                placeholder="e.g. Computer Science"
              />
            </div>
            <div className="form-group">
              <label>Campus / City Location</label>
              <input
                type="text"
                value={eduForm.location}
                onChange={(e) => setEduForm({ ...eduForm, location: e.target.value })}
                placeholder="e.g. Stanford, CA or Cambridge, UK"
              />
            </div>
          </div>

          <div className="form-grid-3">
            <div className="form-group">
              <label>Start Year</label>
              <input
                type="text"
                value={eduForm.start_date}
                onChange={(e) => setEduForm({ ...eduForm, start_date: e.target.value })}
                placeholder="2018"
              />
            </div>
            <div className="form-group">
              <label>End Year</label>
              <input
                type="text"
                value={eduForm.end_date}
                onChange={(e) => setEduForm({ ...eduForm, end_date: e.target.value })}
                placeholder="2022"
              />
            </div>
            <div className="form-group">
              <label>Grade / GPA / Honors</label>
              <input
                type="text"
                value={eduForm.grade}
                onChange={(e) => setEduForm({ ...eduForm, grade: e.target.value })}
                placeholder="e.g. 3.9 / 4.0 or First Class"
              />
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="action-btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="action-btn-primary">
              Save Education
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

