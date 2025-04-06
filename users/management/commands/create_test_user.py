"""Command used to create a non-Super User."""

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
    """Create a test User."""

    def add_arguments(self, parser):
        """Add the required arguments for the command."""
        parser.add_argument(
            "username",
            type=str,
            help="The username of the User.",
        )
        parser.add_argument(
            "password",
            type=str,
            help="The password for the User.",
        )
        parser.add_argument(
            "forum_id",
            type=int,
            help="The forum id number to associate.",
        )
        parser.add_argument(
            "--is_superuser",
            action="store_true",
            default=False,
            help="Whether the User is a superuser.",
        )
        parser.add_argument(
            "--is_staff",
            action="store_true",
            default=False,
            help="Whether the User is a superuser.",
        )

    def handle(self, *_, **options):
        """Verify the arguments and create the User."""
        # Only allow this command in local development
        if not settings.LOCAL:
            msg = "Command can only be run for local development."
            raise CommandError(msg)

        username = options["username"]
        if User.objects.filter(username=username).exists():
            msg = f'User with the username "{username}" already exists.'
            raise CommandError(msg)

        forum_id = options["forum_id"]
        if ForumUser.objects.filter(forum_id=forum_id).exists():
            msg = (
                f'A user is already associated with the forum id "{forum_id}".'
            )
            raise CommandError(msg)

        try:
            user = User.objects.create_user(
                username=username,
                password=options["password"],
                is_staff=options["is_staff"],
                is_superuser=options["is_superuser"],
            )
        except Exception as exception:
            msg = f"Unable to create User due to: {exception}"
            raise CommandError(msg) from exception

        ForumUser.objects.create(
            user=user,
            forum_id=forum_id,
        )
        logger.info(
            'Successfully created user "%s" and associated it with forum id'
            ' "%s".',
            username,
            forum_id,
        )
