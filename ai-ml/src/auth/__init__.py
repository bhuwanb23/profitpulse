from .token_manager import TokenManager

try:
    from .quickbooks_oauth import QuickBooksOAuth
except ImportError:
    class QuickBooksOAuth:
        def __init__(self, *args, **kwargs):
            raise ImportError("authlib is not installed. Install with: pip install authlib")
