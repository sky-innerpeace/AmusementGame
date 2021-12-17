from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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


class GameCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Game
    fields = ['title', 'content', 'head_image', 'price', 'category', 'release_date', 'can_multi_play']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user):
            form.instance.publisher = current_user
            return super(GameCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


class GameUpdate(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['title', 'content', 'head_image', 'price', 'category', 'release_date', 'can_multi_play']

    template_name = 'blog/game_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().publisher:
            return super(GameUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


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