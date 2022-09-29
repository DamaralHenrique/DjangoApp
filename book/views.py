from django.shortcuts import render

# Create your views here.
def bookviews(request):
    return render(request, "FIRST.html")