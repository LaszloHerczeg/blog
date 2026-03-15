from django.contrib import admin, messages
from django.utils.translation import ngettext

# Register your models here.

from .models import Category, Tag, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["post_title", "excerpt", "pub_date", "author", "category", "status", 'list_tags']
    date_hierarchy = "pub_date"
    actions = ['make_published', 'make_archived']
    radio_fields = {"status": admin.HORIZONTAL}
    search_fields = ["post_title", "author__username", "tags__name", "category__name", "status"]
    search_help_text = "Searchable fields: Title, Author's username, Tags, Category, Status"

    @admin.action(description='Mark selected posts as published')
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(
            request,
            ngettext(
                '%d post was successfully marked as published.',
                '%d posts were successfully marked as published',
                updated,
            )
            % updated,
            messages.SUCCESS
        )

    @admin.action(description='Mark selected posts as archived')
    def make_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(
            request,
            ngettext(
                '%d post was successfully marked as archived.',
                '%d posts were successfully marked as archived',
                updated,
            )
            % updated,
            messages.SUCCESS
        )

    @admin.display(description="Tags")
    def list_tags(self, obj):
        queryset = obj.tags.all()
        tags = ''
        for query in queryset:
            tags += query.name + ', '
        return tags[0:-2]