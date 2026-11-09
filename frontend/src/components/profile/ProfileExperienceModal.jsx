import React from 'react';
import { X } from 'lucide-react';

export default function ProfileExperienceModal({
  isOpen,
  onClose,
  editingExp,
  expForm,
  setExpForm,
  handleSaveExp,
}) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="modal-content modal-medium">
        <div className="modal-header">
          <h3>{editingExp ? 'Edit Work Experience' : 'Add Work Experience'}</h3>
          <button className="btn-icon-close" onClick={onClose}>
            <X size={18} />
          </button>
        </div>
        <form onSubmit={handleSaveExp} className="modal-form">
          <div className="form-grid-2">
            <div className="form-group">
              <label>Job Title *</label>
              <input
                type="text"
                value={expForm.title}
                onChange={(e) => setExpForm({ ...expForm, title: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Company / Organization *</label>
              <input
                type="text"
                value={expForm.company}
                onChange={(e) => setExpForm({ ...expForm, company: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={expForm.location}
                onChange={(e) => setExpForm({ ...expForm, location: e.target.value })}
                placeholder="e.g. London, UK"
              />
            </div>
            <div className="form-group">
              <label>Workplace Mode</label>
              <select
                value={expForm.location_type}
                onChange={(e) => setExpForm({ ...expForm, location_type: e.target.value })}
              >
                <option value="onsite">On-site</option>
                <option value="remote">Remote</option>
                <option value="hybrid">Hybrid</option>
              </select>
            </div>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Start Date *</label>
              <input
                type="text"
                value={expForm.start_date}
                onChange={(e) => setExpForm({ ...expForm, start_date: e.target.value })}
                placeholder="e.g. 2022-01 or Jan 2022"
                required
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="text"
                value={expForm.end_date}
                onChange={(e) => setExpForm({ ...expForm, end_date: e.target.value })}
                placeholder="e.g. 2024-05 (leave blank if current)"
                disabled={expForm.is_current}
              />
              <label className="checkbox-inline">
                <input
                  type="checkbox"
                  checked={expForm.is_current}
                  onChange={(e) => setExpForm({ ...expForm, is_current: e.target.checked })}
                />
                I currently work here
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>Key Accomplishments & Bullet Points (one per line)</label>
            <textarea
              rows={4}
              value={expForm.highlights}
              onChange={(e) => setExpForm({ ...expForm, highlights: e.target.value })}
              placeholder="&bull; Architected distributed caching layer saving $50k/mo&#10;&bull; Led a squad of 4 engineers delivering payments API"
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="action-btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="action-btn-primary">
              Save Position
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

