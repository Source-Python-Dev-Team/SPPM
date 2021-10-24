"""Command to create the secret key file for the environment."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
import string

# Django
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
SECRET_FILE = settings.BASE_DIR / '.secret_key'
ALLOWED_CHARS = string.printable

# Remove quotes
ALLOWED_CHARS = ALLOWED_CHARS.replace("'", '').replace('"', '')

# Remove slashes
ALLOWED_CHARS = ALLOWED_CHARS.replace('\\', '').replace('/', '')

# Remove extra characters
ALLOWED_CHARS = ALLOWED_CHARS.replace('`', '').split(' ', maxsplit=1)[0]


# =============================================================================
# COMMANDS
# =============================================================================
class Command(BaseCommand):
    """Create the secret key file."""

    def add_arguments(self, parser):
        """Add the required arguments for the command."""
        parser.add_argument(
            'length',
            type=int,
            help='The number of characters to have in the secret key.',
        )

    def handle(self, *args, **options):
        """Create the file to store the secret key."""
        if SECRET_FILE.isfile():
            raise CommandError('Secret key file already exists.')

        secret_key = get_random_string(
            length=options['length'],
            allowed_chars=ALLOWED_CHARS,
        )

        with SECRET_FILE.open('w') as open_file:
            open_file.write(secret_key)
