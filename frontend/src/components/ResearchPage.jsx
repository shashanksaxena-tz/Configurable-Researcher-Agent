/**
 * ResearchPage Component - Main research interface
 * Integrates SearchInput, ProgressIndicator, ExecutiveBrief, and ReportTabs
 */

import React, { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useResearch } from '../contexts/ResearchContext';
import { SearchInput } from './SearchInput';
import { ProgressIndicator } from './ProgressIndicator';
import { ExecutiveBrief } from './ExecutiveBrief';
import { ReportTabs } from './ReportTabs';
import './ResearchPage.css';

export function ResearchPage() {
    const {
        status,
        progress,
        currentStage,
        questionsCompleted,
        questionsTotal,
        report,
        isLoading,
        isResearching,
        isComplete,
        hasError,
        error,
        startResearch,
        pollStatus,
        fetchReport,
        requestId,
        reset
    } = useResearch();

    const pollIntervalRef = useRef(null);

    // Poll for status when researching
    useEffect(() => {
        if (isResearching && requestId) {
            pollIntervalRef.current = setInterval(() => {
                pollStatus(requestId);
            }, 2000); // Poll every 2 seconds
        }

        return () => {
            if (pollIntervalRef.current) {
                clearInterval(pollIntervalRef.current);
            }
        };
    }, [isResearching, requestId, pollStatus]);

    // Fetch report when complete
    useEffect(() => {
        if (status === 'completed' && requestId && !report) {
            fetchReport(requestId);
        }
    }, [status, requestId, report, fetchReport]);

    const handleSearch = async ({ query, depth }) => {
        await startResearch(query, depth);
    };

    const handleNewResearch = () => {
        reset();
    };

    return (
        <div className="research-page">
            {/* Header */}
            <header className="research-page__header">
                <h1 className="research-page__title">Intelligent Research Agent</h1>
                <p className="research-page__subtitle">
                    AI-powered deep research with verified, cross-referenced insights
                </p>
            </header>

            {/* Search Section */}
            <section className="research-page__search">
                <AnimatePresence mode="wait">
                    {!isResearching && !isComplete && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                        >
                            <SearchInput
                                onSubmit={handleSearch}
                                isLoading={isLoading}
                                placeholder="E.g., Research Tesla's Q4 2023 performance and market outlook..."
                            />
                        </motion.div>
                    )}
                </AnimatePresence>
            </section>

            {/* Progress Section */}
            <AnimatePresence>
                {isResearching && (
                    <motion.section
                        className="research-page__progress"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                    >
                        <ProgressIndicator
                            status={status}
                            progress={progress}
                            currentStage={currentStage}
                            questionsCompleted={questionsCompleted}
                            questionsTotal={questionsTotal}
                        />
                    </motion.section>
                )}
            </AnimatePresence>

            {/* Error Display */}
            <AnimatePresence>
                {hasError && (
                    <motion.div
                        className="research-page__error"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                    >
                        <p className="research-page__error-message">{error || 'An error occurred during research.'}</p>
                        <button className="research-page__retry" onClick={handleNewResearch}>
                            Try Again
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Results Section */}
            <AnimatePresence>
                {isComplete && report && (
                    <motion.section
                        className="research-page__results"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        {/* New Research Button */}
                        <div className="research-page__actions">
                            <button className="research-page__new-btn" onClick={handleNewResearch}>
                                ← New Research
                            </button>
                        </div>

                        {/* Executive Brief */}
                        <ExecutiveBrief
                            summary={report.executive_summary}
                            wordCount={report.total_word_count}
                            readTimeMinutes={Math.ceil(report.total_word_count / 200)}
                        />

                        {/* Tabbed Report Sections */}
                        {report.sections?.length > 0 && (
                            <div className="research-page__sections">
                                <ReportTabs sections={report.sections} />
                            </div>
                        )}

                        {/* Discrepancy Notes */}
                        {report.discrepancy_notes?.length > 0 && (
                            <div className="research-page__discrepancies">
                                <h3>Source Discrepancies</h3>
                                <ul>
                                    {report.discrepancy_notes.map((d, i) => (
                                        <li key={i}>
                                            <strong>{d.topic}:</strong> {d.resolution_notes}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Source Count */}
                        <div className="research-page__sources">
                            <p>
                                Report generated from <strong>{report.total_sources}</strong> verified sources
                            </p>
                        </div>
                    </motion.section>
                )}
            </AnimatePresence>
        </div>
    );
}

export default ResearchPage;
