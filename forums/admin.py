from django.contrib import admin

from .models import Thread, Response

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 3

class ThreadAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['thread_title', 'thread_content']}),
        ('Date information', {'fields': ['thread_date']}),
    ]
    inlines = [ResponseInline]
    list_display = ('thread_title', 'thread_date', 'was_posted_recently')
    list_filter = ['thread_date']
    search_fields = ['thread_title', 'thread_content']

admin.site.register(Thread, ThreadAdmin)