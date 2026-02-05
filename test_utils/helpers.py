"""Helper module for test case functionality."""

# =============================================================================
# IMPORTS
# =============================================================================
# Django
from django.db.models import Model

# =============================================================================
# ALL DECLARATION
# =============================================================================
__all__ = (
    "get_new_fields_for_model",
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def _get_field_names_for_model(model: type[Model]) -> set:
    """Return the names of all fields in a model."""
    return {
        field.name
        for field in vars(model)["_meta"].get_fields()
        if not field.auto_created and
        not field.name.endswith("_rendered")
    }


def get_new_fields_for_model(model: type[Model]) -> set:
    """Return the names of fields in a model not present in parent_model."""
    field_list = _get_field_names_for_model(model)
    for base_class in model.__bases__:
        if base_class is Model or not issubclass(base_class, Model):
            continue
        field_list.difference_update(
            _get_field_names_for_model(base_class),
        )

    return field_list
