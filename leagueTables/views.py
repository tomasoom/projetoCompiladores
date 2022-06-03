from msilib.schema import Class
from pickle import FALSE
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
import random

# Create your views here.

def home_view(request):
    context = {"ligas": Liga.objects.all()}
    return render(request, 'leagueTables/home.html', context)

def addClube_view(request):
    form = ClubeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('leagueTables:home'))

    context = {'form': form}

    return render(request, 'leagueTables/novoClube.html', context)

def addLiga_view(request):
    form = LigaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('leagueTables:home'))

    context = {'form': form}

    return render(request, 'leagueTables/novaLiga.html', context)

def liga_view(request, liga_id):
    liga = Liga.objects.get(pk=liga_id)
    liga.save()

    if not Classificacao.objects.filter(liga=liga):
        for equipa in liga.listaEquipas.all():
            classificacao = Classificacao(clube=equipa, liga=liga)
            classificacao.save()

    if not Jogo.objects.filter(jornada__liga=liga):
        if len(liga.listaEquipas.all()) % 2 == 1: players = liga.listaEquipas.all() + [None]
        # manipulate map (array of indexes for list) instead of list itself
        # this takes advantage of even/odd indexes to determine home vs. away
        n = len(liga.listaEquipas.all())
        map = list(range(n))
        mid = n // 2
        for i in range(n - 1):
            l1 = map[:mid]
            l2 = map[mid:]
            l2.reverse()
            nJornada = Jornada(liga=liga)
            nJornada.save()

            for j in range(mid):
                t1 = liga.listaEquipas.all()[l1[j]]
                t2 = liga.listaEquipas.all()[l2[j]]
                if j == 0 and i % 2 == 1:
                    # flip the first match only, every other round
                    # (this is because the first match always involves the last player in the list)
                    #jornada = Jornada()
                    #jornada.save()
                    jogo = Jogo(equipaCasa=t2, equipaFora=t1, jornada=nJornada)
                    jogo.save()
                    nJornada.save()
                    #nJornada.listaJogos.add(jogo)
                    #jogo.jornada = nJornada
                    #nJornada.save()
                    #jogo.save()

                else:
                    #jornada = Jornada()
                    #jornada.save()
                    jogo = Jogo(equipaCasa=t1, equipaFora=t2, jornada=nJornada)
                    jogo.save()
                    nJornada.save()
                    #nJornada.listaJogos.add(jogo)
                    jogo.jornada = nJornada
                    nJornada.save()
                    jogo.save()

            #liga.jornadas.add(nJornada)
            #nJornada.liga = liga
            #nJornada.save()
            liga.save()

            # rotate list by n/2, leaving last element at the end
            map = map[mid:-1] + map[:mid] + map[-1:]

        #nJ = len(liga.jornadas.all())
        nJ = len(Jornada.objects.filter(liga=liga))

        '''
        for i in range(0, nJ):
            nJornada2 = Jornada(liga=liga)
            nJornada2.save()
            for j in range(0, int(len(liga.listaEquipas.all()) / 2)):
                jogo2 = Jogo(equipaCasa=liga.jornadas.all()[i].listaJogos.all()[j].equipaFora, equipaFora=liga.jornadas.all()[i].listaJogos.all()[j].equipaCasa)
                jogo2.save()
                nJornada2.listaJogos.add(jogo2)
                nJornada2.save()

            liga.jornadas.add(nJornada2)
            liga.save()
        '''

        '''
        for jogo in Jogo.objects.filter(jornada__liga=liga):
            nJornada2 = Jornada(liga=liga)
            nJornada2.save()
            jogo2 = Jogo(equipaCasa=jogo.equipaFora, equipaFora = jogo.equipaCasa, jornada=nJornada2)
            nJornada2.save()
            jogo2.save()
        '''

        #Jornada.objects.all().order_by('?')

        for jornada in Jornada.objects.filter(liga=liga):
            nJornada2 = Jornada(liga=liga)
            nJornada2.save()
            for jogo in Jogo.objects.filter(jornada=jornada):
                jogo2 = Jogo(equipaCasa=jogo.equipaFora, equipaFora=jogo.equipaCasa, jornada=nJornada2)
                nJornada2.save()
                jogo2.save()

        
        

    liga.save()
    i = 0
    #listaEquipasOrdenada = liga.listaEquipas.all().order_by('-pontos', '-diferencaDeGolos', '-golosMarcados')
    listaEquipasOrdenada = Classificacao.objects.filter(liga=liga).order_by('-pontos', '-diferencaDeGolos', '-golosMarcados')
    
    context = {'liga': liga, liga_id: liga_id, 'jogos': Jogo.objects.filter(jornada__liga=liga), 'classificacoes': listaEquipasOrdenada, 'jornadas': Jornada.objects.filter(liga=liga)}
    return render(request, 'leagueTables/liga.html', context)
  

