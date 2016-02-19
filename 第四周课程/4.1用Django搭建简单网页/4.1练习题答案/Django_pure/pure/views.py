from django.shortcuts import render
from django.core.paginator import Paginator
from pure.models import ItemInfo

# Create your views here.

def pure_index(request):
    return render(request,'pure_index.html')



def home(request):
    limit = 10
    item_info = ItemInfo.objects
    paginatior = Paginator(item_info,limit)
    page = request.GET.get('page',1)
    print(request)
    print(request.GET)
    loaded = paginatior.page(page)

    context = {
        'ItemInfo':loaded,
    }

    return render(request,'pure_index_paginator.html',context)