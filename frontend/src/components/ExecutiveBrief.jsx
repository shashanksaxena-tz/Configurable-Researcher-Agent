/**
 * ExecutiveBrief Component - 1-minute summary view
 * Per FR-010: System MUST render an executive brief (1-minute natural language summary)
 */

import React from 'react';
import './ExecutiveBrief.css';

export function ExecutiveBrief({ summary, wordCount, readTimeMinutes = 1, className = '' }) {
    if (!summary) {
        return (
            <div className={`executive-brief executive-brief--empty ${className}`}>
                <div className="executive-brief__placeholder">
                    <span className="executive-brief__placeholder-icon">📊</span>
                    <p>Executive summary will appear here once research is complete.</p>
                </div>
            </div>
        );
    }

    return (
        <article className={`executive-brief ${className}`}>
            <header className="executive-brief__header">
                <h2 className="executive-brief__title">Executive Brief</h2>
                <div className="executive-brief__meta">
                    <span className="executive-brief__read-time">
                        <svg className="executive-brief__icon" viewBox="0 0 24 24" width="16" height="16">
                            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
                            <path d="M12 6v6l4 2" stroke="currentColor" strokeWidth="2" fill="none" />
                        </svg>
                        {readTimeMinutes} min read
                    </span>
                    {wordCount && (
                        <span className="executive-brief__word-count">
                            {wordCount.toLocaleString()} words
                        </span>
                    )}
                </div>
            </header>

            <div className="executive-brief__content">
                <p className="executive-brief__summary">{summary}</p>
            </div>

            <div className="executive-brief__gradient-bar" aria-hidden="true" />
        </article>
    );
}

export default ExecutiveBrief;
