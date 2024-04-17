from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from webapp.forms import SignUpForm

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Você logou com sucesso")
            return redirect("correcao")
        else:
            messages.success(request, "Falha ao efetuar login")
            return redirect("correcao")
    return render(request, "correcao.html")

def signout(request):
    logout(request)
    messages.success(request, "Você efetuou logout")
    return redirect("correcao")

def signup(request):
    params = {
        "view":{
            "id":"registro",
            "titulo":"Registro de usuário"
        },
    }
        
    if request.method == "POST":
        form = SignUpForm(request.POST)
        params["form"] = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Você criou uma conta com sucesso")
            return redirect("correcao")
    else:
        params["form"] = SignUpForm()

    return render(request, "registro.html", params)


