from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def login_view(request):

    error = None

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "admin":
                return redirect('admin_dashboard')

            elif user.role == "rh":
                return redirect('rh_dashboard')

            elif user.role == "Manager":
                return redirect('manager_dashboard')

            else:
                return redirect('employe_dashboard')

        else:

            error = "Identifiants invalides"

    context = {
        "error": error,
    }

    return render(request,'auth/login.html',context)



@login_required
def logout_view(request):

    logout(request)

    return redirect('login')