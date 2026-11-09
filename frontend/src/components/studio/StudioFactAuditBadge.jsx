import React from 'react';
import { CheckCircle2, ShieldCheck, AlertTriangle } from 'lucide-react';

export default function StudioFactAuditBadge({
  factCount = 0,
  atsParsable = true,
  hasWarnings = false,
  warningMessage = '',
}) {
  return (
    <div className="audit-badges-group">
      <span className={`audit-badge ${hasWarnings ? 'warning' : 'pass'}`} title={warningMessage || 'All claims verified against canonical Fact Ledger'}>
        {hasWarnings ? (
          <AlertTriangle className="icon-xxs text-amber" />
        ) : (
          <CheckCircle2 className="icon-xxs" />
        )}
        <span>{hasWarnings ? 'Fact Review Needed' : 'Verified Fact Audit: Passed'}</span>
      </span>
      {atsParsable && (
        <span className="audit-badge ats" title="LaTeX compiles to pure selectable text layer without vector rasterization">
          <ShieldCheck className="icon-xxs" />
          <span>ATS Text-Layer: 100% Parsable</span>
        </span>
      )}
      {factCount > 0 && (
        <span className="audit-badge info" title="Canonical facts anchored to profile">
          <span>{factCount} Verified Citations</span>
        </span>
      )}
    </div>
  );
}

