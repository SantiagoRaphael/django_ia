from django.shortcuts import render, redirect
from django.contrib import messages
import openai
from webapp.models import Registros

OPENAI_KEY = ""

linguagens = [
    "c",
    "clike",
    "cpp",
    "csharp",
    "css",
    "csv",
    "django",
    "go",
    "graphql",
    "html",
    "java",
    "javascript",
    "markup",
    "markup-templating",
    "perl",
    "php",
    "python",
    "ruby",
    "rust",
    "sql",
    "xml-doc",
    "yaml"]

def correcao(request):
    params = {
        "view":{
            "id":"correcao",
            "titulo":"Correção de Código"
        },
        "linguagens":linguagens
    }
    if request.method == "POST":
        params["code"] = request.POST["code"] #code vem da textarea do forms
        params["linguagem"] = request.POST["linguagem"]
        if params["linguagem"] == "Selecione a linguagem de programação":
            messages.success(request, "Por favor, selecione uma linguagem!")
            return render(request, "correcao.html", params)
        #aqui fazemos a request para openai
        openai.api_key = OPENAI_KEY
        openai.Model.list()
        try:
            response = openai.Completion.create(
                engine = "gpt-3.5-turbo-instruct",
                prompt = f"Responde only with code. Fix this {params['linguagem']} code: {params['code']}",
                temperature = 0,
                max_tokens = 1000,
                frequency_penalty = 0.0,
                presence_penalty = 0.0
            )
            params["response"] = response["choices"][0]["text"].strip()
        
            #salva o registro no historico
            registro = Registros(
                pergunta=params["code"],
                respostas=params["response"],
                linguagem=params["linguagem"],
                user=request.user,
                tipo=params["view"]["id"]
            )
            registro.save()
        except Exception as e:
            params["code"] = e

    return render(request, "correcao.html", params)

def criacao(request):
    params = {
        "view":{
            "id":"criacao",
            "titulo":"Criação de Código"
        },
        "linguagens":linguagens
    }
    if request.method == "POST":
        params["code"] = request.POST["code"] #code vem da textarea do forms
        params["linguagem"] = request.POST["linguagem"]
        if params["linguagem"] == "Selecione a linguagem de programação":
            messages.success(request, "Por favor, selecione uma linguagem!")
            return render(request, "criacao.html", params)
        #aqui fazemos a request para openai
        openai.api_key = OPENAI_KEY
        openai.Model.list()
        try:
            response = openai.Completion.create(
                engine = "gpt-3.5-turbo-instruct",
                prompt = f"Responde only with code. code: {params['code']} in {params['linguagem']}",
                temperature = 0,
                max_tokens = 1000,
                frequency_penalty = 0.0,
                presence_penalty = 0.0
            )
            params["response"] = response["choices"][0]["text"].strip()
            #salva o registro no historico
            registro = Registros(
                pergunta=params["code"],
                respostas=params["response"],
                linguagem=params["linguagem"],
                user=request.user,
                tipo=params["view"]["id"]
            )
            registro.save()
        except Exception as e:
            params["code"] = e
        

    return render(request, "criacao.html", params)

def geral(request):
    params = {
        "view":{
            "id":"geral",
            "titulo":"Perguntas Gerais"
        },
        "linguagens":linguagens
    }
    if request.method == "POST":
        params["code"] = request.POST["code"] 
        #aqui fazemos a request para openai
        openai.api_key = OPENAI_KEY
        openai.Model.list()
        try:
            response = openai.Completion.create(
                engine = "gpt-3.5-turbo-instruct",
                prompt = f"{params['code']}",
                temperature = 0,
                max_tokens = 1000,
                frequency_penalty = 0.0,
                presence_penalty = 0.0
            )
            params["response"] = response["choices"][0]["text"].strip()
            #salva o registro no historico
            registro = Registros(
                pergunta=params["code"],
                respostas=params["response"],
                linguagem="geral",
                user=request.user,
                tipo=params["view"]["id"]
            )
            registro.save()
        except Exception as e:
            params["code"] = e
        

    return render(request, "geral.html", params)

def historico(request):
    registros = Registros.objects.filter(user_id=request.user.id)
    params = {
    "titulo":"Historico",
    "registros":registros
    }
    return render(request, "historico.html", params)


def deletar_registro(request, id_do_registro):
    registro = Registros.objects.get(pk=id_do_registro)
    registro.delete()
    messages.sucess(request, "Registro deletado")
    return redirect("historico")