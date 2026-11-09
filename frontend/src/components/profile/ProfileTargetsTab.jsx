import React from 'react';
import { Plus, Trash2, MapPin, Wifi, Building2, Globe } from 'lucide-react';

const WORKPLACE_LABELS = {
  remote: 'Remote',
  hybrid: 'Hybrid',
  onsite: 'On-site',
  any: 'Any Mode',
};

export default function ProfileTargetsTab({
  targetDesignations = [],
  newRole,
  setNewRole,
  onAddDesignation,
  onDeleteDesignation,
  targetLocations = [],
  newLocationName,
  setNewLocationName,
  newLocationType,
  setNewLocationType,
  newRelocation,
  setNewRelocation,
  onAddLocation,
  onDeleteLocation,
}) {
  return (
    <div className="targets-section-grid">
      {/* Target Roles */}
      <div className="panel-card">
        <div className="panel-header">
          <h3>Target Job Roles</h3>
        </div>
        <p className="subtext">Ranked order of target roles. Higher priority roles receive higher search weighting.</p>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (newRole.trim()) {
              onAddDesignation(newRole.trim(), targetDesignations.length);
              setNewRole('');
            }
          }}
          className="add-subrecord-form"
        >
          <input
            type="text"
            placeholder="e.g. Senior Backend Engineer"
            value={newRole}
            onChange={(e) => setNewRole(e.target.value)}
          />
          <button type="submit" className="action-btn-primary">
            <Plus size={16} /> Add Role
          </button>
        </form>

        <div className="subrecord-list">
          {targetDesignations.length === 0 ? (
            <div className="subrecord-empty-state">
              <span>No target roles added yet. Add your preferred job titles above.</span>
            </div>
          ) : (
            targetDesignations.map((desig, idx) => (
              <div key={desig.id || idx} className="subrecord-item">
                <div className="subrecord-left">
                  <span className="rank-badge">#{idx + 1}</span>
                  <span className="item-title">{desig.title}</span>
                </div>
                <button
                  className="btn-icon-danger"
                  title="Remove Role"
                  onClick={() => onDeleteDesignation(desig.id)}
                >
                  <Trash2 size={15} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Workplace Modes & Locations */}
      <div className="panel-card">
        <div className="panel-header">
          <h3>Target Locations & Work Modes</h3>
        </div>
        <p className="subtext">Define locations and whether you prefer Remote, Hybrid, or On-site.</p>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (newLocationName.trim()) {
              onAddLocation(newLocationName.trim(), newLocationType, newRelocation);
              setNewLocationName('');
            }
          }}
          className="add-subrecord-form"
        >
          <input
            type="text"
            placeholder="e.g. London, United Kingdom or Remote"
            value={newLocationName}
            onChange={(e) => setNewLocationName(e.target.value)}
          />
          <select
            value={newLocationType}
            onChange={(e) => setNewLocationType(e.target.value)}
          >
            <option value="remote">Remote</option>
            <option value="hybrid">Hybrid</option>
            <option value="onsite">On-site</option>
            <option value="any">Any Mode</option>
          </select>
          <button type="submit" className="action-btn-primary">
            <Plus size={16} /> Add Location
          </button>
        </form>

        <div className="subrecord-list">
          {targetLocations.length === 0 ? (
            <div className="subrecord-empty-state">
              <span>No target locations added yet. Add your target cities or remote preferences above.</span>
            </div>
          ) : (
            targetLocations.map((loc) => (
              <div key={loc.id} className="subrecord-item">
                <div className="subrecord-left">
                  <MapPin size={15} className="subrecord-pin-icon" />
                  <span className="item-title">{loc.location_name}</span>
                </div>
                <div className="subrecord-actions">
                  <span className={`workplace-badge badge-${loc.location_type}`}>
                    {loc.location_type === 'remote' ? (
                      <Wifi size={11} />
                    ) : loc.location_type === 'hybrid' ? (
                      <Building2 size={11} />
                    ) : loc.location_type === 'onsite' ? (
                      <MapPin size={11} />
                    ) : (
                      <Globe size={11} />
                    )}
                    <span>{WORKPLACE_LABELS[loc.location_type] || loc.location_type}</span>
                  </span>
                  <button
                    className="btn-icon-danger"
                    title="Remove Location"
                    onClick={() => onDeleteLocation(loc.id)}
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

