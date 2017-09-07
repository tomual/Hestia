from django.contrib import admin

from .models import Thread, Response

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 3

class ThreadAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'message']}),
        ('Date information', {'fields': ['posted']}),
    ]
    inlines = [ResponseInline]
    list_display = ('title', 'posted', 'was_posted_recently')
    list_filter = ['posted']
    search_fields = ['title', 'message']

admin.site.register(Thread, ThreadAdmin)