from django.shortcuts import render
from django.http import HttpResponse
import folium
import sys
sys.path.append('templates/static/code/')
from draw_map import map
from origins import origin
from single_share import single
# Create your views here.
def share_route(request):
    m = map()
    m = m._repr_html_()
    context = {
        'm': m
    }
    return render(request, 'share_route.html',context)

def base(request):
    return render(request, 'base.html')
    #return HttpResponse('This is the dap Page')

def orders(request):
    return render(request, 'orders.html')
    #return HttpResponse('This is the dap Page')

def emission(request):
    return render(request, 'emission.html')

def map_orders(request):
    m2 = origin()
    m2 = m2._repr_html_()
    context = {
        'm2': m2
    }
    return render(request, 'origins.html',context)

def single_share(request):
    m3 = single()
    m3 = m3._repr_html_()
    context = {
        'm3': m3
    }
    return render(request, 'single_share.html',context)
