from django.contrib.auth.models import User
from django.db import models
from markdown import markdown
from markdownx.models import MarkdownxField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class Developer(models.Model):  # 개발자(제조사)
    name = models.CharField(max_length=50, unique=True) #제조사명
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/developer/{self.slug}'

    class Meta:
        verbose_name_plural = 'Developers'


class Game(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    price = models.IntegerField()
    publisher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    developer = models.ForeignKey(Developer, null=True, blank=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    release_date = models.DateField()
    can_multi_play = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.publisher}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)

    def get_avatar_url(self):
        if self.publisher.socialaccount_set.exists():
            return self.publisher.socialaccount_set.first().get_avatar_url()
        # 랜덤 아바타를 생성하는 유저 중에 이메일이 없는 유저 예외처리
        else:
            if self.publisher.email:
                return f'https://doitdjango.com/avatar/id/386/eea990dfe51e2ca3/svg/{self.publisher.email}/'
            else:
                return f'https://doitdjango.com/avatar/id/386/eea990dfe51e2ca3/svg/{self.publisher}/'


class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)    #글이 삭제되면 연관된 모든 댓글도 삭제제
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.game.get_absolute_url()}#comment-{self.pk}'    #포스트url#comment-pk

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        # 랜덤 아바타를 생성하는 유저 중에 이메일이 없는 유저 예외처리
        else:
            if self.author.email:
                return f'https://doitdjango.com/avatar/id/386/eea990dfe51e2ca3/svg/{self.author.email}/'
            else:
                return f'https://doitdjango.com/avatar/id/386/eea990dfe51e2ca3/svg/{self.author}/'
