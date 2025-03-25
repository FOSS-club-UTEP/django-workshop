from django import forms
from .models import BlogPost


class NewBlogpostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"
