from django.contrib import admin
from core.models import Evento


# Register your models here.


class EventoAdmin(admin.ModelAdmin):
    # Para definir quais colunas mostrar na tabela
    list_display = ('id', 'titulo', 'data_evento', 'local', 'data_criacao', 'usuario')
    # Adicionando filtros para busca na página do Django-Admin
    list_filter = ('titulo', 'usuario', 'data_evento', 'local')


admin.site.register(Evento, EventoAdmin)
