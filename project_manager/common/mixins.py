"""Common mixins for use in multiple apps."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Django
from django import forms
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.views.generic import View

# 3rd-Party Django
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'DownloadMixin',
    'SubmitButtonMixin',
)


# =============================================================================
# >> MIX-INS
# =============================================================================
class DownloadMixin(View):
    """Mixin for handling downloads and download counts."""

    _full_path = None
    sub_model = None
    slug_url_kwarg = None
    sub_kwarg = None

    @property
    def model(self):
        """Return the release model."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"model" attribute.'
        )

    @property
    def base_url(self):
        """Return the base url for the download."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"base_url" attribute.'
        )

    @property
    def super_model(self):
        """Return the project model."""
        raise NotImplementedError(
            f'Class {self.__class__.__name__} must implement a '
            '"super_model" attribute.'
        )

    @property
    def super_kwarg(self):
        """Return the project's kwarg key."""
        if self.sub_model is not None:
            raise NotImplementedError(
                f'Class {self.__class__.__name__} must implement a '
                '"super_kwarg" attribute.'
            )

    @property
    def full_path(self):
        """Return the full path for the download."""
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
        """Handle dispatching the file."""
        if not self.full_path.isfile():
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle the download and download counter."""
        zip_file = kwargs['zip_file']
        with self.full_path.open('rb') as open_file:
            response = HttpResponse(
                content=open_file.read(),
                content_type='application/force-download',
            )
        response['Content-Disposition'] = f'attachment: filename={zip_file}'
        instance = self.super_model.objects.get(slug=kwargs['slug'])
        if self.sub_model is not None:
            instance = self.sub_model.objects.get(**{
                self.super_kwarg: instance,
                'slug': self.kwargs.get(self.slug_url_kwarg),
            })
        version = zip_file.split(
            f'{instance.slug}-v', 1
        )[1].rsplit('.', 1)[0]
        object_kwarg = (
            self.sub_kwarg if self.sub_kwarg is not None else self.super_kwarg
        )
        self.model.objects.filter(**{
            object_kwarg: instance,
            'version': version,
        }).update(
            download_count=F('download_count') + 1
        )
        return response


class SubmitButtonMixin(forms.ModelForm):
    """Mixin for all forms with 'Submit' buttons."""

    def __init__(self, *args, **kwargs):
        """Add the 'Submit' button to the form."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        submit = Submit('submit', 'Submit')
        submit.field_classes = 'btn btn-submit'
        self.helper.add_input(submit)
