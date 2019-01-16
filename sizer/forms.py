from django import forms

from sizer.models import Photo


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['user', 'image']


class PhotoDetailForm(forms.Form):
    width = forms.IntegerField(required=True, initial=100)
    height = forms.IntegerField(required=True, initial=100)


def get_errors(form):
    return [{field.name: field.errors} for field in form if field.errors]