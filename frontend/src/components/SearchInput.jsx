/**
 * SearchInput Component - Premium search bar with depth selector
 * Per User Story 4: Research depth selection (quick/standard/comprehensive)
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import './SearchInput.css';

const DEPTH_OPTIONS = [
    { value: 'quick', label: 'Quick', desc: '3-5 questions, ~30 sec', icon: '⚡' },
    { value: 'standard', label: 'Standard', desc: '5-7 questions, ~1 min', icon: '📊' },
    { value: 'comprehensive', label: 'Deep', desc: '7-10 questions, ~2 min', icon: '🔬' },
];

export function SearchInput({
    onSubmit,
    isLoading = false,
    placeholder = 'Enter your research query...',
    className = ''
}) {
    const [query, setQuery] = useState('');
    const [depth, setDepth] = useState('standard');
    const [isFocused, setIsFocused] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim().length >= 10 && !isLoading) {
            onSubmit({ query: query.trim(), depth });
        }
    };

    const isValid = query.trim().length >= 10;

    return (
        <form
            className={`search-input ${isFocused ? 'search-input--focused' : ''} ${className}`}
            onSubmit={handleSubmit}
        >
            {/* Main input area */}
            <div className="search-input__container">
                <div className="search-input__icon">
                    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8" />
                        <path d="M21 21l-4.35-4.35" />
                    </svg>
                </div>

                <input
                    type="text"
                    className="search-input__field"
                    placeholder={placeholder}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    disabled={isLoading}
                    minLength={10}
                    maxLength={500}
                    aria-label="Research query"
                />

                <button
                    type="submit"
                    className="search-input__submit"
                    disabled={!isValid || isLoading}
                    aria-label="Start research"
                >
                    {isLoading ? (
                        <motion.div
                            className="search-input__spinner"
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                        />
                    ) : (
                        <span>Research</span>
                    )}
                </button>
            </div>

            {/* Depth selector */}
            <div className="search-input__depth">
                <span className="search-input__depth-label">Research Depth:</span>
                <div className="search-input__depth-options">
                    {DEPTH_OPTIONS.map((option) => (
                        <button
                            key={option.value}
                            type="button"
                            className={`search-input__depth-option ${depth === option.value ? 'search-input__depth-option--active' : ''}`}
                            onClick={() => setDepth(option.value)}
                            disabled={isLoading}
                        >
                            <span className="search-input__depth-icon">{option.icon}</span>
                            <span className="search-input__depth-name">{option.label}</span>
                            <span className="search-input__depth-desc">{option.desc}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Validation message */}
            {query.length > 0 && query.length < 10 && (
                <motion.p
                    className="search-input__hint"
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    Please enter at least 10 characters ({10 - query.length} more needed)
                </motion.p>
            )}
        </form>
    );
}

export default SearchInput;
