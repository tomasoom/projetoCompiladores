from django.urls import path
from . import views

app_name= "leagueTables"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('novoClube', views.addClube_view, name="novoClube"),
    path('novaLiga', views.addLiga_view, name="novaLiga"),
    path('liga/<int:liga_id>', views.liga_view, name="liga"),
    path('jogo/<int:jogo_id>', views.simulaJogo_view, name='simulaJogo'),
    path('limpa/<int:liga_id>', views.clearLiga_view, name="clear"),
    path('simulaLiga/<int:liga_id>', views.simulaLiga_view, name='simulaLiga'),
    path('simulaJornada/<int:jornada_id>', views.simulaJornada_view, name='simulaJornada')
]