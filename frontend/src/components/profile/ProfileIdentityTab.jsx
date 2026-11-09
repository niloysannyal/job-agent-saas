import React from 'react';
import { Save } from 'lucide-react';

export default function ProfileIdentityTab({
  profileForm,
  handleFieldChange,
  onSaveProfile,
  isSaving,
}) {
  return (
    <form onSubmit={onSaveProfile} className="profile-form panel-card">
      <div className="panel-header">
        <h3>Candidate Identity & Executive Contact</h3>
        <button type="submit" disabled={isSaving} className="action-btn-primary">
          <Save className="btn-icon" />
          <span>{isSaving ? 'Saving...' : 'Save Identity'}</span>
        </button>
      </div>

      <div className="form-grid-2">
        <div className="form-group">
          <label>Full Name *</label>
          <input
            type="text"
            name="full_name"
            value={profileForm.full_name || ''}
            onChange={handleFieldChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Professional Headline *</label>
          <input
            type="text"
            name="headline"
            value={profileForm.headline || ''}
            onChange={handleFieldChange}
            placeholder="e.g. Senior Backend Engineer | Distributed Systems"
          />
        </div>
      </div>

      <div className="form-grid-2">
        <div className="form-group">
          <label>Current Role / Title</label>
          <input
            type="text"
            name="current_role"
            value={profileForm.current_role || ''}
            onChange={handleFieldChange}
          />
        </div>
        <div className="form-group">
          <label>Current Organization / Company</label>
          <input
            type="text"
            name="current_company"
            value={profileForm.current_company || ''}
            onChange={handleFieldChange}
          />
        </div>
      </div>

      <div className="form-grid-3">
        <div className="form-group">
          <label>Phone / WhatsApp</label>
          <input
            type="text"
            name="phone"
            value={profileForm.phone || ''}
            onChange={handleFieldChange}
            placeholder="+1 555-0199"
          />
        </div>
        <div className="form-group">
          <label>City</label>
          <input
            type="text"
            name="location_city"
            value={profileForm.location_city || ''}
            onChange={handleFieldChange}
          />
        </div>
        <div className="form-group">
          <label>Country</label>
          <input
            type="text"
            name="location_country"
            value={profileForm.location_country || ''}
            onChange={handleFieldChange}
          />
        </div>
      </div>

      <div className="form-grid-3">
        <div className="form-group">
          <label>LinkedIn URL</label>
          <input
            type="text"
            name="linkedin_url"
            value={profileForm.linkedin_url || ''}
            onChange={handleFieldChange}
          />
        </div>
        <div className="form-group">
          <label>GitHub URL</label>
          <input
            type="text"
            name="github_url"
            value={profileForm.github_url || ''}
            onChange={handleFieldChange}
          />
        </div>
        <div className="form-group">
          <label>Portfolio / Personal Website</label>
          <input
            type="text"
            name="portfolio_url"
            value={profileForm.portfolio_url || ''}
            onChange={handleFieldChange}
            placeholder="https://yourportfolio.com"
          />
        </div>
      </div>

      <div className="form-group">
        <label>Executive Career Summary</label>
        <textarea
          name="summary"
          rows={4}
          value={profileForm.summary || ''}
          onChange={handleFieldChange}
          placeholder="Concise 2-4 sentence executive narrative of your experience, ownership, and engineering impact..."
        />
      </div>
    </form>
  );
}

