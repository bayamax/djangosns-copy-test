from django import forms

from .models import Community

class CommunityCreateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = (
            'name','memo'
        )