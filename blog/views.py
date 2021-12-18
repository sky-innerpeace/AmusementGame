from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
from blog.models import Game, Category, Developer


def new_comment(request, pk):
    if request.user.is_authenticated:
        game = get_object_or_404(Game, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.game = game
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(game.get_absolute_url())
    else:
        raise PermissionDenied


class GameList(ListView):
    model = Game
    ordering = '-pk'
    paginate_by = 8

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
        context['comment_form'] = CommentForm
        context['all'] = Game.objects.all()
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


class GameSearch(GameList):
    paginate_by = None
    ordering = '-pk'

    def get_queryset(self):
        q = self.kwargs['q']
        game_list = Game.objects.filter(
            # 제목, 카테고리에 포함되어 있는지
            Q(title__icontains=q) | Q(category__name__icontains=q)
        ).distinct()
        return game_list

    def get_context_data(self, **kwargs):
        context = super(GameSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'

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