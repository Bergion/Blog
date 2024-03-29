from django.contrib import admin
from .models import Blog, Post, Subscription, MarkedAsRead
from django.contrib.sites.models import Site
# Register your models here.


admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Subscription)
admin.site.register(MarkedAsRead)

admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'domain')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')
admin.site.register(Site, SiteAdmin)