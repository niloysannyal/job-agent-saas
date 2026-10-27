import React from 'react';
import { Sparkles } from 'lucide-react';

export default function Toast({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="floating-toast" role="status" aria-live="polite">
      <Sparkles className="toast-icon" />
      <span className="toast-text">{message}</span>
      <button className="toast-close" onClick={onClose}>
        ×
      </button>
    </div>
  );
}
