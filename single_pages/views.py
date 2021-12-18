from django.shortcuts import render, redirect

# Create your views here.
from blog.models import Game, Comment


def landing(request):
    recent_games = Game.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {
                      'recent_games': recent_games,
                  })

def about_me(request):
    if(request.user.is_authenticated):  #로그인했다면
        comment_list = Comment.objects.filter(author=request.user)

        return render(request,
                    'single_pages/about_me.html',
                    {
                        'comment_list':comment_list,
                    }
                )
    else:   #로그인 안했으면 접근 불가
        return redirect('/')

def amuse(request):
    game_statistic = {'MOBA':0, 'Simulation':0, 'MMORPG':0, 'Horror':0, 'Adventure':0, '미분류': 0}
    game_list = Game.objects.all()
    for game in game_list:
        if(game.category!=None):
            game_statistic[f'{game.category}'] += 1
        else:
            game_statistic['미분류'] += 1
    return render(
        request,
        'single_pages/amuse.html',
        {
            'game_statistic':game_statistic,

        }
    )