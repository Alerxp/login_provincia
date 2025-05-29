from django.contrib import admin
from .models import CUEUsuario

@admin.register(CUEUsuario)
class CUEUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'cue', 'anexo', 'modalidad', 'nivel')
    list_filter = ('cue', 'anexo', 'modalidad', 'nivel')
    search_fields = ('user__username', 'cue')

# Personalización del panel admin
admin.site.site_header = "Sistema Provincial"
admin.site.site_title = "Login Provincial"
admin.site.index_title = "Administración"
