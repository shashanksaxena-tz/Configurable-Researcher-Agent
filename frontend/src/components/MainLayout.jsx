/**
 * MainLayout Component - Application layout wrapper
 * Applies theme and global styles
 */

import React from 'react';
import { ThemeProvider, useTheme } from '../contexts/ThemeContext';
import './MainLayout.css';

function ThemeToggle() {
    const { isDark, toggleTheme } = useTheme();

    return (
        <button
            className="main-layout__theme-toggle"
            onClick={toggleTheme}
            aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
        >
            {isDark ? '☀️' : '🌙'}
        </button>
    );
}

function LayoutContent({ children }) {
    return (
        <div className="main-layout">
            <nav className="main-layout__nav">
                <div className="main-layout__logo">
                    <span className="main-layout__logo-icon">🔬</span>
                    <span className="main-layout__logo-text">Research Agent</span>
                </div>
                <ThemeToggle />
            </nav>

            <main className="main-layout__main">
                {children}
            </main>

            <footer className="main-layout__footer">
                <p>Powered by AI • Cross-referenced from multiple sources</p>
            </footer>
        </div>
    );
}

export function MainLayout({ children }) {
    return (
        <ThemeProvider>
            <LayoutContent>{children}</LayoutContent>
        </ThemeProvider>
    );
}

export default MainLayout;
