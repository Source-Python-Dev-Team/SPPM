from django import forms


class BaseCreateForm(forms.ModelForm):
    class Meta:
        fields = (
            'name',
            'version',
            'slug',
            'zip_file',
        )
        widgets = {
            'slug': forms.HiddenInput(),
        }
