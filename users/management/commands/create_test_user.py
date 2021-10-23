# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

# App
from users.models import ForumUser


# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
User = get_user_model()


# =============================================================================
# COMMANDS
# =============================================================================
class Command(BaseCommand):
    """Populate the Game objects."""

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='The username of the User.',
        )
        parser.add_argument(
            'password',
            type=str,
            help='The password for the User.',
        )
        parser.add_argument(
            'forum_id',
            type=int,
            help='The forum id number to associate.',
        )

    def handle(self, *args, **options):
        username = options['username']
        if User.objects.filter(username=username).exists():
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

        try:
            user = User.objects.create_user(
                username=username,
                password=options['password'],
            )
        except Exception as e:
            raise CommandError(
                f'Unable to create User due to: {e}'
            )

        ForumUser.objects.create(
            user=user,
            forum_id=forum_id,
        )
        print(
            f'User "{username}" successfully associated with forum id '
            f'"{forum_id}".'
        )
