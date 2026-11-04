import React from 'react';
import { FolderGit2, Plus, Edit2, Trash2, ExternalLink, GitBranch } from 'lucide-react';

export default function ProfileProjectsTab({
  profile,
  handleOpenAddProj,
  handleOpenEditProj,
  handleDeleteProj,
}) {
  return (
    <div className="panel-card">
      <div className="panel-header">
        <div>
          <h3>Featured Projects & Deliverables</h3>
          <p className="subtext">Portfolio projects, open-source repositories, and key engineering systems.</p>
        </div>
        <button className="action-btn-primary" onClick={handleOpenAddProj}>
          <Plus size={16} /> Add Project
        </button>
      </div>

      <div className="projects-list">
        {(!profile?.projects || profile.projects.length === 0) ? (
          <div className="empty-panel-state">
            <FolderGit2 size={36} className="dim-icon" />
            <h4>No projects recorded yet</h4>
            <p>Click "Add Project" above to highlight open-source repositories, client deliverables, or portfolio systems.</p>
          </div>
        ) : (
          profile.projects.map((proj) => (
            <div key={proj.id} className="career-card">
              <div className="career-card-header">
                <div>
                  <div className="role-company-line">
                    <h4 className="card-title">{proj.title}</h4>
                    {proj.role && (
                      <>
                        <span className="card-at">as</span>
                        <h4 className="card-company">{proj.role}</h4>
                      </>
                    )}
                    {proj.end_date === 'Present' && <span className="badge-active">Ongoing</span>}
                  </div>

                  <div className="card-meta">
                    <span>{proj.start_date || 'Project'} -- {proj.end_date || 'Completed'}</span>
                  </div>

                  {/* Project Links (Live Demo + GitHub) */}
                  <div className="project-links-row">
                    {proj.url && (
                      <a
                        href={proj.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="project-link-badge"
                        title="Open live project"
                      >
                        <ExternalLink size={12} />
                        <span>Live Demo</span>
                      </a>
                    )}
                    {proj.github_url && (
                      <a
                        href={proj.github_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="project-link-badge"
                        title="Open GitHub repository"
                      >
                        <GitBranch size={12} />
                        <span>GitHub Repo</span>
                      </a>
                    )}
                  </div>

                  {/* Tech stack badges */}
                  {proj.technologies && (
                    <div className="tech-stack-row">
                      {proj.technologies.split(',').map((tech, tIdx) => (
                        <span key={tIdx} className="tech-stack-badge">
                          {tech.trim()}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="card-actions">
                  <button className="btn-icon-subtle" title="Edit Project" onClick={() => handleOpenEditProj(proj)}>
                    <Edit2 size={15} />
                  </button>
                  <button className="btn-icon-danger" title="Remove Project" onClick={() => handleDeleteProj(proj.id)}>
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>

              {proj.description && <p className="card-desc">{proj.description}</p>}

              {proj.highlights && (
                <ul className="card-highlights">
                  {(typeof proj.highlights === 'string' && proj.highlights.startsWith('[')
                    ? JSON.parse(proj.highlights)
                    : proj.highlights.split('\n')
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

