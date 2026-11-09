import React from 'react';
import { X } from 'lucide-react';

export default function ProfileProjectModal({
  isOpen,
  onClose,
  editingProj,
  projForm,
  setProjForm,
  handleSaveProj,
}) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="modal-content modal-medium">
        <div className="modal-header">
          <h3>{editingProj ? 'Edit Project' : 'Add Project'}</h3>
          <button className="btn-icon-close" onClick={onClose}>
            <X size={18} />
          </button>
        </div>
        <form onSubmit={handleSaveProj} className="modal-form">
          <div className="form-grid-2">
            <div className="form-group">
              <label>Project Name *</label>
              <input
                type="text"
                value={projForm.title}
                onChange={(e) => setProjForm({ ...projForm, title: e.target.value })}
                placeholder="e.g. Full Send Sports AI"
                required
              />
            </div>
            <div className="form-group">
              <label>Role / Ownership</label>
              <input
                type="text"
                value={projForm.role}
                onChange={(e) => setProjForm({ ...projForm, role: e.target.value })}
                placeholder="e.g. Creator & Lead Architect"
              />
            </div>
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Live Link / Demo URL</label>
              <input
                type="url"
                value={projForm.url}
                onChange={(e) => setProjForm({ ...projForm, url: e.target.value })}
                placeholder="https://example.com/demo"
              />
            </div>
            <div className="form-group">
              <label>GitHub Repository URL</label>
              <input
                type="url"
                value={projForm.github_url}
                onChange={(e) => setProjForm({ ...projForm, github_url: e.target.value })}
                placeholder="https://github.com/user/project"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Tech Stack (comma-separated)</label>
            <input
              type="text"
              value={projForm.technologies}
              onChange={(e) => setProjForm({ ...projForm, technologies: e.target.value })}
              placeholder="e.g. Python, FastAPI, React 19, PostgreSQL, Docker, AWS"
            />
          </div>

          <div className="form-grid-2">
            <div className="form-group">
              <label>Start Date</label>
              <input
                type="text"
                value={projForm.start_date}
                onChange={(e) => setProjForm({ ...projForm, start_date: e.target.value })}
                placeholder="e.g. 2024-01 or Jan 2024"
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="text"
                value={projForm.end_date}
                onChange={(e) => setProjForm({ ...projForm, end_date: e.target.value })}
                placeholder="e.g. 2024-06"
                disabled={projForm.is_current}
              />
              <label className="checkbox-inline">
                <input
                  type="checkbox"
                  checked={projForm.is_current}
                  onChange={(e) => setProjForm({ ...projForm, is_current: e.target.checked })}
                />
                Ongoing project
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>Project Description</label>
            <textarea
              rows={2}
              value={projForm.description}
              onChange={(e) => setProjForm({ ...projForm, description: e.target.value })}
              placeholder="Summary of the project's purpose, architecture, and engineering scale..."
            />
          </div>

          <div className="form-group">
            <label>Key Highlights & Accomplishments (one bullet per line)</label>
            <textarea
              rows={3}
              value={projForm.highlights}
              onChange={(e) => setProjForm({ ...projForm, highlights: e.target.value })}
              placeholder="&bull; Trained ensemble XGBoost pipeline on 10k+ records with sub-100ms latency&#10;&bull; Deployed on AWS with high-availability autoscaling"
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="action-btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="action-btn-primary">
              Save Project
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

