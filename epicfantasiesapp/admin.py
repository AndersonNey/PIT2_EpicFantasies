from django.contrib import admin
from .models import Perfil, RedesSociais,Historias,Comentario,Reacao,Denuncias,Categoria,TwoFactorAuth,SystemUtilities


admin.site.register(Perfil)
admin.site.register(RedesSociais)
admin.site.register(Historias)
admin.site.register(Comentario)
admin.site.register(Reacao)
admin.site.register(Denuncias)
admin.site.register(Categoria)
admin.site.register(TwoFactorAuth)
admin.site.register(SystemUtilities)

