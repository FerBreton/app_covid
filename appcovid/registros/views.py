from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import *
from .models import *
from django.contrib import messages
import datetime

# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, 'index.html', {})

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