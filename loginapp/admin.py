from django.contrib import admin
from .models import CUEUsuario

admin.site.register(CUEUsuario)
admin.site.site_header = "Sistema Provincial"
admin.site.site_title = "Login Provincial"
admin.site.index_title = "Administración"
