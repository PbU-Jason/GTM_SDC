from django.shortcuts import render

from .models import GRB

def download_table(request):
    grb_db = GRB.objects.all().order_by('name').values()
    return render(request, "table.html", {'db': grb_db, 'db_keys': grb_db[0].keys()})