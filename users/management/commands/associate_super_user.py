"""Command used to associate a User with a ForumUser object."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
import logging

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

# App
from users.models import ForumUser


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
User = get_user_model()

logger = logging.getLogger(__name__)


# =============================================================================
# COMMANDS
# =============================================================================
class Command(BaseCommand):
    """Create a ForumUser for a Super User."""

    def add_arguments(self, parser):
        """Add the required arguments for the command."""
        parser.add_argument(
            'username',
            type=str,
            help='The username of the SuperUser.',
        )
        parser.add_argument(
            'forum_id',
            type=int,
            help='The forum id number to associate.',
        )

    def handle(self, *args, **options):
        """Verify the arguments and associate the User."""
        # Only allow this command in local development
        if not settings.LOCAL:
            raise CommandError(
                'Command can only be run for local development.'
            )

        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(
                f'User with the username "{username}" was not found.'
            ) from User.DoesNotExist

        forum_id = options['forum_id']
        if ForumUser.objects.filter(
            forum_id=forum_id,
        ).exists():
            raise CommandError(
                f'A user is already associated with the forum id "{forum_id}".'
            )

        ForumUser.objects.create(
            user=user,
            forum_id=forum_id,
        )
        logger.info(
            f'User "{username}" successfully associated with forum id '
            f'"{forum_id}".'
        )
