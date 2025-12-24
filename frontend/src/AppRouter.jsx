/**
 * Router Configuration - Enables both legacy and new research views
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ResearchProvider } from './contexts/ResearchContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { MainLayout } from './components/MainLayout';
import { ResearchPage } from './components/ResearchPage';

import ErrorBoundary from './components/ErrorBoundary';

// Lazy load legacy app for bundle optimization
const LegacyApp = React.lazy(() => import('./LegacyApp'));

function AppRouter() {
    return (
        <ErrorBoundary fallbackMessage="The application encountered a critical error. Please refresh the page.">
            <BrowserRouter>
                <ThemeProvider>
                    <ResearchProvider>
                        <Routes>
                            {/* New Intelligent Research Agent */}
                            <Route
                                path="/research"
                                element={
                                    <MainLayout>
                                        <ErrorBoundary>
                                            <ResearchPage />
                                        </ErrorBoundary>
                                    </MainLayout>
                                }
                            />

                            {/* Legacy module-based research */}
                            <Route
                                path="/legacy"
                                element={
                                    <React.Suspense fallback={<div>Loading...</div>}>
                                        <LegacyApp />
                                    </React.Suspense>
                                }
                            />

                            {/* Default redirect to new research page */}
                            <Route path="/" element={<Navigate to="/research" replace />} />
                            <Route path="*" element={<Navigate to="/research" replace />} />
                        </Routes>
                    </ResearchProvider>
                </ThemeProvider>
            </BrowserRouter>
        </ErrorBoundary>
    );
}

export default AppRouter;
