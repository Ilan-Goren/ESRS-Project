"""
App configuration for the store application.
"""

from django.apps import AppConfig


class StoreConfig(AppConfig):
    """Configuration for the store application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = 'Restaurant Store Management'
    
    def ready(self):
        """
        Initialize app when ready.
        This imports any signal handlers or performs other one-time setup.
        """
        import store.signals  # noqa