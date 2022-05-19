from django.forms import ModelForm
from leagueTables.models import Clube, Jogo, Liga

class ClubeForm(ModelForm):
    class Meta:
        model = Clube
        fields = '__all__'
        exclude = ['qualidade']

class LigaForm(ModelForm):
    class Meta:
        model = Liga
        fields = '__all__'
        exclude = []