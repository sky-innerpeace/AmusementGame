from django.contrib.auth.models import User
from django.test import TestCase, Client


# Create your tests here.
from blog.models import Game


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_sky = User.objects.create_user(username='sky', password='somepassword')


    def test_game_list(self):
        # 포스트 목록 페이지 가져옴
        response = self.client.get('/blog/')
        # 정상적으로 페이지 로드?
        self.assertEqual(response.status_code,200)

    def test_game_detail(self):
        game_001 = Game.objects.create(
            title = 'League of Legend',
            content = "무한대기 챔피언~",
            price = 2010,
            release_date = '2010-11-11',
            can_multi_play=False
        )
        self.assertEqual(game_001.get_absolute_url(), '/blog/1/')

