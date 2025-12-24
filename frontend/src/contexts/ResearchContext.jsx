/**
 * ResearchContext - Global state for research operations
 * 
 * Manages:
 * - Current research request and progress
 * - Research plan and sub-questions
 * - Completed report data
 * - Loading and error states
 */

import React, { createContext, useContext, useState, useCallback } from 'react';
import api from '../services/api';

const ResearchContext = createContext(null);

// Initial state
const initialState = {
    // Current request
    requestId: null,
    query: '',
    depthLevel: 'standard',

    // Status
    status: 'idle', // idle, planning, executing, verifying, synthesizing, completed, failed
    progress: 0,
    currentStage: '',

    // Research plan
    plan: null,
    questionsCompleted: 0,
    questionsTotal: 0,

    // Results
    report: null,
    citations: [],

    // UI state
    isLoading: false,
    error: null
};

export function ResearchProvider({ children }) {
    const [state, setState] = useState(initialState);

    // Start a new research request
    const startResearch = useCallback(async (query, depthLevel = 'standard') => {
        setState(prev => ({
            ...initialState,
            query,
            depthLevel,
            status: 'planning',
            isLoading: true
        }));

        try {
            // Call execute endpoint (async mode)
            const response = await api.post('/api/research/execute', {
                query,
                depth_level: depthLevel,
                async: true
            });

            const { request_id } = response.data;

            setState(prev => ({
                ...prev,
                requestId: request_id,
                status: 'executing'
            }));

            return request_id;
        } catch (error) {
            setState(prev => ({
                ...prev,
                status: 'failed',
                isLoading: false,
                error: error.message || 'Failed to start research'
            }));
            throw error;
        }
    }, []);

    // Poll for research status
    const pollStatus = useCallback(async (requestId) => {
        try {
            const response = await api.get(`/api/research/${requestId}/status`);
            const data = response.data;

            setState(prev => ({
                ...prev,
                status: data.status,
                progress: data.progress_percent || 0,
                currentStage: data.current_stage || '',
                questionsCompleted: data.questions_completed || 0,
                questionsTotal: data.questions_total || 0
            }));

            return data.status;
        } catch (error) {
            console.error('Status poll failed:', error);
            return state.status;
        }
    }, [state.status]);

    // Fetch completed report
    const fetchReport = useCallback(async (requestId) => {
        setState(prev => ({ ...prev, isLoading: true }));

        try {
            const response = await api.get(`/api/research/${requestId}/report`);

            setState(prev => ({
                ...prev,
                report: response.data,
                status: 'completed',
                isLoading: false
            }));

            return response.data;
        } catch (error) {
            setState(prev => ({
                ...prev,
                isLoading: false,
                error: error.message || 'Failed to fetch report'
            }));
            throw error;
        }
    }, []);

    // Fetch citations for a report
    const fetchCitations = useCallback(async (requestId) => {
        try {
            const response = await api.get(`/api/research/${requestId}/citations`);

            setState(prev => ({
                ...prev,
                citations: response.data.citations || []
            }));

            return response.data.citations;
        } catch (error) {
            console.error('Failed to fetch citations:', error);
            return [];
        }
    }, []);

    // Reset state for new research
    const reset = useCallback(() => {
        setState(initialState);
    }, []);

    // Update specific state field
    const updateState = useCallback((updates) => {
        setState(prev => ({ ...prev, ...updates }));
    }, []);

    const value = {
        // State
        ...state,

        // Actions
        startResearch,
        pollStatus,
        fetchReport,
        fetchCitations,
        reset,
        updateState,

        // Computed
        isResearching: ['planning', 'executing', 'verifying', 'synthesizing'].includes(state.status),
        isComplete: state.status === 'completed',
        hasError: state.status === 'failed'
    };

    return (
        <ResearchContext.Provider value={value}>
            {children}
        </ResearchContext.Provider>
    );
}

export function useResearch() {
    const context = useContext(ResearchContext);
    if (!context) {
        throw new Error('useResearch must be used within a ResearchProvider');
    }
    return context;
}

export default ResearchContext;
