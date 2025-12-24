/**
 * ThemeContext - Theme provider for dark/light mode switching
 * Per FR-016: System MUST support dark mode by default with optional high-contrast light mode
 */

import React, { createContext, useContext, useState, useEffect } from 'react';

// Theme options per FR-016
const THEMES = {
    DARK: 'dark',
    LIGHT: 'light',
    LIGHT_HC: 'light-hc', // High contrast light mode
    SYSTEM: 'system'
};

const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {
    // Dark mode is default per FR-016
    const [theme, setTheme] = useState(THEMES.DARK);
    const [resolvedTheme, setResolvedTheme] = useState(THEMES.DARK);

    // Apply theme to document
    useEffect(() => {
        let actualTheme = theme;

        if (theme === THEMES.SYSTEM) {
            // Detect system preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            actualTheme = prefersDark ? THEMES.DARK : THEMES.LIGHT;
        }

        setResolvedTheme(actualTheme);

        // Apply theme to HTML element via data attribute
        document.documentElement.setAttribute('data-theme', actualTheme);

        // Also update color-scheme for native elements
        document.documentElement.style.colorScheme = actualTheme === THEMES.DARK ? 'dark' : 'light';
    }, [theme]);

    // Listen for system theme changes when in system mode
    useEffect(() => {
        if (theme !== THEMES.SYSTEM) return;

        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        const handleChange = (e) => {
            setResolvedTheme(e.matches ? THEMES.DARK : THEMES.LIGHT);
            document.documentElement.setAttribute('data-theme', e.matches ? THEMES.DARK : THEMES.LIGHT);
        };

        mediaQuery.addEventListener('change', handleChange);
        return () => mediaQuery.removeEventListener('change', handleChange);
    }, [theme]);

    // Persist theme preference
    useEffect(() => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme && Object.values(THEMES).includes(savedTheme)) {
            setTheme(savedTheme);
        }
    }, []);

    useEffect(() => {
        localStorage.setItem('theme', theme);
    }, [theme]);

    const value = {
        theme,
        resolvedTheme,
        setTheme,
        themes: THEMES,
        isDark: resolvedTheme === THEMES.DARK,
        toggleTheme: () => {
            setTheme(prev => prev === THEMES.DARK ? THEMES.LIGHT : THEMES.DARK);
        }
    };

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
}

export function useTheme() {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
}

export { THEMES };
export default ThemeContext;
