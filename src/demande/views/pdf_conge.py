from django.http import HttpResponse
from utils.generer_pdf_conge import generer_pdf_conge
from demande.models.conges_model import Conges

def conge_pdf_view(request, pk):

    conge = Conges.objects.get(pk=pk)

    pdf_buffer = generer_pdf_conge(conge)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="conge_{conge.employe.nom}_{conge.employe.prenom}.pdf"'

    return response