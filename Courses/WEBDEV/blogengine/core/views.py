from sqlite3 import IntegrityError
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

from .models import Post, Tag
from .forms import PostCreationForm, TagCreationForm
from .vendor.mixins import CreateObjectMixin, DeleteObjectMixin, DetailObjectMixin, \
  ListObjectsMixin, UpdateObjectMixin
from .vendor.samples import tags


# == == == == == == == == == == == Post views == == == == == == == == == == == #
class PostDetails(DetailObjectMixin, View):
  """ Post details page """
  model = Post
  template = 'core/post_details.html'


class PostList(ListObjectsMixin, View):
  """ Posts list page """
  model = Post
  template = 'core/posts_list.html',


class CreatePost(CreateObjectMixin, View):
  """ Create post form """
  model = Post
  form = PostCreationForm
  template = 'core/post_create.html'


class UpdatePost(UpdateObjectMixin, View):
  """ Update post form """
  model = Post
  form = PostCreationForm
  template = 'core/post_update.html'


class DeletePost(DeleteObjectMixin, View):
  model = Post
  template = 'core/post_delete.html'
  redirect_url = 'display_posts'


# == == == == == == == == == == == Tags views == == == == == == == == == == == #
class TagDetails(DetailObjectMixin, View):
  """ Tag details page """
  model = Tag
  template = 'core/tag_details.html',


class TagList(ListObjectsMixin, View):
  """ Tags list page """
  model = Tag
  template = 'core/tags_list.html',


class CreateTag(CreateObjectMixin, View):
  """ Create tag form """
  model = Tag
  form = TagCreationForm
  template = 'core/tag_create.html'


class UpdateTag(UpdateObjectMixin, View):
  """ Update tag form """
  model = Tag
  form = TagCreationForm
  template = 'core/tag_update.html'


class DeleteTag(DeleteObjectMixin, View):
  model = Tag
  template = 'core/tag_delete.html'
  redirect_url = 'display_tags'


# == == == == == == == == == == == Util views == == == == == == == == == == == #
class SampleGenerator(View):
  def get(self, request):
    import lorem
    import random
    
    if Tag.objects.filter(title__iexact=tags[0]).count():
      my_tags = list(Tag.objects.all())
    else:
      my_tags = [Tag.objects.create(title=tag) for tag in tags]
    
    count = len(tags) - 1
    
    for _ in range(100):
      title = ' '.join(lorem.sentence().split()[:4])
      title = title + '.' if title[-1] != '.' else title
      post = Post.objects.create(
        title=title,
        body=lorem.text()+'\n'+lorem.text(),
      )
      
      for tag in random.sample(my_tags, random.randint(0, count)):
        post.tags.add(tag)

    return redirect(reverse('display_posts'))

