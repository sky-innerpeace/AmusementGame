from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from blog.models import Game, Category


class GameList(ListView):
    model = Game
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(GameList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_game_count'] = Game.objects.filter(category=None).count()
        return context



class GameDetail(DetailView):
    model = Game
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(GameDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_game_count'] = Game.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        game_list = Game.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        game_list = Game.objects.filter(category=category)

    return render(
        request,
        'blog/game_list.html',
        {
            'game_list': game_list,
            'categories': Category.objects.all(),
            'no_category_game_count': Game.objects.filter(category=None).count(),
            'category': category,
        }
    )