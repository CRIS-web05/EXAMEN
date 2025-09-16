from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import PeliculaForm
from .models import Pelicula

def home(request):
    return render(request, "home.html")

def peliculas(request):
    peliculas = Pelicula.objects.filter(user=request.user)
    return render(request, "peliculas.html", {"peliculas": peliculas})

def seleccionar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id, user=request.user)
    if request.method == "POST":
        return redirect('peliculas')
    return render(request, 'seleccionar.html', {'pelicula': pelicula})

def create_peliculas(request):
    if request.method == "GET":
        return render(request, "create_peliculas.html", {"form": PeliculaForm()})
    else:
        try:
            form = PeliculaForm(request.POST)
            new_pelicula = form.save(commit=False)
            new_pelicula.user = request.user
            new_pelicula.save()
            return redirect("peliculas")
        except ValueError:
            return render(request, "create_peliculas.html", {
                "form": PeliculaForm(),
                "error": "Por favor ingrese datos válidos"
            })

def editar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, pk=pelicula_id, user=request.user)
    if request.method == "GET":
        form = PeliculaForm(instance=pelicula)
        return render(request, "editar.html", {"form": form, "pelicula": pelicula})
    else:
        try:
            form = PeliculaForm(request.POST, instance=pelicula)
            if form.is_valid():
                form.save()
                return redirect("peliculas")
            else:
                return render(request, "editar.html", {"form": form, "pelicula": pelicula, "error": "Datos inválidos"})
        except ValueError:
            return render(request, "editar.html", {"form": form, "pelicula": pelicula, "error": "Error al editar la película"})

def eliminar_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id, user=request.user)
    if request.method == "POST":
        pelicula.delete()
        return redirect("peliculas")
    return render(request, "eliminar.html", {"pelicula": pelicula})

def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                "form": AuthenticationForm(),
                "error": "Usuario o contraseña incorrecta"
            })
        else:
            login(request, user)
            return redirect("peliculas")

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect("peliculas")
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": UserCreationForm(),
                    "error": "Error al crear el usuario"
                })
        else:
            return render(request, 'signup.html', {
                "form": UserCreationForm(),
                "error": "Error, las contraseñas no coinciden"
})

# Create your views here.