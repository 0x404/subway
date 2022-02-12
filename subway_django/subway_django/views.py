import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .subway import subway

def index(req):
    return render(req, 'index.html')

def get_shortest(req):
    """Get shortest path.

    Return:
        code: 200, every thing is ok.
              201 with error message.
        data: xpath, ypath
    """
    res = {"code": 200, "msg": '', "data": None}

    start = req.POST.get('start_stop')
    end = req.POST.get('end_stop')

    try:
        data = {}
        ansx, ansy = subway.query_shortest_path(start, end)
        data["xpath"] = ansx
        data["ypath"] = ansy
        res["data"] = data
    except:
        res["code"] = 201
        res["msg"] = "查询失败，请检查站点名是否出错"

    res["data"] = data
    res = json.dumps(res)
    return HttpResponse(res)

def get_travel(req):
    res = {"code": 200, "msg": '', "data": None}

    start = req.POST.get('start_stop')

    try:
        data = {}
        ansx, ansy = subway.query_travel_path(start)
        data["xpath"] = ansx
        data["ypath"] = ansy
        res["data"] = data
    except:
        res["code"] = 201
        res["msg"] = "查询失败，请检查站点名是否出错"

    res["data"] = data
    res = json.dumps(res)
    return HttpResponse(res)


