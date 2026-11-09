import React from 'react';
import JobRadarCarousel from './JobRadarCarousel';
import TailorDiffReview from './TailorDiffReview';
import SendApprovalGate from './SendApprovalGate';
import STARStoryMatch from './STARStoryMatch';
import FunnelInsight from './FunnelInsight';

const WIDGETS = {
  JobRadarCarousel,
  TailorDiffReview,
  SendApprovalGate,
  STARStoryMatch,
  FunnelInsight,
};

export default function RenderWidget({ widget }) {
  if (!widget || !widget.type) return null;

  const Component = WIDGETS[widget.type];
  if (!Component) {
    return (
      <div className="agent-widget unknown-widget">
        <span className="text-muted">Interactive Card: {widget.type}</span>
      </div>
    );
  }

  return <Component props={widget.props} actions={widget.actions} />;
}
