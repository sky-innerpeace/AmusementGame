from django.contrib import admin

# Register your models here.
from markdownx.admin import MarkdownxModelAdmin

from blog.models import Game, Category, Comment, Developer

admin.site.register(Game, MarkdownxModelAdmin)
admin.site.register(Comment)


class DeveloperAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Developer, DeveloperAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)