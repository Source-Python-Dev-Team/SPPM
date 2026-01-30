"""Common mixins for use in multiple apps."""

# =============================================================================
# IMPORTS
# =============================================================================
# Python
from typing import Any

# Django
from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBase
from django.utils.functional import cached_property
from django.views.generic import View

# Third Party Python
from path import Path

# App
from project_manager.models.abstract import Project

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "DownloadMixin",
)


# =============================================================================
# MIX-INS
# =============================================================================
class DownloadMixin(View):
    """Mixin for handling downloads and download counts."""

    @property
    def model(self) -> Project:
        """Return the release model."""
        msg = (
            f'Class "{self.__class__.__name__}" must implement a '
            '"model" attribute.'
        )
        raise NotImplementedError(msg)

    @property
    def base_url(self) -> str:
        """Return the base url for the download."""
        msg = (
            f'Class "{self.__class__.__name__}" must implement a '
            '"base_url" attribute.'
        )
        raise NotImplementedError(msg)

    @property
    def project_model(self) -> Project:
        """Return the project model."""
        msg = (
            f'Class "{self.__class__.__name__}" must implement a '
            '"project_model" attribute.'
        )
        raise NotImplementedError(msg)

    @property
    def model_kwarg(self) -> str:
        """Return the project's kwarg key."""
        msg = (
            f'Class "{self.__class__.__name__}" must implement a '
            '"model_kwarg" attribute.'
        )
        raise NotImplementedError(msg)

    @cached_property
    def full_path(self) -> Path:
        """Return the full path for the download."""
        return self.get_base_path() / self.kwargs["zip_file"]

    def get_base_path(self) -> Path:
        """Return the base path for the download."""
        return settings.MEDIA_ROOT / self.base_url / self.kwargs["slug"]

    def dispatch(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict,
    ) -> HttpResponseBase:
        """Handle dispatching the file."""
        if not self.full_path.is_file():
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, _: HttpRequest, **kwargs: dict[str, Any]) -> HttpResponse:
        """Handle the download and download counter."""
        zip_file = kwargs["zip_file"]
        with self.full_path.open("rb") as open_file:
            response = HttpResponse(
                content=open_file.read(),
                content_type="application/force-download",
            )
        response["Content-Disposition"] = f"attachment: filename={zip_file}"
        self.update_download_count(
            kwargs=kwargs,
        )
        return response

    def get_instance(self, kwargs: dict) -> Project:
        """Return the project's instance."""
        return self.project_model.objects.get(slug=kwargs["slug"])

    def update_download_count(
        self,
        kwargs: dict[str, Any],
    ) -> None:
        """Increments the download count for the release."""
        instance = self.get_instance(kwargs)
        zip_file = kwargs["zip_file"]
        version = zip_file.split(
            f"{instance.slug}-v", 1,
        )[1].rsplit(".", 1)[0]
        self.model.objects.filter(**{
            self.model_kwarg: instance,
            "version": version,
        }).update(
            download_count=F("download_count") + 1,
        )
