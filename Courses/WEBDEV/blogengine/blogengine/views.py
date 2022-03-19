from django.shortcuts import render


def index_page(request):
  """ Render the welcome page """
  return render(request, 'base.html')
