import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

def index(req):
    return render(req, 'index.html')

#获取两个地铁站最短距离
def get_shortest(req):
    '''
    返回结果说明：
    一切正常，code为200
    如果起始站或者终点站不存在，code为201，并将提示信息放入到msg之中
    xpath为距离左端的比例
    ypath为距离上端的比例
    '''
    res = {"code": 200, "msg": '', "data": None}

    start_stop = req.POST.get('start_stop')
    end_stop = req.POST.get('end_stop')
    print(start_stop + '1123')
    print(end_stop)

    data = {}
    data["xpath"] = [0.1, 0.2, 0.3]
    data["ypath"] = [0.2, 0.4, 0.6]
    res["data"] = data
    res = json.dumps(res)
    return HttpResponse(res)

#获取所有可到达的车站
def get_travel(req):
    res = {"code": 200, "msg": '', "data": None}

    start_stop = req.POST.get('start_stop')


    data = {}
    data["xpath"] = [0.1, 0.2, 0.3]
    data["ypath"] = [0.2, 0.4, 0.6]
    res["data"] = data
    res = json.dumps(res)
    return HttpResponse(res)


