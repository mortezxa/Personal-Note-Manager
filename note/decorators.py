import time
from functools import wraps
from typing import Any, Callable

from note.logger import logger


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Started executing '{func.__name__}'")
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        logger.info(f"Finished executing '{func.__name__}' in {execution_time:.6f}s")
        return result

    return wrapper


def handle_exceptions(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error occurred in '{func.__name__}': {str(e)}", exc_info=True
            )
            return None

    return wrapper
