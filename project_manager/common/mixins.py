"""Common mixins for use in multiple apps."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.views.generic import View


# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadMixin',
)


# =============================================================================
# MIX-INS
# =============================================================================
class DownloadMixin(View):
    """Mixin for handling downloads and download counts."""

    _full_path = None

    @property
    def model(self):
        """Return the release model."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"model" attribute.'
        )

    @property
    def base_url(self):
        """Return the base url for the download."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"base_url" attribute.'
        )

    @property
    def project_model(self):
        """Return the project model."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"project_model" attribute.'
        )

    @property
    def model_kwarg(self):
        """Return the project's kwarg key."""
        raise NotImplementedError(
            f'Class "{self.__class__.__name__}" must implement a '
            '"model_kwarg" attribute.'
        )

    @property
    def full_path(self):
        """Return the full path for the download."""
        if self._full_path is None:
            self._full_path = self.get_base_path()
            self._full_path /= self.kwargs['zip_file']
        return self._full_path

    def get_base_path(self):
        """Return the base path for the download."""
        return settings.MEDIA_ROOT / self.base_url / self.kwargs['slug']

    def dispatch(self, request, *args, **kwargs):
        """Handle dispatching the file."""
        if not self.full_path.isfile():
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """Handle the download and download counter."""
        zip_file = kwargs['zip_file']
        with self.full_path.open('rb') as open_file:
            response = HttpResponse(
                content=open_file.read(),
                content_type='application/force-download',
            )
        response['Content-Disposition'] = f'attachment: filename={zip_file}'
        self.update_download_count(
            kwargs=kwargs,
            zip_file=zip_file,
        )
        return response

    def get_instance(self, kwargs):
        """Return the project's instance."""
        return self.project_model.objects.get(slug=kwargs['slug'])

    def update_download_count(self, kwargs, zip_file):
        """Increments the download count for the release."""
        instance = self.get_instance(kwargs)
        version = zip_file.split(
            f'{instance.slug}-v', 1
        )[1].rsplit('.', 1)[0]
        self.model.objects.filter(**{
            self.model_kwarg: instance,
            'version': version,
        }).update(
            download_count=F('download_count') + 1
        )
