"""Structured logging utility for the Intelligent Research Agent.

Per NFR-003 to NFR-006:
- NFR-003: Log structured events for each workflow stage with duration
- NFR-004: Log all LLM API calls with prompt length, response length, latency
- NFR-005: Log search provider calls with query, result count, latency
- NFR-006: Logs MUST be structured (JSON format)
"""

import structlog
import time
from functools import wraps
from typing import Any, Callable, Optional
from datetime import datetime
import logging
import os
from backend.config import settings

# Configure structlog for JSON output
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Configure standard logging to file
if settings.LOG_TO_FILE:
    os.makedirs(os.path.dirname(settings.LOG_FILE_PATH), exist_ok=True)
    
    # Remove existing handlers to avoid duplication if reloaded
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)
            
    handlers = [logging.StreamHandler()]
    handlers.append(logging.FileHandler(settings.LOG_FILE_PATH))
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(message)s",
        handlers=handlers
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance.
    
    Args:
        name: Logger name, typically module name
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class StageTimer:
    """Context manager for timing workflow stages with structured logging.
    
    Per NFR-003: Log structured events for each workflow stage with duration.
    
    Usage:
        with StageTimer("planning", logger) as timer:
            # do planning work
        # Automatically logs duration on exit
    """
    
    def __init__(self, stage_name: str, logger: structlog.BoundLogger, **extra_context):
        self.stage_name = stage_name
        self.logger = logger
        self.extra_context = extra_context
        self.start_time: float = 0
        self.end_time: float = 0
        
    def __enter__(self) -> 'StageTimer':
        self.start_time = time.perf_counter()
        self.logger.info(
            f"stage_started",
            stage=self.stage_name,
            **self.extra_context
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        duration_ms = (self.end_time - self.start_time) * 1000
        
        if exc_type is None:
            self.logger.info(
                f"stage_completed",
                stage=self.stage_name,
                duration_ms=round(duration_ms, 2),
                **self.extra_context
            )
        else:
            self.logger.error(
                f"stage_failed",
                stage=self.stage_name,
                duration_ms=round(duration_ms, 2),
                error=str(exc_val),
                error_type=exc_type.__name__,
                **self.extra_context
            )
        return False  # Don't suppress exceptions


def log_llm_call(logger: structlog.BoundLogger):
    """Decorator to log LLM API calls with metrics.
    
    Per NFR-004: Log all LLM API calls with prompt length, response length, latency.
    
    Usage:
        @log_llm_call(logger)
        async def call_openai(prompt: str) -> str:
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract prompt from args or kwargs
            prompt = kwargs.get('prompt', args[0] if args else '')
            prompt_length = len(str(prompt))
            
            start_time = time.perf_counter()
            
            try:
                result = await func(*args, **kwargs)
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                
                response_length = len(str(result)) if result else 0
                
                logger.info(
                    "llm_call_completed",
                    function=func.__name__,
                    prompt_length=prompt_length,
                    response_length=response_length,
                    latency_ms=round(latency_ms, 2),
                    model=kwargs.get('model', 'unknown')
                )
                
                return result
                
            except Exception as e:
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                
                logger.error(
                    "llm_call_failed",
                    function=func.__name__,
                    prompt_length=prompt_length,
                    latency_ms=round(latency_ms, 2),
                    error=str(e),
                    error_type=type(e).__name__,
                    model=kwargs.get('model', 'unknown')
                )
                raise
        
        return wrapper
    return decorator


def log_search_call(logger: structlog.BoundLogger):
    """Decorator to log search provider calls with metrics.
    
    Per NFR-005: Log search provider calls with query, result count, latency.
    
    Usage:
        @log_search_call(logger)
        async def search_duckduckgo(query: str) -> List[dict]:
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            query = kwargs.get('query', args[0] if args else '')
            provider = kwargs.get('provider', func.__name__)
            
            start_time = time.perf_counter()
            
            try:
                result = await func(*args, **kwargs)
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                
                result_count = len(result) if isinstance(result, list) else 1
                
                logger.info(
                    "search_call_completed",
                    provider=provider,
                    query=query[:100],  # Truncate for log readability
                    result_count=result_count,
                    latency_ms=round(latency_ms, 2)
                )
                
                return result
                
            except Exception as e:
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                
                logger.error(
                    "search_call_failed",
                    provider=provider,
                    query=query[:100],
                    latency_ms=round(latency_ms, 2),
                    error=str(e),
                    error_type=type(e).__name__
                )
                raise
        
        return wrapper
    return decorator


def log_workflow_event(
    logger: structlog.BoundLogger,
    event: str,
    request_id: str,
    stage: str,
    **extra
):
    """Log a workflow event with standard fields.
    
    Args:
        logger: Structlog logger instance
        event: Event name (e.g., 'workflow_started', 'question_completed')
        request_id: Research request ID
        stage: Current workflow stage (planning, executing, verifying, synthesizing)
        **extra: Additional context fields
    """
    logger.info(
        event,
        request_id=request_id,
        stage=stage,
        timestamp=datetime.now().isoformat(),
        **extra
    )
