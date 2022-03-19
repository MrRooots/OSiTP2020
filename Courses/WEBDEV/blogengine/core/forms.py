from django import forms
from django.forms import ValidationError
from django.utils.safestring import mark_safe

from .models import Post, Tag


class PostCreationForm(forms.ModelForm):
  """
  Implementation of post creation form
  """

  def __init__(self, *args, **kwargs):
    """ Override the __init__ method to disable form body filed strip """
    super(PostCreationForm, self).__init__(*args, **kwargs)
    self.fields['body'].strip = False

  class Meta:
    model = Post
    fields = ['title', 'body', 'tags']

    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'body': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
      'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
    }


class TagCreationForm(forms.ModelForm):
  """
  Implementation of tag creation form
  """

  class Meta:
    model = Tag
    fields = ['title']

    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
    }

  def clean_title(self):
    """ Check the new tag for uniqueness """
    title = self.cleaned_data.get('title', None)
    tag = Tag.objects.filter(title__iexact=title)
    if tag.count():
      raise ValidationError(
        mark_safe(
          'The tag must be unique! We already have <a href="{}">{}</a> tag!'.format(
            tag.first().get_absolute_url(), title.capitalize()
          )
        )
      )

    return title
