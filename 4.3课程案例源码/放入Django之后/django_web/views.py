from django.shortcuts import render
from django_web.models import ArtiInfo
from django.core.paginator import Paginator

def index(request):
    limit = 20
    arti_info = ArtiInfo.objects
    paginatior = Paginator(arti_info,limit)
    page = request.GET.get('page',1)
    print(request)
    print(request.GET)
    loaded = paginatior.page(page)
    context = {
        'ArtiInfo':loaded
    }
    return render(request,'new_index2.html',context)








