from django.urls import path
from .views import CreatePost, CreateTag, DeletePost, DeleteTag, PostDetails, PostList, SampleGenerator, TagDetails, \
  TagList, UpdateTag, UpdatePost

urlpatterns = [
  path('posts/', PostList.as_view(), name='display_posts'),
  path('posts/create', CreatePost.as_view(), name='create_post'),
  path('posts/<str:slug>', PostDetails.as_view(), name='post_details'),
  path('posts/<str:slug>/update', UpdatePost.as_view(), name='post_update'),
  path('posts/<str:slug>/delete', DeletePost.as_view(), name='post_delete'),

  path('tags/', TagList.as_view(), name='display_tags'),
  path('tags/create', CreateTag.as_view(), name='create_tag'),
  path('tags/<str:slug>', TagDetails.as_view(), name='tag_details'),
  path('tags/<str:slug>/update', UpdateTag.as_view(), name='tag_update'),
  path('tags/<str:slug>/delete', DeleteTag.as_view(), name='tag_delete'),

  path('generate_samples/', SampleGenerator.as_view(), name='generate_samples')
]
