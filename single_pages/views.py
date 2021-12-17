from django.shortcuts import render

# Create your views here.
from blog.models import Game


def landing(request):
    recent_games = Game.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {
                      'recent_games': recent_games,
                  })

def about_me(request):
    return render(request, 'single_pages/about_me.html')

def amuse(request):
    return render(request, 'single_pages/amuse.html')