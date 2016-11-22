from django.shortcuts import render
from purelayoutblog.models import ItemInfo
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    limit = 10
    item_info = ItemInfo.objects[:20]
    paginator = Paginator(item_info,limit)
    page = request.GET.get('page',1)
    print(request)
    print(request.GET)


    loaded = paginator.page(page)


    context = {
         # 'title':item_info[0].title,
         # 'area' :item_info[0].area
        # 'area' :'海淀区',
        # 'title' :'测试一下'
        'ItemInfo':loaded


    }

    # print (context)


    return render(request,'index.html',context)

