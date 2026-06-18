from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from demande.models.repos_maladie_model import ReposMaladie
from demande.forms.repos_maladie_form import ReposMaladieForm


@login_required()
def repos_maladie_list(request):

    user = request.user

    employe = request.user.employe

    repos_maladies = None

    if user.role == 'employe':
        repos_maladies = ReposMaladie.objects.filter(statut='en attente', employe=employe).order_by('-date_creation')
    elif user.role in ['rh', 'admin']:
        repos_maladies = ReposMaladie.objects.all().order_by('-date_creation')
    elif user.role == 'manager':
        pass

    context = {
        'repos_maladies': repos_maladies
    }

    return render(request,'repos_maladie/index.html', context)


@login_required()
def repos_maladie_create(request):

    employe = request.user.employe

    repos_maladie_form = ReposMaladieForm()

    if request.method == 'POST':

        repos_maladie_form = ReposMaladieForm(request.POST, request.FILES)

        if repos_maladie_form.is_valid():
            repos = repos_maladie_form.save(commit=False)
            repos.employe = employe
            repos.save()

            return redirect('repos_maladie_list')


    context = {
        'repos_maladie_form': repos_maladie_form
    }

    return render(request, 'repos_maladie/create.html', context)




@login_required()
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


@login_required()
def repos_maladie_update(request, pk):

    repos_maladie = get_object_or_404(ReposMaladie, pk=pk)

    repos_maladie_form = ReposMaladieForm(instance=repos_maladie)

    if request.method == 'POST':

        repos_maladie_form = ReposMaladieForm(request.POST, request.FILES, instance=repos_maladie)

        if repos_maladie_form.is_valid():
            repos_maladie_form.save()

            return redirect('repos_maladie_list')


    context = {
        'repos_maladie_form': repos_maladie_form
    }

    return render(request, 'repos_maladie/update.html', context)


@login_required()
def repos_maladie_delete(request, pk):

    repos_maladie = get_object_or_404(
        ReposMaladie,
        pk=pk
    )

    repos_maladie.delete()

    return redirect(
        'repos_maladie_list'
    )