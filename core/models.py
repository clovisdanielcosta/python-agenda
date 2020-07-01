from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Evento (models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    local = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Para usar os usuários do Django

    class Meta:
        db_table = 'evento'

    # Para exibir o nome do campo no Django-Admin
    def __str__(self):
        return self.titulo

    # Alterando o formato do horário que aparece na agenda
    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

    # Restaurando o formato do horário para aparecer na Edição dos Eventos
    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    # Verificando se a data está atrasada
    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False