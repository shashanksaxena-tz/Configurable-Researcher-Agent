/**
 * CitationTooltip Component - Inline citation with source details
 * Per FR-012: System MUST render claims with clickable inline citations
 */

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './CitationTooltip.css';

export function CitationTooltip({
    citationId,
    sourceUrl,
    sourceTitle,
    extractionTimestamp,
    excerpt,
    children,
    className = ''
}) {
    const [isOpen, setIsOpen] = useState(false);
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const triggerRef = useRef(null);
    const tooltipRef = useRef(null);

    // Calculate tooltip position
    useEffect(() => {
        if (isOpen && triggerRef.current) {
            const rect = triggerRef.current.getBoundingClientRect();
            setPosition({
                x: rect.left + rect.width / 2,
                y: rect.bottom + 8
            });
        }
    }, [isOpen]);

    // Close on click outside
    useEffect(() => {
        const handleClickOutside = (e) => {
            if (tooltipRef.current && !tooltipRef.current.contains(e.target) &&
                triggerRef.current && !triggerRef.current.contains(e.target)) {
                setIsOpen(false);
            }
        };

        if (isOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        }
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen]);

    const formattedDate = extractionTimestamp
        ? new Date(extractionTimestamp).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
        : 'Unknown';

    return (
        <>
            <span
                ref={triggerRef}
                className={`citation-tooltip__trigger ${className}`}
                onClick={() => setIsOpen(!isOpen)}
                role="button"
                aria-expanded={isOpen}
                aria-haspopup="true"
                tabIndex={0}
                onKeyDown={(e) => e.key === 'Enter' && setIsOpen(!isOpen)}
            >
                {children || `[${citationId}]`}
            </span>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        ref={tooltipRef}
                        className="citation-tooltip__popup"
                        style={{
                            position: 'fixed',
                            left: position.x,
                            top: position.y,
                            transform: 'translateX(-50%)'
                        }}
                        initial={{ opacity: 0, y: -10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -10, scale: 0.95 }}
                        transition={{ duration: 0.15 }}
                    >
                        <div className="citation-tooltip__arrow" />

                        <div className="citation-tooltip__header">
                            <span className="citation-tooltip__badge">Source</span>
                            <button
                                className="citation-tooltip__close"
                                onClick={() => setIsOpen(false)}
                                aria-label="Close"
                            >
                                ×
                            </button>
                        </div>

                        <h4 className="citation-tooltip__title">{sourceTitle || 'Unknown Source'}</h4>

                        {excerpt && (
                            <p className="citation-tooltip__excerpt">"{excerpt}"</p>
                        )}

                        <div className="citation-tooltip__meta">
                            <span className="citation-tooltip__timestamp">
                                Extracted: {formattedDate}
                            </span>
                        </div>

                        <a
                            href={sourceUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="citation-tooltip__link"
                        >
                            View Original Source →
                        </a>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
}

export default CitationTooltip;
