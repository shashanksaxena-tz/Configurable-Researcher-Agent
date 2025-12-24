/**
 * DiscrepancyPanel Component - Display conflicting source information
 * Per FR-009: System MUST handle conflicting info with all sources cited
 * Per SC-003: For conflicts, MUST present all conflicting claims with sources
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './DiscrepancyPanel.css';

export function DiscrepancyPanel({ discrepancies = [], className = '' }) {
    const [expandedIndex, setExpandedIndex] = useState(null);

    if (!discrepancies.length) {
        return null; // Don't render if no discrepancies
    }

    return (
        <aside className={`discrepancy-panel ${className}`}>
            <header className="discrepancy-panel__header">
                <span className="discrepancy-panel__icon">⚠️</span>
                <div>
                    <h3 className="discrepancy-panel__title">Source Discrepancies</h3>
                    <p className="discrepancy-panel__subtitle">
                        {discrepancies.length} conflicting claim{discrepancies.length > 1 ? 's' : ''} detected
                    </p>
                </div>
            </header>

            <ul className="discrepancy-panel__list">
                {discrepancies.map((disc, index) => (
                    <li key={disc.id || index} className="discrepancy-panel__item">
                        <button
                            className="discrepancy-panel__item-header"
                            onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
                            aria-expanded={expandedIndex === index}
                        >
                            <span className="discrepancy-panel__topic">{disc.topic}</span>
                            <span className="discrepancy-panel__toggle">
                                {expandedIndex === index ? '▼' : '▶'}
                            </span>
                        </button>

                        <AnimatePresence>
                            {expandedIndex === index && (
                                <motion.div
                                    className="discrepancy-panel__details"
                                    initial={{ height: 0, opacity: 0 }}
                                    animate={{ height: 'auto', opacity: 1 }}
                                    exit={{ height: 0, opacity: 0 }}
                                    transition={{ duration: 0.2 }}
                                >
                                    <div className="discrepancy-panel__claims">
                                        {disc.conflicting_claims?.map((claim, cIndex) => (
                                            <div key={cIndex} className="discrepancy-panel__claim">
                                                <div className="discrepancy-panel__claim-text">
                                                    "{claim.claim || claim.text}"
                                                </div>
                                                <a
                                                    href={claim.source_url}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="discrepancy-panel__claim-source"
                                                >
                                                    {claim.source_title || claim.source_url}
                                                </a>
                                            </div>
                                        ))}
                                    </div>

                                    {disc.resolution_notes && (
                                        <div className="discrepancy-panel__resolution">
                                            <strong>Resolution:</strong> {disc.resolution_notes}
                                            {disc.resolution_basis && (
                                                <span className="discrepancy-panel__basis">
                                                    (Based on: {disc.resolution_basis})
                                                </span>
                                            )}
                                        </div>
                                    )}

                                    {disc.preferred_claim && (
                                        <div className="discrepancy-panel__preferred">
                                            <span className="discrepancy-panel__preferred-label">Preferred:</span>
                                            "{disc.preferred_claim}"
                                        </div>
                                    )}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </li>
                ))}
            </ul>
        </aside>
    );
}

export default DiscrepancyPanel;
