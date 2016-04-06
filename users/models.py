from __future__ import unicode_literals

from django.db import models

from SPPM.settings import FORUM_URL


__all__ = (
    'User',
)


_forum_member_url = FORUM_URL + '/member.php?{0}'


# Create your models here.
class User(models.Model):

    name = models.CharField(
        max_length=30,
    )

    forum_id = models.IntegerField(
        primary_key=True,
        unique=True,
    )

    def get_forum_url(self):
        return _forum_member_url.format(self.forum_id)
