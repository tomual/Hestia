from django.contrib import admin

from .models import Group, Membership

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 3

class GroupAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]

admin.site.register(Group, GroupAdmin)