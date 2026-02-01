"""Utility functions and helpers"""

from typing import Any, Dict

def format_response(data: Any, message: str = None, status: str = "success") -> Dict:
    """Format API response in consistent format"""
    return {
        "status": status,
        "message": message,
        "data": data
    }


def format_error(error: str, status_code: int = 400) -> Dict:
    """Format error response"""
    return {
        "status": "error",
        "message": error,
        "status_code": status_code
    }


def paginate(items: list, skip: int = 0, limit: int = 100) -> Dict:
    """Paginate list of items"""
    return {
        "items": items[skip:skip+limit],
        "total": len(items),
        "skip": skip,
        "limit": limit
    }
