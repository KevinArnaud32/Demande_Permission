from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from demande.models.conges_model import Conges


def conge_list(request):

    conges = Conges.objects.all().order_by('-id')

    context = {
        'conges': conges
    }

    return render(
        request,
        'conge/index.html',
        context
    )


def conge_create(request):

    if request.method == 'POST':

        date_debut = request.POST.get('date_debut')

        nombre_jours = request.POST.get(
            'nombre_jours'
        )

        Conges.objects.create(
            employe=request.user.employe,
            date_debut=date_debut,
            nombre_jours=nombre_jours
        )

        return redirect('conge_list')

    return render(
        request,
        'conge/create.html'
    )


def conge_detail(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    context = {
        'conge': conge
    }

    return render(
        request,
        'conge/detail.html',
        context
    )


def conge_update(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    if request.method == 'POST':

        conge.date_debut = request.POST.get(
            'date_debut'
        )

        conge.nombre_jours = request.POST.get(
            'nombre_jours'
        )

        conge.save()

        return redirect('conge_list')

    context = {
        'conge': conge
    }

    return render(
        request,
        'conge/update.html',
        context
    )


def conge_delete(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    conge.delete()

    return redirect('conge_list')