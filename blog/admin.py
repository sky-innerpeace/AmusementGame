from django.contrib import admin

# Register your models here.
from blog.models import Game, Category

admin.site.register(Game)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)