from django.shortcuts import render, redirect, get_object_or_404
from demande.models.permission_model import Permission

def permission_list(request):

    permissions = Permission.objects.all().order_by('-id')

    context = {
        'permissions': permissions
    }

    return render(request,'permission/index.html',context)


def permission_create(request):

    if request.method == 'POST':
        motif = request.POST.get('motif')
        heure_sortie = request.POST.get('heure_sortie')
        nombre_minute = request.POST.get('nombre_minute')

        Permission.objects.create(
            employe=request.user.employe,
            motif=motif,
            heure_sortie=heure_sortie,
            nombre_minute=nombre_minute
        )

        return redirect('permission_list')

    return render(request, 'permission/create.html')


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


def permission_update(request, pk):

    permission = get_object_or_404(
        Permission,
        pk=pk
    )

    if request.method == 'POST':

        permission.motif = request.POST.get('motif')

        permission.heure_sortie = request.POST.get(
            'heure_sortie'
        )

        permission.nombre_minute = request.POST.get(
            'nombre_minute'
        )

        permission.save()

        return redirect('permission_list')

    context = {
        'permission': permission
    }

    return render(
        request,
        'permission/update.html',
        context
    )



def permission_delete(request, pk):

    permission = get_object_or_404(
        Permission,
        pk=pk
    )

    permission.delete()

    return redirect('permission_list')