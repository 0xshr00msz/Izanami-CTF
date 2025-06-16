"""
App configuration for the accounts app.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        """Import signals when the app is ready."""
        import accounts.signals
