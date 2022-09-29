from django.shortcuts import render

# Create your views here.
def flightviews(request):
    return render(request, "main.html")