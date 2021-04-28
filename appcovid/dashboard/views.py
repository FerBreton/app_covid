from django.shortcuts import render

# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, 'index.html', {})