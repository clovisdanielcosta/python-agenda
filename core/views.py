from django.shortcuts import render
from core.models import Evento

# Create your views here.

# caso seja precisa usar uma view para o index importe o 'redirect' tbem de 'shortcurts'
# def index(request):
#      return redirect('/agenda/')

def lista_eventos(request):
        # evento = Evento.objects.get(id=1) #para consulta pelo id
        # Pelo usuário
        # usuario = request.user
        # evento = Evento.objects.filter(usuario=usuario)
        evento = Evento.objects.all() #todos
        dados = {'eventos':evento}
        return render(request, 'agenda.html', dados)

