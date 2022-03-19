from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404


class DetailObjectMixin:
  """ 
  Wrapper that handles request [GET] methods for a single object from database
  """

  model = None
  template = None

  def get(self, request, slug: str):
    obj = get_object_or_404(self.model, slug__iexact=slug)

    return render(
      request,
      self.template,
      context={self.model.__name__.lower(): obj}
    )


class ListObjectsMixin:
  """ 
  Wrapper that handles request [GET] methods for all objects from database
  """

  model = None
  template = None

  def get(self, request):
    search_query = request.GET.get('search', None)

    if search_query:
      objs = self.model.objects.filter(
        Q(title__icontains=search_query) | Q(body__icontains=search_query)
      )
    else:
      objs = self.model.objects.all()

    paginator = Paginator(objs, 5)
    page = paginator.get_page(request.GET.get('page', 1))

    if page.has_next():
      next_url = f'?page={page.next_page_number()}'
    else:
      next_url = ''
    if page.has_previous():
      previous_url = f'?page={page.previous_page_number()}'
    else:
      previous_url = ''

    return render(
      request,
      self.template,
      context={
        'page': page, 
        'next_url': next_url, 
        'previous_url': previous_url, 
        'search_query': search_query
      }
    )


class CreateObjectMixin:
  """ 
  Wrapper that handles request [GET, POST] methods 
  to receive the creation form and post it to server
  """

  form = None
  model = None
  template = None

  def get(self, request):
    return render(
      request,
      self.template,
      context={'form': self.form()}
    )

  def post(self, request):
    bound_form = self.form(request.POST)

    if bound_form.is_valid():
      bound_form.save()
      return redirect('display_{}s'.format(self.model.__name__.lower()))

    return render(
      request,
      self.template,
      context={'form': bound_form}
    )


class UpdateObjectMixin:
  model = None
  form = None
  template = None

  def get(self, request, slug: str):
    obj = get_object_or_404(self.model, slug__iexact=slug)
    bound_form = self.form(instance=obj)

    return render(
      request,
      self.template,
      context={'form': bound_form, self.model.__name__.lower(): obj}
    )

  def post(self, request, slug: str):
    obj = get_object_or_404(self.model, slug__iexact=slug)
    bound_form = self.form(request.POST, instance=obj)

    if bound_form.is_valid():
      bound_form.save()
      return redirect('display_{}s'.format(self.model.__name__.lower()))

    return render(
      request,
      self.template,
      context={'form': bound_form}
    )


class DeleteObjectMixin:
  model = None
  template = None
  redirect_url = None

  def get(self, request, slug: str):
    obj = get_object_or_404(self.model, slug__iexact=slug)
    
    return render(
      request, 
      self.template,
      context={self.model.__name__.lower(): obj}
    )


  def post(self, request, slug: str):
    obj = get_object_or_404(self.model, slug__iexact=slug)
    obj.delete()
    
    return redirect(reverse(self.redirect_url))
