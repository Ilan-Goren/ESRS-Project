"""
App configuration for the supplier application.
"""

from django.apps import AppConfig


class SupplierConfig(AppConfig):
    """Configuration for the supplier application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'supplier'
    verbose_name = 'Supplier Management'
    
    def ready(self):
        """
        Initialize app when ready.
        This imports any signal handlers or performs other one-time setup.
        """
        import supplier.signals  # noqa