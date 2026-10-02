import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from note.logger import logger


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(f"Started executing '{func.__name__}'")
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        execution_time = time.perf_counter() - start_time
        logger.debug(f"Finished executing '{func.__name__}' in {execution_time:.6f}s")
        return result

    return wrapper


def handle_exceptions(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (OSError, ValueError, TypeError, KeyError, RuntimeError) as exc:
            logger.error(f"Error in '{func.__name__}': {exc}", exc_info=True)
            return None

    return wrapper