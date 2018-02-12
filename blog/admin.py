from django.contrib import admin


from .models import Post, Author, Tag, Category, Feedback

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_on')
    search_fields = ['name', 'email']
    ordering = ["-name"]
    list_filter = ['active']
    date_hierarchy = 'created_on'

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'author', 'category',)
    search_fields = ['title', 'content']
    ordering = ['-publication_date']
    list_filter = ['publication_date']
    date_hierarchy = 'publication_date'
    # Form ManyToManyField class only
    filter_horizontal = ('tags',)
    # performance optimization if a huge number of tags
    raw_id_fields = ('tags',)
    # Prepopulate raw_id_fields
    prepopulated_fields = {'slug': ('title',)}
    # Make some fields non-editable
    # readonly_fields = ('slug', )
    # Fields with auto_now and auto_now_add won't appear even if specified, and will even raise a FieldError
    fields = ('title', 'slug', 'content', 'author', 'category', 'tags')
    # fields = ('title', 'content', 'slug',  'author', 'category', 'tags', 'publication_date')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Feedback, FeedbackAdmin)
