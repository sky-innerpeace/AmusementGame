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

# def index(request):
#     games = Game.objects.all().order_by('-pk')
#     return render(request, 'blog/index.html',
#                   {
#                       'games' : games
#                   }
#                   )
#
# def single_game_page(request, pk):
#     game = Game.objects.get(pk=pk)
#     return render(request, 'blog/single_game_page.html',
#                   {
#                       'game' : game
#                   }
#                   )
