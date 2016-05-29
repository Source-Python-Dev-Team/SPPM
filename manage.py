#!/usr/bin/env python
# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import os
import sys


# =============================================================================
# >> EXECUTE
# =============================================================================
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPPM.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
