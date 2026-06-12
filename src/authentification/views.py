from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def login_view(request):

    if request.user.is_authenticated:
        if request.user.role == "admin":
            return redirect('admin_dashboard')
        elif request.user.role == "rh":
            return redirect('rh_dashboard')
        elif request.user.role == "manager":
            return redirect('manager_dashboard')
        elif request.user.role == 'employe':
            return redirect('employe_dashboard')


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

            if user.first_login:
                return redirect('change_password_first')

            if user.role == "admin":
                return redirect('admin_dashboard')

            elif user.role == "rh":
                return redirect('rh_dashboard')

            elif user.role == "manager":
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



@login_required
def change_password_first(request):

    if request.method == "POST":

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:

            user = request.user
            user.set_password(password1)

            user.first_login = False
            user.save()

            return redirect("login")

        else:

            context = {
                'error': "Les mots de passe ne correspondent pas",
            }

            return render(request, "auth/change_password.html")

    return render(request, "auth/change_password.html")