# =============================================================================
# IMPORTS
# =============================================================================
# Python
from os import urandom

# Django
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


# =============================================================================
# COMMANDS
# =============================================================================
class Command(BaseCommand):
    """Populate the Game objects."""

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='The number of users to create.',
        )

    def handle(self, *args, **options):
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
        for n, username in enumerate(username_list):
            user = User.objects.create_user(
                username=username,
                password=urandom(8),
            )
            obj_list.append(
                ForumUser(
                    user=user,
                    forum_id=id_list[n],
                )
            )

        if obj_list:
            ForumUser.objects.bulk_create(
                objs=obj_list,
            )

        print(f'Successfully created "{count}" users.')

    @staticmethod
    def validate_unique_list(username_list, current_usernames, count):
        return len(set(username_list).difference(current_usernames)) == count
