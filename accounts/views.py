from django.shortcuts import render

# Create your views here.

def signup(request):
    if request.method == "POST":
        #
    return render(request, 'accounts/signup.html')

def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    # TODO need to route to homepage
    return render(request, 'accounts/signup.html')