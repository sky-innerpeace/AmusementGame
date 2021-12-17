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


class Game(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    price = models.IntegerField()
    publisher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    release_date = models.DateField()
    can_multi_play = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.publisher}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_content_markdown(self):
        return markdown(self.content)