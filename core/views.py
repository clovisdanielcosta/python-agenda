from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from  django.contrib import messages

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

@login_required(login_url='/login/') # Precisa colocar a barra no início pra não concatenar
def lista_eventos(request):
        # evento = Evento.objects.get(id=1) #para consulta pelo id
        # Pelo usuário
        #evento = Evento.objects.all() #todos
        usuario = request.user
        evento = Evento.objects.filter(usuario=usuario)
        dados = {'eventos':evento}
        return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
        return render(request, 'evento.html')

@login_required(login_url='/login/')
def submit_evento(request):
        if request.POST:
                titulo = request.POST.get('titulo')
                data_evento = request.POST.get('data_evento')
                local = request.POST.get('local_evento')
                descricao = request.POST.get('descricao')
                usuario = request.user
                Evento.objects.create(titulo=titulo,
                                      data_evento=data_evento,
                                      local = local,
                                      descricao=descricao,
                                      usuario=usuario)
        return redirect('/')