def simulaJogo_view(request, jogo_id):
    jogo = Jogo.objects.get(pk=jogo_id)

    if jogo.concluido == False:

        

        jogo.concluido = True
        jogo.save()
        equipaC = jogo.equipaCasa
        equipaC.save()
        equipaF = jogo.equipaFora
        equipaF.save()

        classificacaoCasa = Classificacao.objects.get(clube=equipaC, liga=jogo.jornada.liga)
        classificacaoCasa.save()
        classificacaoFora = Classificacao.objects.get(clube=equipaF, liga=jogo.jornada.liga)
        classificacaoFora.save()

        jogo.golosCasa = 0
        jogo.save()
        jogo.golosFora = 0
        jogo.save()


        #self.golosCasa = 0
        #self.golosFora = 0

        ponderadorCasa = jogo.equipaCasa.qualidade ** 2.50 / jogo.equipaFora.qualidade ** 2.50
        ponderadorFora = jogo.equipaFora.qualidade ** 2.50 / jogo.equipaCasa.qualidade ** 2.50

        lista1 = [i for i in range(1, int((5000 + 1) * ponderadorFora))]
        lista2 = [i for i in range(1, int((5000 + 1) * ponderadorCasa))]

        for tempo in range(1, 90 + 1):
            if random.choice(lista1) <= jogo.equipaCasa.qualidade:
                jogo.golosCasa += 1
                jogo.save()
                classificacaoCasa.golosMarcados += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoFora.golosSofridos += 1
                classificacaoFora.save()
                jogo.save()
                classificacaoCasa.diferencaDeGolos += 1
                classificacaoCasa.save()
                classificacaoFora.diferencaDeGolos -= 1
                classificacaoFora.save()
            elif random.choice(lista2) <= jogo.equipaFora.qualidade:
                jogo.golosFora += 1
                jogo.save()
                classificacaoFora.golosMarcados += 1
                classificacaoFora.save()
                jogo.save()
                classificacaoCasa.golosSofridos += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoCasa.diferencaDeGolos -= 1
                classificacaoCasa.save()
                classificacaoFora.diferencaDeGolos += 1
                classificacaoFora.save()

        #string = f"{ponderadorCasa}  {self.equipaCasa.nome} {self.golosCasa} - {self.golosFora} {self.equipaFora.nome}  {ponderadorFora}"

        if jogo.golosCasa > jogo.golosFora:
            classificacaoCasa.vitorias += 1
            classificacaoCasa.save()
            jogo.save()
            classificacaoCasa.pontos += 3
            classificacaoCasa.save()
            jogo.save()
            classificacaoFora.derrotas += 1
            classificacaoFora.save()
            jogo.save()
            classificacaoCasa.jogosDisputados += 1
            classificacaoCasa.save()
            jogo.save()
            classificacaoFora.jogosDisputados += 1
            classificacaoFora.save()
            jogo.save()

        elif jogo.golosCasa == jogo.golosFora:
            classificacaoCasa.empates += 1
            classificacaoCasa.save()
            jogo.save()
            classificacaoCasa.pontos += 1
            classificacaoCasa.save()
            jogo.save()
            classificacaoFora.empates += 1
            classificacaoFora.save()
            jogo.save()
            classificacaoFora.pontos += 1
            classificacaoFora.save()
            jogo.save()
            classificacaoCasa.jogosDisputados += 1
            classificacaoCasa.save()
            jogo.save()
            classificacaoFora.jogosDisputados += 1
            classificacaoFora.save()
            jogo.save()
        else:
            classificacaoCasa.derrotas += 1
            classificacaoCasa.save()
            jogo.save()
            classificacaoFora.vitorias += 1
            classificacaoFora.save()
            jogo.save()
            classificacaoFora.pontos += 3
            classificacaoFora.save()
            jogo.save()
            classificacaoCasa.jogosDisputados += 1
            classificacaoCasa.save()
            jogo.save()
            classificacaoFora.jogosDisputados += 1
            classificacaoFora.save()
            jogo.save()
        
        return HttpResponseRedirect(reverse('leagueTables:home'))
        #context = {'jogo': jogo, jogo_id: jogo_id}
        #return render(request, 'leagueTables/liga.html', context)
    return HttpResponseRedirect(reverse('leagueTables:home'))


