/**
 * ProgressIndicator Component - Visual workflow progress display
 * Shows current stage and completion percentage for the research workflow
 */

import React from 'react';
import { motion } from 'framer-motion';
import './ProgressIndicator.css';

const STAGES = [
    { key: 'planning', label: 'Planning', icon: '🎯' },
    { key: 'executing', label: 'Researching', icon: '🔍' },
    { key: 'verifying', label: 'Verifying', icon: '✓' },
    { key: 'synthesizing', label: 'Synthesizing', icon: '📝' },
];

export function ProgressIndicator({
    status = 'pending',
    progress = 0,
    currentStage = '',
    questionsCompleted = 0,
    questionsTotal = 0,
    estimatedTimeRemaining,
    className = ''
}) {
    const getCurrentStageIndex = () => {
        return STAGES.findIndex(s =>
            currentStage.toLowerCase().includes(s.key) || status === s.key
        );
    };

    const currentStageIndex = getCurrentStageIndex();
    const isComplete = status === 'completed';
    const isFailed = status === 'failed';

    return (
        <div className={`progress-indicator ${className} ${isComplete ? 'progress-indicator--complete' : ''} ${isFailed ? 'progress-indicator--failed' : ''}`}>
            {/* Progress bar */}
            <div className="progress-indicator__bar-container">
                <motion.div
                    className="progress-indicator__bar"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5, ease: 'easeOut' }}
                />
            </div>

            {/* Percentage and status */}
            <div className="progress-indicator__header">
                <span className="progress-indicator__percentage">{progress}%</span>
                <span className="progress-indicator__status">{getStatusLabel(status, currentStage)}</span>
            </div>

            {/* Stage steps */}
            <div className="progress-indicator__stages">
                {STAGES.map((stage, index) => (
                    <div
                        key={stage.key}
                        className={`progress-indicator__stage ${index < currentStageIndex ? 'progress-indicator__stage--complete' : ''
                            } ${index === currentStageIndex ? 'progress-indicator__stage--active' : ''
                            }`}
                    >
                        <div className="progress-indicator__stage-icon">
                            {index < currentStageIndex ? '✓' : stage.icon}
                        </div>
                        <span className="progress-indicator__stage-label">{stage.label}</span>
                    </div>
                ))}
            </div>

            {/* Additional info */}
            <div className="progress-indicator__info">
                {questionsTotal > 0 && (
                    <span className="progress-indicator__questions">
                        {questionsCompleted}/{questionsTotal} questions
                    </span>
                )}
                {estimatedTimeRemaining && (
                    <span className="progress-indicator__time">
                        ~{Math.ceil(estimatedTimeRemaining / 60)} min remaining
                    </span>
                )}
            </div>

            {/* Pulsing animation for active state */}
            {!isComplete && !isFailed && (
                <motion.div
                    className="progress-indicator__pulse"
                    animate={{
                        scale: [1, 1.02, 1],
                        opacity: [0.7, 1, 0.7],
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />
            )}
        </div>
    );
}

function getStatusLabel(status, currentStage) {
    switch (status) {
        case 'completed':
            return 'Research Complete';
        case 'failed':
            return 'Research Failed';
        case 'planning':
            return 'Analyzing research requirements...';
        case 'executing':
            return 'Gathering and extracting information...';
        case 'verifying':
            return 'Cross-referencing sources...';
        case 'synthesizing':
            return 'Generating narrative report...';
        default:
            return currentStage || 'Initializing...';
    }
}

export default ProgressIndicator;
