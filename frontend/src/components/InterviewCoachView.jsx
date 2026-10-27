import React, { useState } from 'react';
import {
  GraduationCap,
  Sparkles,
  BookOpen,
  Plus,
  Trash2,
  CheckCircle2,
  ShieldCheck,
  AlertTriangle,
  Lightbulb,
  Building2,
  Target,
  RefreshCw,
  Search,
  Tag,
} from 'lucide-react';

export default function InterviewCoachView({
  stories = [],
  tags = [],
  profile,
  jobs = [],
  onAddStory,
  onDeleteStory,
  showToast,
}) {
  const [activeTab, setActiveTab] = useState('library'); // library | simulator
  const [selectedTag, setSelectedTag] = useState('all');
  const [searchStory, setSearchStory] = useState('');

  // Simulator state
  const [selectedRole, setSelectedRole] = useState(profile?.current_role || 'AI Engineer');
  const [selectedCompany, setSelectedCompany] = useState('');
  const [selectedJobId, setSelectedJobId] = useState('');
  const [prepResult, setPrepResult] = useState(null);
  const [isGeneratingPrep, setIsGeneratingPrep] = useState(false);

  // Add Story Modal state
  const [showAddModal, setShowAddModal] = useState(false);
  const [storyTitle, setStoryTitle] = useState('');
  const [storyCompany, setStoryCompany] = useState(profile?.current_company || 'Betopia Limited');
  const [storyRole, setStoryRole] = useState(profile?.current_role || 'AI Engineer');
  const [storySituation, setStorySituation] = useState('');
  const [storyAction, setStoryAction] = useState('');
  const [storyResult, setStoryResult] = useState('');
  const [storyTags, setStoryTags] = useState('ownership, adaptability, production systems');

  // Filtered stories
  const filteredStories = stories.filter((story) => {
    if (selectedTag !== 'all') {
      const tags = (story.good_for_tags || '').toLowerCase();
      if (!tags.includes(selectedTag.toLowerCase())) return false;
    }
    if (searchStory.trim()) {
      const q = searchStory.toLowerCase();
      const matchTitle = story.title?.toLowerCase().includes(q);
      const matchComp = story.company?.toLowerCase().includes(q);
      const matchSit = story.situation?.toLowerCase().includes(q);
      if (!matchTitle && !matchComp && !matchSit) return false;
    }
    return true;
  });

  const handleGeneratePrep = async () => {
    if (!profile?.account_id) return;
    try {
      setIsGeneratingPrep(true);
      const res = await fetch('/api/v1/interview/prep', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          account_id: profile.account_id,
          job_id: selectedJobId || undefined,
          role_title: selectedRole || undefined,
          company_name: selectedCompany || undefined,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setPrepResult(data);
        showToast('Interview prep generated and mapped to verified STAR stories!');
      } else {
        showToast('Failed to generate interview prep.', 4000);
      }
    } catch (err) {
      console.error('Interview prep generation error:', err);
      showToast('Error generating interview prep.', 4000);
    } finally {
      setIsGeneratingPrep(false);
    }
  };

  const handleCreateStorySubmit = (e) => {
    e.preventDefault();
    if (!storyTitle.trim() || !storySituation.trim() || !storyAction.trim()) {
      showToast('Please fill in title, situation, and action.', 3000);
      return;
    }
    onAddStory({
      title: storyTitle,
      company: storyCompany,
      role: storyRole,
      situation: storySituation,
      action: storyAction,
      result: storyResult,
      good_for_tags: storyTags,
      is_verified: true,
      sort_order: stories.length,
    });
    setShowAddModal(false);
    setStoryTitle('');
    setStorySituation('');
    setStoryAction('');
    setStoryResult('');
  };

  return (
    <div className="section-container interview-view">
      {/* View Header */}
      <div className="interview-header panel-card">
        <div className="interview-title-group">
          <GraduationCap className="interview-icon" />
          <div>
            <h3>STAR Interview Coach & Story Library</h3>
            <p className="interview-subtext">
              Verified career story repository and AI-assisted interview simulator mapped directly to real production achievements.
            </p>
          </div>
        </div>

        <div className="interview-tabs-switch">
          <button
            className={`sub-tab-btn ${activeTab === 'library' ? 'active' : ''}`}
            onClick={() => setActiveTab('library')}
          >
            <BookOpen className="tab-icon-sm" />
            <span>Story Library ({stories.length})</span>
          </button>
          <button
            className={`sub-tab-btn ${activeTab === 'simulator' ? 'active' : ''}`}
            onClick={() => setActiveTab('simulator')}
          >
            <Sparkles className="tab-icon-sm" />
            <span>Interview Simulator & Prep</span>
          </button>
        </div>
      </div>

      {/* TAB 1: STAR STORY LIBRARY */}
      {activeTab === 'library' && (
        <div className="story-library-wrapper">
          {/* Controls Bar */}
          <div className="library-toolbar panel-card">
            <div className="search-box">
              <Search className="search-icon" />
              <input
                type="text"
                placeholder="Search stories by topic, technology, or situation..."
                value={searchStory}
                onChange={(e) => setSearchStory(e.target.value)}
              />
            </div>

            <div className="tags-filter-group">
              <label>Filter by Tag:</label>
              <select
                value={selectedTag}
                onChange={(e) => setSelectedTag(e.target.value)}
                className="tag-select"
              >
                <option value="all">All Tags ({tags.length})</option>
                {tags.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <button
              className="action-btn-primary"
              onClick={() => setShowAddModal(true)}
            >
              <Plus className="btn-icon" />
              <span>Add Verified Story</span>
            </button>
          </div>

          {/* Stories Grid */}
          <div className="stories-grid">
            {filteredStories.map((story) => (
              <div key={story.id} className="story-card panel-card">
                <div className="story-card-header">
                  <div>
                    <h4 className="story-title">{story.title}</h4>
                    <span className="story-meta">
                      {story.company} • {story.role}
                    </span>
                  </div>
                  <div className="story-header-actions">
                    {story.is_verified && (
                      <span className="verified-badge" title="Verified against career fact ledger">
                        <CheckCircle2 className="icon-xxs" />
                        <span>Verified</span>
                      </span>
                    )}
                    <button
                      className="delete-icon-btn"
                      onClick={() => onDeleteStory(story.id)}
                      title="Delete story"
                    >
                      <Trash2 className="icon-xs" />
                    </button>
                  </div>
                </div>

                <div className="star-blocks">
                  <div className="star-block situation">
                    <span className="star-label">Situation</span>
                    <p>{story.situation}</p>
                  </div>

                  <div className="star-block action">
                    <span className="star-label">Action</span>
                    <p>{story.action}</p>
                  </div>

                  <div className="star-block result">
                    <span className="star-label">Result & Metric</span>
                    <p>{story.result}</p>
                  </div>
                </div>

                <div className="story-tags-footer">
                  <Tag className="icon-xxs" />
                  <div className="tag-pills">
                    {(story.good_for_tags || '')
                      .split(',')
                      .map((t) => t.trim())
                      .filter(Boolean)
                      .map((t) => (
                        <span key={t} className="tag-pill">
                          {t}
                        </span>
                      ))}
                  </div>
                </div>
              </div>
            ))}

            {filteredStories.length === 0 && (
              <div className="empty-state-panel panel-card">
                <GraduationCap className="empty-icon" />
                <h3>No stories match the selected criteria</h3>
                <p>Add a new production story or clear your tag filter.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 2: AI INTERVIEW SIMULATOR & PREP */}
      {activeTab === 'simulator' && (
        <div className="simulator-wrapper">
          {/* Target Role Selector */}
          <div className="simulator-controls-panel panel-card">
            <div className="controls-header">
              <Sparkles className="panel-icon" />
              <div>
                <h4>Generate Customized Interview Simulator Questions</h4>
                <p className="panel-subtext">
                  Maps technical and behavioral interview questions directly to your verified STAR stories with talking points and pitfalls to avoid.
                </p>
              </div>
            </div>

            <div className="form-grid-3">
              <div className="form-group">
                <label>Target Designation / Role</label>
                <input
                  type="text"
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value)}
                  placeholder="e.g. AI Engineer, LLM Engineer"
                />
              </div>

              <div className="form-group">
                <label>Company Name (Optional)</label>
                <input
                  type="text"
                  value={selectedCompany}
                  onChange={(e) => setSelectedCompany(e.target.value)}
                  placeholder="e.g. Anthropic, Scale AI, Betopia"
                />
              </div>

              <div className="form-group">
                <label>Or Link to Ingested Opportunity</label>
                <select
                  value={selectedJobId}
                  onChange={(e) => {
                    const id = e.target.value;
                    setSelectedJobId(id);
                    const j = jobs.find((job) => job.id === id);
                    if (j) {
                      setSelectedRole(j.title || j.role || '');
                      setSelectedCompany(j.company || '');
                    }
                  }}
                >
                  <option value="">-- Choose Ingested Job --</option>
                  {jobs.map((j) => (
                    <option key={j.id} value={j.id}>
                      {j.title || j.role} @ {j.company}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="controls-footer">
              <button
                className="action-btn-primary"
                disabled={isGeneratingPrep}
                onClick={handleGeneratePrep}
              >
                {isGeneratingPrep ? (
                  <>
                    <RefreshCw className="btn-icon icon-spin" />
                    <span>Analyzing Stories & Generating Prep...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="btn-icon" />
                    <span>Generate Interview Prep Guide</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Generated Prep Results */}
          {prepResult && (
            <div className="prep-results-container">
              {/* Advice Banner */}
              <div className="prep-advice-banner panel-card">
                <div className="advice-left">
                  <Lightbulb className="advice-icon" />
                  <div>
                    <strong>Core Interview Tone & Narrative Grounding</strong>
                    <p>{prepResult.narrative_advice}</p>
                  </div>
                </div>

                {prepResult.dealbreaker_reminder && (
                  <div className="dealbreaker-reminder-pill">
                    <ShieldCheck className="icon-xxs" />
                    <span>Dealbreaker filter: {prepResult.dealbreaker_reminder}</span>
                  </div>
                )}
              </div>

              {/* Questions List */}
              <div className="prep-questions-grid">
                {prepResult.questions.map((q, idx) => (
                  <div key={q.id || idx} className="prep-question-card panel-card">
                    <div className="question-header">
                      <span className="question-number">Question {idx + 1}</span>
                      <span className="question-category">{q.category}</span>
                    </div>

                    <h4 className="question-text">"{q.question}"</h4>

                    {/* Mapped STAR Story */}
                    {q.suggested_story_title && (
                      <div className="mapped-story-banner">
                        <CheckCircle2 className="mapped-icon" />
                        <div>
                          <span className="mapped-label">Recommended STAR Story:</span>
                          <strong className="mapped-title">{q.suggested_story_title}</strong>
                        </div>
                      </div>
                    )}

                    {/* Talking Points */}
                    <div className="talking-points-section">
                      <span className="section-label">Key Talking Points:</span>
                      <ul className="talking-points-list">
                        {q.talking_points.map((pt, pIdx) => (
                          <li key={pIdx}>{pt}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Pitfalls to Avoid */}
                    {q.pitfalls_to_avoid && (
                      <div className="pitfalls-section">
                        <AlertTriangle className="pitfall-icon" />
                        <div>
                          <strong>Trap to Avoid:</strong>
                          <p>{q.pitfalls_to_avoid}</p>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Add Story Modal */}
      {showAddModal && (
        <div className="modal-backdrop">
          <div className="modal-card panel-card">
            <div className="modal-header">
              <h3>Add Verified Production STAR Story</h3>
              <button
                className="close-modal-btn"
                onClick={() => setShowAddModal(false)}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleCreateStorySubmit} className="modal-form">
              <div className="form-group">
                <label>Story Title</label>
                <input
                  type="text"
                  placeholder="e.g. Betopia Sales Agent — end-to-end ownership"
                  value={storyTitle}
                  onChange={(e) => setStoryTitle(e.target.value)}
                  required
                />
              </div>

              <div className="form-grid-2">
                <div className="form-group">
                  <label>Company / Organization</label>
                  <input
                    type="text"
                    value={storyCompany}
                    onChange={(e) => setStoryCompany(e.target.value)}
                  />
                </div>
                <div className="form-group">
                  <label>Role</label>
                  <input
                    type="text"
                    value={storyRole}
                    onChange={(e) => setStoryRole(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Situation & Context</label>
                <textarea
                  rows={2}
                  placeholder="What was the business problem or project necessity?"
                  value={storySituation}
                  onChange={(e) => setStorySituation(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Action (Your Specific Technical Contribution)</label>
                <textarea
                  rows={3}
                  placeholder="What architecture, code, models, or systems did you design and implement?"
                  value={storyAction}
                  onChange={(e) => setStoryAction(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Result & Metrics</label>
                <textarea
                  rows={2}
                  placeholder="Production metrics: 700+ salespersons, zero downtime, sub-second latency..."
                  value={storyResult}
                  onChange={(e) => setStoryResult(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label>Tags (Comma-separated)</label>
                <input
                  type="text"
                  placeholder="ownership, learning speed, multimodal AI, LLM routing"
                  value={storyTags}
                  onChange={(e) => setStoryTags(e.target.value)}
                />
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="action-btn-secondary"
                  onClick={() => setShowAddModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="action-btn-primary">
                  Save Verified Story
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

