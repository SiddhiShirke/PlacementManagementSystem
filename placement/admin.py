from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import signup,studentData,company_details,appliedStudents,training_skill,shortlisted

class placementad(UserAdmin):
    pass
#
# class CustomUserAdmin(UserAdmin):
#     model = signup
#     list_display = ('email', 'is_staff', 'is_active',)
#     list_filter = ('email', 'is_staff', 'is_active',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)


admin.site.register(signup)
admin.site.register(studentData)
admin.site.register(company_details)
admin.site.register(appliedStudents)
admin.site.register(training_skill)
admin.site.register(shortlisted)