def clearLiga_view(request, liga_id):
    liga = Liga.objects.get(pk=liga_id)
    for jogo in Jogo.objects.filter(jornada__liga=liga, concluido=True):
        jogo.golosCasa=0
        jogo.save()
        jogo.golosFora=0
        jogo.save()
        jogo.concluido=False
        jogo.save()
    
    #liga.listaEquipas.all().update(jogosDisputados=0, vitorias=0, empates=0, derrotas=0, golosMarcados=0, golosSofridos=0, diferencaDeGolos=0, pontos=0)
    Classificacao.objects.filter(liga=liga).update(jogosDisputados=0, vitorias=0, empates=0, derrotas=0, golosMarcados=0, golosSofridos=0, diferencaDeGolos=0, pontos=0)
    #context = {'liga': liga.listaEquipas.order_by('-pontos', '-diferencaDeGolos')}

    return HttpResponseRedirect(reverse('leagueTables:home'))

def simulaLiga_view(request, liga_id):
    liga = Liga.objects.get(pk=liga_id)
    for jogo in Jogo.objects.filter(jornada__liga=liga):
        if jogo.concluido == False:

            jogo.concluido = True
            jogo.save()
            equipaC = jogo.equipaCasa
            equipaC.save()
            equipaF = jogo.equipaFora
            equipaF.save()

            #classificacaoCasa = Classificacao(clube=equipaC, liga=liga)
            #classificacaoCasa.save()
            classificacaoCasa = Classificacao.objects.get(clube=equipaC, liga=liga)
            classificacaoCasa.save()
            classificacaoFora = Classificacao.objects.get(clube=equipaF, liga=liga)
            classificacaoFora.save()

            jogo.golosCasa = 0
            jogo.save()
            jogo.golosFora = 0
            jogo.save()
            #self.golosCasa = 0
            #self.golosFora = 0

            ponderadorCasa = jogo.equipaCasa.qualidade ** 2.50 / jogo.equipaFora.qualidade ** 2.50
            ponderadorFora = jogo.equipaFora.qualidade ** 2.50 / jogo.equipaCasa.qualidade ** 2.50

            lista1 = [i for i in range(1, int((5000 + 1) * ponderadorFora))]
            lista2 = [i for i in range(1, int((5000 + 1) * ponderadorCasa))]

            for tempo in range(1, 90 + 1):
                if random.choice(lista1) <= jogo.equipaCasa.qualidade:
                    jogo.golosCasa += 1
                    jogo.save()
                    classificacaoCasa.golosMarcados += 1
                    classificacaoCasa.save()
                    jogo.save()
                    classificacaoFora.golosSofridos += 1
                    classificacaoFora.save()
                    jogo.save()
                    classificacaoCasa.diferencaDeGolos += 1
                    classificacaoCasa.save()
                    classificacaoFora.diferencaDeGolos -= 1
                    classificacaoFora.save()
                elif random.choice(lista2) <= jogo.equipaFora.qualidade:
                    jogo.golosFora += 1
                    jogo.save()
                    classificacaoFora.golosMarcados += 1
                    classificacaoFora.save()
                    jogo.save()
                    classificacaoCasa.golosSofridos += 1
                    classificacaoCasa.save()
                    jogo.save()
                    classificacaoCasa.diferencaDeGolos -= 1
                    classificacaoCasa.save()
                    classificacaoFora.diferencaDeGolos += 1
                    classificacaoFora.save()

            #string = f"{ponderadorCasa}  {self.equipaCasa.nome} {self.golosCasa} - {self.golosFora} {self.equipaFora.nome}  {ponderadorFora}"

            if jogo.golosCasa > jogo.golosFora:
                classificacaoCasa.vitorias += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoCasa.pontos += 3
                classificacaoCasa.save()
                jogo.save()
                classificacaoFora.derrotas += 1
                classificacaoFora.save()
                jogo.save()
                classificacaoCasa.jogosDisputados += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoFora.jogosDisputados += 1
                classificacaoFora.save()
                jogo.save()

            elif jogo.golosCasa == jogo.golosFora:
                classificacaoCasa.empates += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoCasa.pontos += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoFora.empates += 1
                classificacaoFora.save()
                jogo.save()
                classificacaoFora.pontos += 1
                classificacaoFora.save()
                jogo.save()
                classificacaoCasa.jogosDisputados += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoFora.jogosDisputados += 1
                classificacaoFora.save()
                jogo.save()
            else:
                classificacaoCasa.derrotas += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoFora.vitorias += 1
                classificacaoFora.save()
                jogo.save()
                classificacaoFora.pontos += 3
                classificacaoFora.save()
                jogo.save()
                classificacaoCasa.jogosDisputados += 1
                classificacaoCasa.save()
                jogo.save()
                classificacaoFora.jogosDisputados += 1
                classificacaoFora.save()
                jogo.save()
    
    return HttpResponseRedirect(reverse('leagueTables:home'))
