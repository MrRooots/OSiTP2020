import time
from sqlite3 import IntegrityError
from django.urls import reverse
from django.db import models
from django.utils.text import slugify


def build_slug(title: str):
  """ Function that build unique slug from given title """
  return f'{slugify(title, allow_unicode=True)}-{int(time.time())}'


class Post(models.Model):
  """
  Post model
  """

  title = models.CharField(max_length=128, db_index=True)
  slug = models.SlugField(max_length=128, db_index=True)
  body = models.TextField(blank=True, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

  class Meta:
    ordering = ['-updated_at', '-created_at']

  def __str__(self) -> str:
    return 'Post details:\nTitle: {}\nSlug: {}\nBody: {}\nCreated at: {}'.format(
      self.title, self.slug, self.body, self.created_at
    )

  def get_absolute_url(self):
    return reverse('post_details', kwargs={'slug': self.slug})

  def get_update_url(self):
    return reverse('post_update', kwargs={'slug': self.slug})

  def get_delete_url(self):
    return reverse('post_delete', kwargs={'slug': self.slug})

  def get_date_difference(self):
    return (self.updated_at - self.created_at).seconds > 0

  def save(self, *args, **kwargs) -> None:
    self.title = self.title.title()

    try:
      self.body = self.body[0].capitalize() + self.body[1:]
    except IndexError:
      pass

    if not self.slug:
      self.slug = build_slug(self.title)

    return super().save(*args, **kwargs)


class Tag(models.Model):
  """
  Tag model
  """

  title = models.CharField(max_length=128, unique=True)
  slug = models.SlugField(max_length=128, db_index=True)

  class Meta:
    ordering = ['title']

  def __str__(self) -> str:
    return self.title

  def get_absolute_url(self):
    return reverse('tag_details', kwargs={'slug': self.slug})

  def get_update_url(self):
    return reverse('tag_update', kwargs={'slug': self.slug})

  def get_delete_url(self):
    return reverse('tag_delete', kwargs={'slug': self.slug})

  def save(self, *args, **kwargs) -> None:
    self.title = self.title.title()

    if not self.slug:
      self.slug = build_slug(self.title)

    return super().save(*args, **kwargs)
