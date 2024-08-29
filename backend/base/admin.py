from django.contrib import admin
from base.models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_select_related = ("profile",)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "gender", "privacy_status")
    search_fields = ("user__username", "first_name", "last_name", "gender")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project)
admin.site.register(ProjectContributorMap)
