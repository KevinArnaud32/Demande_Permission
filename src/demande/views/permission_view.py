from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from demande.models.permission_model import Permission
from demande.forms.permission_form import PermissionForm

@login_required
def permission_list(request):

    user = request.user

    if user.role == 'employe':

        permissions = Permission.objects.filter(
            employe=user.employe
        )

    elif user.role == 'manager':

        permissions = Permission.objects.filter(
            employe__superieur=user.employe
        )

    else:

        permissions = Permission.objects.all().order_by('-id')

    context = {
        'permissions': permissions
    }

    return render(request,'permission/index.html',context)


@login_required
def permission_create(request):

    permission_form = PermissionForm()

    if request.method == 'POST':
        permission_form = PermissionForm(request.POST)

        if permission_form.is_valid():
            permission = permission_form.save(commit=False)
            permission.employe = request.user.employe
            permission.save()

            return redirect('permission_list')


    context = {
        'permission_form': permission_form
    }

    return render(request, 'permission/create.html', context)

@login_required
def permission_detail(request, pk):

    permission = get_object_or_404(
        Permission,
        pk=pk
    )

    context = {
        'permission': permission
    }

    return render(
        request,
        'permission/detail.html',
        context
    )

@login_required
def permission_update(request, pk):

    permission = get_object_or_404(
        Permission,
        pk=pk
    )

    permission_form = PermissionForm(instance=permission)

    if request.method == 'POST':

        permission_form = PermissionForm(request.POST, instance=permission)

        if permission_form.is_valid():
            permission_form.save()

            return redirect('permission_list')

    context = {
        'permission_form': permission_form
    }

    return render(
        request,
        'permission/update.html',
        context
    )


@login_required
def permission_delete(request, pk):

    permission = get_object_or_404(
        Permission,
        pk=pk
    )

    if request.method == 'POST':

        permission.delete()

        return redirect(
            'permission_list'
        )

    context = {
        'permission': permission
    }

    return render(
        request,
        'permission/delete.html',
        context
    )