import React from 'react';
import { Mic, Award, Target, Zap, CheckCircle2 } from 'lucide-react';
import { useAgent } from '../../../hooks/useAgent';

export default function STARStoryMatch({ props }) {
  const { sendMessage } = useAgent();
  const {
    question,
    story_title,
    good_for_tags,
    situation,
    action,
    result,
    job_title,
    company,
  } = props || {};

  const handleNextQuestion = () => {
    sendMessage(`Ask me a follow-up behavioral question about: ${story_title}`, {
      story_title,
      job_title,
      company,
    });
  };

  return (
    <div className="agent-widget star-story-match">
      <div className="widget-header">
        <div className="widget-title-group">
          <Mic size={16} className="text-emerald" />
          <span className="widget-title">STAR Interview Coach Match</span>
        </div>
        <span className="widget-badge">Story Bank</span>
      </div>

      {question && (
        <div className="interview-question-box">
          <div className="q-label">Simulated Question:</div>
          <div className="q-text">"{question}"</div>
        </div>
      )}

      <div className="story-card-wrapper">
        <div className="story-title-row">
          <Award size={15} className="text-emerald" />
          <span className="story-title">{story_title}</span>
        </div>

        {good_for_tags && (
          <div className="story-tags-row">
            {good_for_tags.split(',').map((tag, i) => (
              <span key={i} className="story-tag">{tag.trim()}</span>
            ))}
          </div>
        )}

        <div className="star-breakdown">
          {situation && (
            <div className="star-phase-item">
              <span className="phase-letter letter-s">S/T</span>
              <div className="phase-desc">{situation}</div>
            </div>
          )}
          {action && (
            <div className="star-phase-item">
              <span className="phase-letter letter-a">A</span>
              <div className="phase-desc">{action}</div>
            </div>
          )}
          {result && (
            <div className="star-phase-item">
              <span className="phase-letter letter-r">R</span>
              <div className="phase-desc">{result}</div>
            </div>
          )}
        </div>
      </div>

      <div className="widget-footer-action">
        <button
          type="button"
          className="btn-outline-action"
          onClick={handleNextQuestion}
        >
          <Zap size={13} />
          <span>Practice Follow-Up Question</span>
        </button>
      </div>
    </div>
  );
}
