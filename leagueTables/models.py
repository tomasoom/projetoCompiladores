from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Clube(models.Model):
    nome = models.CharField(max_length=30)        #no Construtor
    qualidade = models.IntegerField(default=50)   #no Construtor
    jogosDisputados = models.IntegerField(default = 0, editable=False)
    vitorias = models.IntegerField(default=0, editable=False)
    empates = models.IntegerField(default=0, editable=False)
    derrotas = models.IntegerField(default=0, editable=False)
    golosMarcados = models.IntegerField(default=0, editable=False)
    golosSofridos = models.IntegerField(default=0, editable=False)
    diferencaDeGolos = models.IntegerField(default=0, editable=False)
    pontos = models.IntegerField(default=0, editable=False)
    nacionalidade = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Liga(models.Model):
    nome = models.CharField(max_length=30, default="liga")
    listaEquipas = models.ManyToManyField(Clube)
    #jornadas = models.ManyToManyField(Jornada)

    def __str__(self):
        return self.nome


class Jornada(models.Model):
    #listaJogos = models.ManyToManyField(Jogo)
    liga = models.ForeignKey(Liga, on_delete=models.CASCADE, related_name='liga')        

    def __str__(self):
        return f"Jornada x"
        

class Jogo(models.Model):
    equipaCasa = models.ForeignKey(Clube, on_delete=models.CASCADE, related_name='equipaCasa')
    equipaFora = models.ForeignKey(Clube, on_delete=models.CASCADE, related_name='equipaFora')
    golosCasa = models.IntegerField(default=0, editable=False)
    golosFora = models.IntegerField(default=0, editable=False)
    concluido = models.BooleanField(default=False, editable=False)
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE, related_name='jornada')
    
    def __str__(self):
        return f"{self.equipaCasa} vs {self.equipaFora}"


    



