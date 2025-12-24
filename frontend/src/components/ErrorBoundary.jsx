/**
 * ErrorBoundary Component - React error boundary for graceful error handling
 * Production-ready error catching with recovery options
 */

import React, { Component } from 'react';
import './ErrorBoundary.css';

class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null,
            eventId: null
        };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // Log error to console in development
        console.error('ErrorBoundary caught an error:', error, errorInfo);

        this.setState({ errorInfo });

        // In production, you would send to error tracking service
        // Example: Sentry.captureException(error, { extra: errorInfo });
    }

    handleRetry = () => {
        this.setState({ hasError: false, error: null, errorInfo: null });
    };

    handleReload = () => {
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-boundary">
                    <div className="error-boundary__content">
                        <div className="error-boundary__icon">⚠️</div>
                        <h2 className="error-boundary__title">Something went wrong</h2>
                        <p className="error-boundary__message">
                            {this.props.fallbackMessage ||
                                "We're sorry, but something unexpected happened. Please try again."}
                        </p>

                        {process.env.NODE_ENV === 'development' && this.state.error && (
                            <details className="error-boundary__details">
                                <summary>Error Details (Development Only)</summary>
                                <pre>{this.state.error.toString()}</pre>
                                <pre>{this.state.errorInfo?.componentStack}</pre>
                            </details>
                        )}

                        <div className="error-boundary__actions">
                            <button
                                className="error-boundary__button error-boundary__button--primary"
                                onClick={this.handleRetry}
                            >
                                Try Again
                            </button>
                            <button
                                className="error-boundary__button error-boundary__button--secondary"
                                onClick={this.handleReload}
                            >
                                Reload Page
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;

// Higher-order component for wrapping with error boundary
export function withErrorBoundary(WrappedComponent, fallbackMessage) {
    return function WithErrorBoundary(props) {
        return (
            <ErrorBoundary fallbackMessage={fallbackMessage}>
                <WrappedComponent {...props} />
            </ErrorBoundary>
        );
    };
}
