from django.contrib import admin
from myblog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'blogger', 'title', 'text', 'posts', 'time_created']
    fields = (('blogger', 'title'), ('text'), ('subscriptions', 'readposts'))

admin.site.register(Post, PostAdmin)
