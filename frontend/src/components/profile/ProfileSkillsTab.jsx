import React from 'react';
import { Plus, X } from 'lucide-react';

export default function ProfileSkillsTab({
  profile,
  newSkillName,
  setNewSkillName,
  newSkillCategory,
  setNewSkillCategory,
  newSkillProficiency,
  setNewSkillProficiency,
  handleAddSkill,
  handleDeleteSkill,
}) {
  return (
    <div className="panel-card">
      <div className="panel-header">
        <div>
          <h3>Skills & Competencies</h3>
          <p className="subtext">Categorized technical and professional skills matched during job searches.</p>
        </div>
      </div>

      {/* Add skill form with aligned height and tokens */}
      <form onSubmit={handleAddSkill} className="add-subrecord-form">
        <input
          type="text"
          placeholder="e.g. Python, Docker, Financial Modeling..."
          value={newSkillName}
          onChange={(e) => setNewSkillName(e.target.value)}
          required
        />
        <select
          value={newSkillCategory}
          onChange={(e) => setNewSkillCategory(e.target.value)}
        >
          <option value="Languages">Languages</option>
          <option value="Frameworks">Frameworks & Libraries</option>
          <option value="Cloud & DevOps">Cloud & DevOps</option>
          <option value="Databases">Databases & Storage</option>
          <option value="Tools">Tools & Systems</option>
          <option value="Management">Management & Leadership</option>
          <option value="Soft Skills">Soft Skills & Communication</option>
        </select>
        <select
          value={newSkillProficiency}
          onChange={(e) => setNewSkillProficiency(e.target.value)}
        >
          <option value="Beginner">Beginner</option>
          <option value="Intermediate">Intermediate</option>
          <option value="Advanced">Advanced</option>
          <option value="Expert">Expert</option>
        </select>
        <button type="submit" className="action-btn-primary">
          <Plus size={16} /> Add Skill
        </button>
      </form>

      {/* Grouped Skills */}
      <div className="skills-categories-grid">
        {['Languages', 'Frameworks', 'Cloud & DevOps', 'Databases', 'Tools', 'Management', 'Soft Skills'].map((cat) => {
          const catSkills = (profile?.skills || []).filter((s) => s.category === cat);
          if (catSkills.length === 0) return null;
          return (
            <div key={cat} className="skill-category-box">
              <h4 className="category-title">{cat}</h4>
              <div className="skill-chips-row">
                {catSkills.map((s) => (
                  <span key={s.id} className="skill-chip">
                    <span className="skill-chip-name">{s.name}</span>
                    <span className="skill-chip-level">{s.proficiency}</span>
                    <button
                      type="button"
                      className="chip-remove"
                      title="Remove skill"
                      onClick={() => handleDeleteSkill(s.id)}
                    >
                      <X size={12} />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

