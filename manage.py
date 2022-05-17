#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from services.requirements_manager import update_requirements

# python manage.py show_urls


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    update_requirements()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
