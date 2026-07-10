from django.http import HttpResponse
from utils.generer_pdf_conge import generer_pdf_conge
from utils.generer_pdf_permission import generer_pdf_permission
from utils.generer_pdf_repos_maladie import generer_pdf_repos_maladie
from demande.models.conges_model import Conges
from demande.models.permission_model import Permission
from demande.models.repos_maladie_model import ReposMaladie

def conge_pdf_view(request, pk):

    conge = Conges.objects.get(pk=pk)

    pdf_buffer = generer_pdf_conge(conge)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="conge_{conge.employe.nom}_{conge.employe.prenom}.pdf"'

    return response


def permission_pdf_view(request, pk):

    permission = Permission.objects.get(pk=pk)

    pdf_buffer = generer_pdf_permission(permission)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="permission_{permission.employe.nom}_{permission.employe.prenom}.pdf"'

    return response



def repos_maladie_pdf_view(request, pk):

    repos = ReposMaladie.objects.get(pk=pk)

    pdf_buffer = generer_pdf_conge(repos)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="repos_{repos.employe.nom}_{repos.employe.prenom}.pdf"'

    return response