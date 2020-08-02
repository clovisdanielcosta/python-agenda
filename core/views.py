from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.

def login_user(request):
        return render(request, 'login.html')

def logout_user(request):
        logout(request)
        return redirect('/')

def submit_login(request):
        if request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                usuario = authenticate(username=username, password=password)
                if usuario is not None:
                        login(request, usuario)
                        return redirect('/')
                else:
                        messages.error(request, 'Usuário ou Senha inválidos')
        return  redirect('/')

                # caso seja precisa usar uma view para o index importe o 'redirect' tbem de 'shortcurts'
                # def index(request):
                #      return redirect('/agenda/')

# Lista os eventos atuais a partir de duas horas atrás
@login_required(login_url='/login/') # Precisa colocar a barra no início pra não concatenar
def lista_eventos(request):
        # evento = Evento.objects.get(id=1) #para consulta pelo id
        # Pelo usuário
        #evento = Evento.objects.all() #todos
        usuario = request.user
        data_atual = datetime.now() - timedelta(days=1) # Pegando não atrasados de de até 1 hora atrás
        evento = Evento.objects.filter(usuario=usuario,
                                       data_evento__gt=data_atual).order_by('data_evento', 'titulo') # '__lt' para datas menores
        dados = {'eventos':evento}
        return render(request, 'agenda.html', dados)

# Lista todos os eventos
@login_required(login_url='/login/')
def lista_todos_eventos(request):
        usuario = request.user
        evento = Evento.objects.filter(usuario=usuario,
                                       local='Maria').order_by('data_evento', 'titulo') # '__lt' para datas menores
        dados = {'eventos': evento}
        return render(request, 'todos.html', dados)

# Lista apenas os eventos passados
@login_required(login_url='/login/') # Precisa colocar a barra no início pra não concatenar
def lista_eventos_passados(request):
        usuario = request.user
        data_atual = datetime.now() - timedelta(hours=2) # Pegando não atrasados de de até 1 hora atrás
        evento = Evento.objects.filter(usuario=usuario,
                                       data_evento__lt=data_atual).order_by('data_evento', 'titulo') # '__lt' para datas menores
        dados = {'eventos':evento}
        return render(request, 'passado.html', dados)

# Consulta um evento pelo id
@login_required(login_url='/login/')
def evento(request):
        id_evento = request.GET.get('id')
        dados = {}
        if id_evento:
                dados['evento'] = Evento.objects.get(id=id_evento)
        return render(request, 'evento.html', dados)

# Inclui um novo evento
@login_required(login_url='/login/')
def submit_evento(request):
        if request.POST:
                titulo = request.POST.get('titulo')
                data_evento = request.POST.get('data_evento')
                local = request.POST.get('local_evento')
                descricao = request.POST.get('descricao')
                usuario = request.user
                id_evento = request.POST.get('id_evento')
                if id_evento:
                        evento = Evento.objects.get(id=id_evento)
                        if evento.usuario == usuario:
                                evento.titulo = titulo
                                evento.data_evento = data_evento
                                evento.local = local
                                evento.descricao = descricao
                                evento.save()

                        # Também pode ser assim
                        # Evento.objects.filter(id=id_evento).update(titulo=titulo,
                        #                                            data_evento=data_evento,
                        #                                            local=local,
                        #                                            descricao=descricao)
                else:
                        Evento.objects.create(titulo=titulo,
                                              data_evento=data_evento,
                                              local = local,
                                              descricao=descricao,
                                              usuario=usuario)
        return redirect('/')

# Exclui um evento
@login_required(login_url='/login/')
def delete_evento(request, id_evento):
        # Impedindo a deleção de evento de outro usuário
        usuario = request.user
        try:
                evento = Evento.objects.get(id=id_evento)
        except Exception:
                raise Http404()
        if usuario == evento.usuario:
                evento.delete()
        else:
                raise Http404()
        return redirect('/')

# Lista eventos em formato JSON
@login_required(login_url='/login/')
def json_lista_evento(request):
        usuario = request.user
        evento = Evento.objects.all().values('id',
                                             'titulo',
                                             'descricao',
                                             'data_evento',
                                             'local',
                                             'data_criacao')
        return JsonResponse(list(evento), safe=False)
