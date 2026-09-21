from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from demande.models.type_permission_model import TypePermission
from demande.forms.type_permissions_form import TypePermissionForm


# ============================================================
# TYPE DE PERMISSION - LIST
# ============================================================

def type_permission_list(request):

    types_permissions = TypePermission.objects.all().order_by("-id")

    context = {
        "types_permissions": types_permissions,
    }

    return render(
        request,
        "type_permission/index.html",
        context
    )








# ============================================================
# TYPE DE PERMISSION - CREATE
# ============================================================

def type_permission_create(request):

    if request.method == "POST":

        type_permission_form = TypePermissionForm(request.POST)

        if type_permission_form.is_valid():

            type_permission_form.save()

            messages.success(
                request,
                "Le type de permission a été ajouté avec succès."
            )

            return redirect("type_permission_list")

    else:

        type_permission_form = TypePermissionForm()

    context = {
        'type_permission_form': type_permission_form
    }

    return render(
        request,
        "type_permission/create.html",
        context
    )


# ============================================================
# TYPE DE PERMISSION - DETAIL
# ============================================================

def type_permission_detail(request, pk):

    type_permission = get_object_or_404(
        TypePermission,
        pk=pk
    )

    return render(
        request,
        "type_permission/detail.html",
        {
            "type_permission": type_permission,
        }
    )


# ============================================================
# TYPE DE PERMISSION - UPDATE
# ============================================================

def type_permission_update(request, pk):

    type_permission = get_object_or_404(
        TypePermission,
        pk=pk
    )

    if request.method == "POST":

        type_permission_form = TypePermissionForm(
            request.POST,
            instance=type_permission
        )

        if type_permission_form.is_valid():

            type_permission_form.save()

            messages.success(
                request,
                "Le type de permission a été modifié avec succès."
            )

            return redirect("type_permission_list")

    else:

        type_permission_form = TypePermissionForm(
            instance=type_permission
        )

    context = {
        'type_permission_form': type_permission_form
    }

    return render(
        request,
        "type_permission/update.html",
        context
    )


# ============================================================
# TYPE DE PERMISSION - DELETE
# ============================================================

def type_permission_delete(request, pk):

    type_permission = get_object_or_404(
        TypePermission,
        pk=pk
    )



    type_permission.delete()

    messages.success(
        request,
        "Le type de permission a été supprimé avec succès."
    )

    return redirect("type_permission_list")

