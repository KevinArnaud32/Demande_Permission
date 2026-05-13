from django.shortcuts import render, redirect, get_object_or_404
from demande.models.repos_maladie_model import ReposMaladie


def repos_maladie_list(request):

    repos_maladies = ReposMaladie.objects.all().order_by('-id')

    context = {
        'repos_maladies': repos_maladies
    }

    return render(
        request,
        'repos_maladie/index.html',
        context
    )

def repos_maladie_create(request):

    if request.method == 'POST':

        date_debut = request.POST.get(
            'date_debut'
        )

        nombre_jours = request.POST.get(
            'nombre_jours'
        )

        justificatif = request.FILES.get(
            'justificatif'
        )

        ReposMaladie.objects.create(
            employe=request.user.employe,
            date_debut=date_debut,
            nombre_jours=nombre_jours,
            justificatif=justificatif
        )

        return redirect(
            'repos_maladie_list'
        )

    return render(
        request,
        'repos_maladie/create.html'
    )


def repos_maladie_detail(request, pk):

    repos_maladie = get_object_or_404(
        ReposMaladie,
        pk=pk
    )

    context = {
        'repos_maladie': repos_maladie
    }

    return render(
        request,
        'repos_maladie/detail.html',
        context
    )



def repos_maladie_update(request, pk):

    repos_maladie = get_object_or_404(
        ReposMaladie,
        pk=pk
    )

    if request.method == 'POST':

        repos_maladie.date_debut = request.POST.get(
            'date_debut'
        )

        repos_maladie.nombre_jours = request.POST.get(
            'nombre_jours'
        )

        justificatif = request.FILES.get(
            'justificatif'
        )

        if justificatif:
            repos_maladie.justificatif = justificatif

        repos_maladie.save()

        return redirect(
            'repos_maladie_list'
        )

    context = {
        'repos_maladie': repos_maladie
    }

    return render(
        request,
        'repos_maladie/update.html',
        context
    )


def repos_maladie_delete(request, pk):

    repos_maladie = get_object_or_404(
        ReposMaladie,
        pk=pk
    )

    repos_maladie.delete()

    return redirect(
        'repos_maladie_list'
    )