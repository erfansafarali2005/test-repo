from django.contrib import admin

from .models import Relation


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'created', 'updated')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('created', 'updated')
    ordering = ('-created',)
    list_display_links = ('id', 'from_user', 'to_user')
    fields = ('from_user', 'to_user')
    date_hierarchy = 'created'