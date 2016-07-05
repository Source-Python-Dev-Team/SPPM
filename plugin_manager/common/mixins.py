# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.views.generic import View


# =============================================================================
# >> MIX-INS
# =============================================================================
class DownloadMixin(View):
    _full_path = None
    sub_model = None
    slug_url_kwarg = None
    sub_kwarg = None

    @property
    def model(self):
        raise NotImplementedError(
            'Class {class_name} must implement a model attribute.'.format(
                class_name=self.__class__.__name__,
            ),
        )

    @property
    def base_url(self):
        raise NotImplementedError(
            'Class {class_name} must implement a base_url attribute.'.format(
                class_name=self.__class__.__name__,
            ),
        )

    @property
    def super_model(self):
        raise NotImplementedError(
            'Class {class_name} must implement a super_model attribute.'.format(
                class_name=self.__class__.__name__,
            ),
        )

    @property
    def super_kwarg(self):
        if self.sub_model is not None:
            raise NotImplementedError(
                'Class {class_name} must implement a super_kwarg '
                'attribute.'.format(
                    class_name=self.__class__.__name__,
                )
            )
        return None

    @property
    def full_path(self):
        if self._full_path is None:
            self._full_path = (
                settings.MEDIA_ROOT / self.base_url / self.kwargs['slug']
            )
            if self.slug_url_kwarg is not None:
                slug = self.kwargs.get(self.slug_url_kwarg)
                if slug is not None:
                    self._full_path /= slug
            self._full_path /= self.kwargs['zip_file']
        return self._full_path

    def dispatch(self, request, *args, **kwargs):
        if not self.full_path.isfile():
            raise Http404
        return super(DownloadMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        zip_file = kwargs['zip_file']
        with self.full_path.open('rb') as open_file:
            response = HttpResponse(
                content=open_file.read(),
                content_type='application/force-download',
            )
        response['Content-Disposition'] = (
            'attachment: filename={filename}'.format(
                filename=zip_file,
            )
        )
        instance = self.super_model.objects.get(slug=kwargs['slug'])
        if self.sub_model is not None:
            instance = self.sub_model.objects.get(**{
                self.super_kwarg: instance,
                'slug': self.kwargs.get(self.slug_url_kwarg),
            })
        version = zip_file.split(
            '{slug}-v'.format(slug=instance.slug), 1
        )[1].rsplit('.', 1)[0]
        object_kwarg = (
            self.sub_kwarg if self.sub_kwarg is not None else self.super_kwarg
        )
        self.model.objects.filter(**{
            object_kwarg: instance,
            'version': version,
        }
        ).update(
            download_count=F('download_count') + 1
        )
        return response
