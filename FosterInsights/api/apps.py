import sys
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # Skip this check during migrations so management commands work cleanly
        if "manage.py" in sys.argv and any(
            cmd in sys.argv for cmd in ["migrate", "makemigrations", "import_csv_data"]
        ):
            return

        from django.urls import get_resolver

        resolver = get_resolver()

        # Audit every registered URL endpoint in the app
        for url_pattern in resolver.url_patterns:
            if hasattr(url_pattern, "callback"):
                view_func = url_pattern.callback

                if getattr(view_func, "__is_react_spa_entry__", True):
                    return

                # Verify that the hidden attribute attached by @protected_api_view exists
                if not getattr(view_func, "__is_license_protected__", False):
                    raise RuntimeError(
                        f"\n===================================================================\n"
                        f" SECURITY VIOLATION: View '{view_func.__name__}' is missing\n"
                        f" the mandatory '@protected_api_view' guard.\n"
                        f" All endpoints must be decorated with license protection.\n"
                        f"===================================================================\n"
                    )
