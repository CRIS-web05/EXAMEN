from django.contrib import admin
from django.urls import path
from peliculas import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('', views.home, name='home'),  
    path('peliculas/', views.peliculas, name='peliculas'),
    path('peliculas/create/', views.create_peliculas, name='create_peliculas'),
    path('peliculas/<int:pelicula_id>/', views.seleccionar_pelicula, name='seleccionar'),
    path('peliculas/<int:pelicula_id>/editar/', views.editar_pelicula, name='editar_pelicula'),
    path('peliculas/<int:pelicula_id>/eliminar/', views.eliminar_pelicula, name='eliminar_pelicula'),path('peliculas/seleccionar/<int:pk>/', views.seleccionar_pelicula, name='seleccionar_pelicula'),
]


