from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

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

    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None):
        self.slug = slugify(self.name).replace('_', '-')
        super(User, self).save(
                force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse(
            viewname='users:user-detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_forum_url(self):
        return _forum_member_url.format(self.forum_id)
