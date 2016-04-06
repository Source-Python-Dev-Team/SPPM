from common.forms import BaseCreateForm

from .models import Package


__all__ = (
    'PackageCreateForm',
)


class PackageCreateForm(BaseCreateForm):
    class Meta(BaseCreateForm.Meta):
        model = Package
