from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

# Create your views here.
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')
        else:
            context = {
                "error": "Identifiants incorrects"
            }

            return render(
                request,
                'auth/login.html',
                context
            )

    return render(
        request,
        'auth/login.html'
    )



def logout_view(request):

    logout(request)

    return redirect('login')