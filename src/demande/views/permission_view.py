from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.decorators import role_required
from demande.models.permission_model import Permission
from demande.forms.permission_form import PermissionForm
from demande.models.validation_model import Validation


@login_required
def permission_list(request):

    user = request.user

    permissions = Permission.objects.none()

    if user.role == 'employe':
        permissions = Permission.objects.filter(employe=request.user.employe)
    elif user.role == 'manager':
        permissions = Permission.objects.filter(employe__departement=user.employe.departement).exclude(employe=user.employe)
    elif user.role in ['rh', 'admin']:
        permissions = Permission.objects.all()

    context = {
        'permissions': permissions.order_by('-id')
    }

    return render(request,'permission/index.html', context)




@login_required()
@role_required('employe')
def permission_create(request):

    user = request.user

    permission_form = PermissionForm()

    if request.method == 'POST':
        permission_form = PermissionForm(request.POST)

        if permission_form.is_valid():
            permission = permission_form.save(commit=False)
            permission.employe = user.employe
            permission.save()
            messages.success(request, "Demande de permission envoyée avec succès.")
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

    validations = Validation.objects.filter(
        type_demande='permission',
        demande_id=permission.id).order_by('-date_creation')

    context = {
        'permission': permission,
        'validations': validations,
    }

    return render(request,'permission/detail.html', context)



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

    permission = get_object_or_404(Permission, pk=pk)

    permission.delete()

    return redirect('permission_list')


@login_required
def valider_permission(request, pk):

    permission = get_object_or_404(Permission, pk=pk)

    user = request.user

    # verification du role utilisateur

    if request.user.role != 'manager':
        return redirect('permission_list')

    if permission.employe.departement != user.employe.departement:
        return redirect("permission_list")

    # Empêcher de valider sa propre demande
    if permission.employe == user.employe:
        messages.error(request, "Vous ne pouvez pas valider votre propre demande.")
        return redirect("permission_detail", pk=pk)


    # Vérifier le statut
    if permission.statut != "en attente":
        messages.warning(request, "Cette demande a déjà été traitée.")
        return redirect("permission_detail", pk=pk)


    # Mise à jour du statut
    permission.statut = "accepte"
    permission.save()

    # Historique
    Validation.objects.create(
        demande_id=permission.id,
        validateur=user,
        type_demande="permission",
        decision="accepte",
        commentaire="Demande validée"
    )

    messages.success(request, "La demande a été validée avec succès.")

    return redirect("permission_detail", pk=pk)



@login_required
def refuser_permission(request, pk):

    permission = get_object_or_404(Permission, pk=pk)

    user = request.user

    # verification du role utilisateur

    if request.user.role != 'manager':
        return redirect('permission_list')

    if permission.employe.departement != user.employe.departement:
        return redirect("permission_list")

    # Empêcher de valider sa propre demande
    if permission.employe == user.employe:
        messages.error(request, "Vous ne pouvez pas traiter votre propre demande.")
        return redirect("permission_detail", pk=pk)


    # Vérifier le statut
    if permission.statut != "en attente":
        messages.warning(request, "Cette demande a déjà été traitée.")
        return redirect("permission_detail", pk=pk)


    # Mise à jour du statut
    permission.statut = "refuse"
    permission.save()

    # Historique
    Validation.objects.create(
        demande_id=permission.id,
        validateur=user,
        type_demande="permission",
        decision="refuse",
        commentaire="Demande refusée"
    )

    messages.success(request, "La demande a été refusée.")

    return redirect("permission_detail", pk=pk)