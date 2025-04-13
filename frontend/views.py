from django.shortcuts import render


def home(request):
    dark_mode = request.COOKIES.get('darkMode') == 'enabled'
    return render(request, 'home.html', {'dark_mode': dark_mode})