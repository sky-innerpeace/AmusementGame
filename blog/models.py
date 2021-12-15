from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    #head_image
    price = models.IntegerField()
    publisher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #category
    release_date = models.DateField()
    can_multi_play = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.pk}]{self.title}'
