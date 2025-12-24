/**
 * ReportTabs Component - Tabbed report sections with smooth transitions
 * Per FR-011: System MUST organize detailed findings into tabbed sections
 */

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './ReportTabs.css';

export function ReportTabs({ sections = [], activeTab = 0, onTabChange }) {
    const [selectedTab, setSelectedTab] = useState(activeTab);
    const [indicatorStyle, setIndicatorStyle] = useState({});
    const tabRefs = useRef([]);

    // Update indicator position on tab change
    useEffect(() => {
        const activeTabEl = tabRefs.current[selectedTab];
        if (activeTabEl) {
            setIndicatorStyle({
                width: activeTabEl.offsetWidth,
                left: activeTabEl.offsetLeft,
            });
        }
    }, [selectedTab, sections]);

    const handleTabClick = (index) => {
        setSelectedTab(index);
        onTabChange?.(index);
    };

    if (!sections.length) {
        return (
            <div className="report-tabs report-tabs--empty">
                <p className="report-tabs__placeholder">
                    Report sections will appear here once analysis is complete.
                </p>
            </div>
        );
    }

    return (
        <div className="report-tabs">
            {/* Tab Navigation */}
            <div className="report-tabs__nav" role="tablist">
                {sections.map((section, index) => (
                    <button
                        key={section.id || index}
                        ref={(el) => (tabRefs.current[index] = el)}
                        role="tab"
                        aria-selected={selectedTab === index}
                        aria-controls={`panel-${section.id || index}`}
                        className={`report-tabs__tab ${selectedTab === index ? 'report-tabs__tab--active' : ''}`}
                        onClick={() => handleTabClick(index)}
                    >
                        <span className="report-tabs__tab-label">{section.title}</span>
                        {section.word_count && (
                            <span className="report-tabs__tab-badge">
                                {section.word_count.toLocaleString()} words
                            </span>
                        )}
                    </button>
                ))}

                {/* Animated indicator */}
                <motion.div
                    className="report-tabs__indicator"
                    animate={indicatorStyle}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                />
            </div>

            {/* Tab Panels */}
            <div className="report-tabs__panels">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={selectedTab}
                        role="tabpanel"
                        id={`panel-${sections[selectedTab]?.id || selectedTab}`}
                        className="report-tabs__panel"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.2 }}
                    >
                        <div className="report-tabs__panel-header">
                            <h3 className="report-tabs__section-title">
                                {sections[selectedTab]?.title}
                            </h3>
                            <div className="report-tabs__section-meta">
                                <span className="report-tabs__category">
                                    {sections[selectedTab]?.category}
                                </span>
                                {sections[selectedTab]?.citation_ids?.length > 0 && (
                                    <span className="report-tabs__citations">
                                        {sections[selectedTab].citation_ids.length} sources
                                    </span>
                                )}
                            </div>
                        </div>

                        <div
                            className="report-tabs__content"
                            dangerouslySetInnerHTML={{
                                __html: formatContent(sections[selectedTab]?.content)
                            }}
                        />
                    </motion.div>
                </AnimatePresence>
            </div>
        </div>
    );
}

// Helper to format content with citation markers
function formatContent(content) {
    if (!content) return '';

    // Convert [cite:ID] markers to clickable citations
    return content.replace(
        /\[cite:([^\]]+)\]/g,
        '<sup class="report-tabs__cite" data-cite-id="$1">[$1]</sup>'
    );
}

export default ReportTabs;
