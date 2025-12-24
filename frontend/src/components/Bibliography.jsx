/**
 * Bibliography Component - Complete source list for reports
 * Per FR-013: System MUST provide complete bibliography/source list with all references
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import './Bibliography.css';

export function Bibliography({ citations = [], className = '' }) {
    const [sortBy, setSortBy] = useState('relevance'); // relevance, date, source
    const [expandedId, setExpandedId] = useState(null);

    if (!citations.length) {
        return (
            <div className={`bibliography bibliography--empty ${className}`}>
                <p>No sources to display.</p>
            </div>
        );
    }

    const sortedCitations = [...citations].sort((a, b) => {
        if (sortBy === 'date') {
            return new Date(b.timestamp || 0) - new Date(a.timestamp || 0);
        }
        if (sortBy === 'source') {
            return (a.source_title || '').localeCompare(b.source_title || '');
        }
        // Default: by relevance (order in array)
        return 0;
    });

    return (
        <section className={`bibliography ${className}`}>
            <header className="bibliography__header">
                <h3 className="bibliography__title">
                    📚 Sources & References
                    <span className="bibliography__count">{citations.length} sources</span>
                </h3>

                <div className="bibliography__controls">
                    <label className="bibliography__sort-label">Sort by:</label>
                    <select
                        className="bibliography__sort-select"
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value)}
                    >
                        <option value="relevance">Relevance</option>
                        <option value="date">Date</option>
                        <option value="source">Source Name</option>
                    </select>
                </div>
            </header>

            <ul className="bibliography__list">
                {sortedCitations.map((citation, index) => (
                    <motion.li
                        key={citation.id || index}
                        className="bibliography__item"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                    >
                        <div
                            className="bibliography__item-header"
                            onClick={() => setExpandedId(expandedId === citation.id ? null : citation.id)}
                        >
                            <span className="bibliography__index">[{index + 1}]</span>
                            <div className="bibliography__item-main">
                                <h4 className="bibliography__source-title">
                                    {citation.source_title || 'Unknown Source'}
                                </h4>
                                <a
                                    href={citation.source_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="bibliography__url"
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    {truncateUrl(citation.source_url)}
                                </a>
                            </div>
                            <span className="bibliography__expand-icon">
                                {expandedId === citation.id ? '−' : '+'}
                            </span>
                        </div>

                        {expandedId === citation.id && (
                            <motion.div
                                className="bibliography__item-details"
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                            >
                                {citation.excerpt && (
                                    <blockquote className="bibliography__excerpt">
                                        "{citation.excerpt}"
                                    </blockquote>
                                )}
                                <div className="bibliography__meta">
                                    {citation.timestamp && (
                                        <span>Accessed: {formatDate(citation.timestamp)}</span>
                                    )}
                                    {citation.confidence && (
                                        <span>Confidence: {Math.round(citation.confidence * 100)}%</span>
                                    )}
                                </div>
                            </motion.div>
                        )}
                    </motion.li>
                ))}
            </ul>
        </section>
    );
}

function truncateUrl(url, maxLength = 50) {
    if (!url) return '';
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

export default Bibliography;
