from django.shortcuts import render

def metro_home(request):
    return render(request, 'metro/metro_home.html') 