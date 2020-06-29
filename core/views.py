from django.shortcuts import render, HttpResponse

# Create your views here.
def consulta_evento(request, titulo_evento):

    data_ev = HttpResponse.Evento.get(titulo=titulo_evento)

    return HttpResponse('O Evento {} será em' .format(data_ev))



