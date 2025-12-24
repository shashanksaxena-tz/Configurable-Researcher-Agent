/**
 * DepthSelector Component - Interactive research depth selection
 * Per User Story 4: Users can configure research depth (quick/standard/comprehensive)
 * Per FR-004: System MUST implement configurable recursion depth limit
 */

import React from 'react';
import { motion } from 'framer-motion';
import './DepthSelector.css';

const DEPTH_LEVELS = [
    {
        value: 'quick',
        label: 'Quick',
        emoji: '⚡',
        questions: '3-5',
        recursion: '1 level',
        time: '~30 sec',
        description: 'Fast overview with key facts. Best for simple questions.',
        color: 'var(--success-color)'
    },
    {
        value: 'standard',
        label: 'Standard',
        emoji: '📊',
        questions: '5-7',
        recursion: '2 levels',
        time: '~1 min',
        description: 'Balanced research with multiple perspectives. Recommended for most queries.',
        color: 'var(--accent-gold)'
    },
    {
        value: 'comprehensive',
        label: 'Comprehensive',
        emoji: '🔬',
        questions: '7-10',
        recursion: '3 levels',
        time: '~2 min',
        description: 'Deep analysis with extensive cross-referencing. Best for complex topics.',
        color: 'var(--info-color)'
    }
];

export function DepthSelector({
    value = 'standard',
    onChange,
    disabled = false,
    className = ''
}) {
    return (
        <div className={`depth-selector ${className}`}>
            <h4 className="depth-selector__title">Research Depth</h4>

            <div className="depth-selector__options">
                {DEPTH_LEVELS.map((level) => (
                    <motion.button
                        key={level.value}
                        type="button"
                        className={`depth-selector__option ${value === level.value ? 'depth-selector__option--active' : ''}`}
                        onClick={() => onChange?.(level.value)}
                        disabled={disabled}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        style={{
                            '--level-color': level.color
                        }}
                    >
                        <div className="depth-selector__option-header">
                            <span className="depth-selector__emoji">{level.emoji}</span>
                            <span className="depth-selector__label">{level.label}</span>
                            {value === level.value && (
                                <span className="depth-selector__check">✓</span>
                            )}
                        </div>

                        <div className="depth-selector__option-body">
                            <p className="depth-selector__description">{level.description}</p>

                            <div className="depth-selector__specs">
                                <span className="depth-selector__spec">
                                    <span className="depth-selector__spec-icon">❓</span>
                                    {level.questions} questions
                                </span>
                                <span className="depth-selector__spec">
                                    <span className="depth-selector__spec-icon">🔁</span>
                                    {level.recursion}
                                </span>
                                <span className="depth-selector__spec">
                                    <span className="depth-selector__spec-icon">⏱️</span>
                                    {level.time}
                                </span>
                            </div>
                        </div>
                    </motion.button>
                ))}
            </div>

            {/* Visual indicator of selected depth */}
            <div className="depth-selector__indicator">
                <div className="depth-selector__indicator-track">
                    <motion.div
                        className="depth-selector__indicator-fill"
                        animate={{
                            width: value === 'quick' ? '33%' : value === 'standard' ? '66%' : '100%'
                        }}
                        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                    />
                </div>
                <div className="depth-selector__indicator-labels">
                    <span>Faster</span>
                    <span>Deeper</span>
                </div>
            </div>
        </div>
    );
}

export default DepthSelector;
