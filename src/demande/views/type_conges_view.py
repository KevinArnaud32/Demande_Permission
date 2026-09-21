from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from demande.forms.type_conges_form import TypeCongesForm
from demande.models.conges_model import TypeConge


# ============================================================
# TYPE DE CONGE - LIST
# ============================================================

def type_conge_list(request):

    types_conges = TypeConge.objects.all().order_by("-id")

    context = {
        "types_conges": types_conges,
    }

    return render(
        request,
        "type_conge/index.html",
        context
    )


# ============================================================
# TYPE DE CONGE - CREATE
# ============================================================

def type_conge_create(request):

    if request.method == "POST":

        type_conge_form = TypeCongesForm(request.POST)

        if type_conge_form.is_valid():

            type_conge_form.save()

            messages.success(
                request,
                "Le type de congé a été ajouté avec succès."
            )

            return redirect("type_conge_list")

    else:

        type_conge_form = TypeCongesForm()

    context = {
        'type_conge_form': type_conge_form
    }

    return render(
        request,
        "type_conge/create.html",
        context
    )


# ============================================================
# TYPE DE CONGE - DETAIL
# ============================================================

def type_conge_detail(request, pk):

    type_conge = get_object_or_404(
        TypeConge,
        pk=pk
    )

    return render(
        request,
        "type_conges/detail.html",
        {
            "type_conge": type_conge,
        }
    )


# ============================================================
# TYPE DE CONGE - UPDATE
# ============================================================

def type_conge_update(request, pk):

    type_conge = get_object_or_404(
        TypeConge,
        pk=pk
    )

    if request.method == "POST":

        type_conge_form = TypeCongesForm(
            request.POST,
            instance=type_conge
        )

        if type_conge_form.is_valid():

            type_conge_form.save()

            messages.success(
                request,
                "Le type de congé a été modifié avec succès."
            )

            return redirect("type_conge_list")

    else:

        type_conge_form = TypeCongesForm(
            instance=type_conge
        )

    context = {
        'type_conge_form': type_conge_form
    }

    return render(
        request,
        "type_conge/update.html",
        context
    )


# ============================================================
# TYPE DE CONGE - DELETE
# ============================================================

def type_conge_delete(request, pk):

    type_conge = get_object_or_404(
        TypeConge,
        pk=pk
    )



    type_conge.delete()

    messages.success(
        request,
        "Le type de congé a été supprimé avec succès."
    )

    return redirect('type_conge_list')