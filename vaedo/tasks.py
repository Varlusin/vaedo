import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaedo.settings")
import django
from django.core.cache import cache
from location.constants import (SERVICE_AVAILABLE_SPACE,
                                SITY_LIST,
                                COMUNITY_DATA)


django.setup()

def main():
    """
    Main function to save constants to cache.
    """
    # Save constants to cache
    cache.set('SERVICE_AVAILABLE_SPACE', SERVICE_AVAILABLE_SPACE, timeout=None)
    cache.set('SITY_LIST', SITY_LIST, timeout=None)
    cache.set('COMUNITY_DATA', COMUNITY_DATA, timeout=None)

if __name__ == "__main__":
    main()