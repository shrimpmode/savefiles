from django.contrib import admin

# Register your models here.

from .models import Folder, File


class FolderAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['is_root', 'user']


admin.site.register(Folder, FolderAdmin)
admin.site.register(File)
