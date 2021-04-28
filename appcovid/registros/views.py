import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import *
from .models import *
import datetime
from django.contrib import messages

# Create your views here.

class Home(View):
    def get(self, request):
        cov = 'https://covidtracking.com/api/states/'
        response = requests.get(cov)
        x = 'https://api.covidtracking.com/v1/us/current.json'
        response1 = requests.get(x)

        estados = ['AK', 'AL', 'AR', 'AS', 'AZ']
        datos = []

        for i in response.json():
            for j in estados:
                if i['state'] == j:
                    datos.append(i['positive'])

        context = {
            'response' : response.json(),
            'US' : response1.json(),
            'data' : datos,
        }
        return render(request, 'index.html', context)

class Entrada(View):
    def get(self, request):
        form = RegistroForm()
        context = {'form': form}
        return render(request, 'registro.html', context)
    
    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            llenado = form.save(commit=False)
            registros = Registro.objects.filter(email=llenado.email, timestamp_in__gte=datetime.date.today(), timestamp_out=None)
            if registros:
                messages.error(request, 'Los resultados de este correo ya están entregados')
                return redirect('registro')
            else:
                llenado.save()
                messages.success(request, 'Registro guardado. Vea sus resultados')
                return redirect('index')
        else:
            context = {'form': form}
            messages.error(request, 'Los datos ingresados son incorrectos. Intente de nuevo.')
            return render(request, 'registro.html', context)

class Resultados(View):
    def get(self, request):
        form = ResultadoForm()
        context = {'form': form}
        return render(request, 'resultados.html', context)

    def post(self, request):
        form = ResultadoForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)

            registros = Registro.objects.filter(email=entrega.email, timestamp_out=None, timestamp_in__gte=datetime.date.today())
            if registros:
                resultado = Registro.objects.get(pk=registros[0].id)
                resultado.timestamp_out = datetime.datetime.now()
                if resultado.temperatura > 37.5 or resultado.oxigenacion < 90:
                    resultado.estado = "Positivo"
                    resultado.save()
                    messages.error(request, 'Sus resultados son positivos. Visite a un médico lo antes posible.')
                    return redirect('index')
                else:
                    resultado.estado = "Negativo"
                    resultado.save()
                    messages.success(request, 'Sus resultados son negativos. Siga cuidandose')
                    return redirect('index')
            else:
                messages.error(request, 'Este correo aun no tiene datos. Intente de nuevo.')
                return redirect('resultados')
        else:
            context = {'form': form}
            messages.error(request, 'Los datos ingresados son incorrectos. Intente de nuevo.')
            return render(request, 'salida.html', context)

class Historial(View):
    def get(self, request):
        registros = Registro.objects.all()

        context = {'registros' : registros}
        return render(request, 'historial.html', context)