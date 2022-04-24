"""Command used to create random users."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
import logging
from os import urandom

# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

# Third Party Python
from random_username.generate import generate_username

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
    """Create some random Users."""

    def add_arguments(self, parser):
        """Add the required arguments for the command."""
        parser.add_argument(
            'count',
            type=int,
            help='The number of users to create.',
        )

    def handle(self, *args, **options):
        """Verify the arguments and create the Users."""
        # Only allow this command in local development
        if not settings.LOCAL:
            raise CommandError(
                'Command can only be run for local development.'
            )

        count = options['count']
        current_usernames = User.objects.values_list(
            'username',
            flat=True,
        )

        username_list = []
        valid = False
        while not valid:
            username_list = generate_username(count)
            valid = self.validate_unique_list(
                username_list=username_list,
                current_usernames=current_usernames,
                count=count,
            )

        current_forum_ids = list(
            ForumUser.objects.values_list(
                'forum_id',
                flat=True,
            )
        )
        max_id = count + len(current_forum_ids)
        id_list = list(set(range(1, max_id + 1)).difference(current_forum_ids))
        obj_list = []
        for index, username in enumerate(username_list):
            user = User.objects.create_user(
                username=username,
                password=urandom(8),
            )
            obj_list.append(
                ForumUser(
                    user=user,
                    forum_id=id_list[index],
                )
            )

        if obj_list:  # pragma: no branch
            ForumUser.objects.bulk_create(
                objs=obj_list,
            )

        logger.info(
            'Successfully created "%s" users.',
            count,
        )

    @staticmethod
    def validate_unique_list(username_list, current_usernames, count):
        """Validate the given list is unique and has the correct count."""
        return len(set(username_list).difference(current_usernames)) == count
