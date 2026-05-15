from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from demande.models.validation_model import Validation
from demande.models.permission_model import Permission
from demande.models.conges_model import Conges
from demande.models.repos_maladie_model import ReposMaladie


def validation_list(request):

    validations = Validation.objects.all().order_by(
        '-id'
    )

    context = {
        'validations': validations
    }

    return render(
        request,
        'validation/index.html',
        context
    )


def validate_permission(request, pk):

    permission = get_object_or_404(
        Permission,
        pk=pk
    )

    if request.method == 'POST':

        decision = request.POST.get(
            'decision'
        )

        commentaire = request.POST.get(
            'commentaire'
        )

        Validation.objects.create(
            type_demande='permission',
            demande_id=permission.id,
            decision=decision,
            validateur=request.user,
            commentaire=commentaire
        )

        if decision == 'ACCEPTEE':
            permission.statut = 'accepte'
        else:
            permission.statut = 'refuse'

        permission.save()

        return redirect(
            'permission_list'
        )

    context = {
        'permission': permission
    }

    return render(
        request,
        'validation/permission_validation.html',
        context
    )


def validate_conge(request, pk):

    conge = get_object_or_404(
        Conges,
        pk=pk
    )

    if request.method == 'POST':

        decision = request.POST.get(
            'decision'
        )

        commentaire = request.POST.get(
            'commentaire'
        )

        Validation.objects.create(
            type_demande='conge',
            demande_id=conge.id,
            decision=decision,
            validateur=request.user,
            commentaire=commentaire
        )

        if decision == 'ACCEPTEE':
            conge.statut = 'accepte'
        else:
            conge.statut = 'refuse'

        conge.save()

        return redirect(
            'conge_list'
        )

    context = {
        'conge': conge
    }

    return render(
        request,
        'validation/conge_validation.html',
        context
    )



def validate_repos_maladie(request, pk):

    repos = get_object_or_404(
        ReposMaladie,
        pk=pk
    )

    if request.method == 'POST':

        decision = request.POST.get(
            'decision'
        )

        commentaire = request.POST.get(
            'commentaire'
        )

        Validation.objects.create(
            type_demande='repos_maladie',
            demande_id=repos.id,
            decision=decision,
            validateur=request.user,
            commentaire=commentaire
        )

        if decision == 'ACCEPTEE':
            repos.statut = 'accepte'
        else:
            repos.statut = 'refuse'

        repos.save()

        return redirect(
            'repos_maladie_list'
        )

    context = {
        'repos': repos
    }

    return render(
        request,
        'validation/repos_validation.html',
        context
    )