from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from predict.main import Robot
import gc

def index(request):
    robots = []
    for obj in gc.get_objects():
        if isinstance(obj, Robot):
            robots.push(obj)
    return render(request,'index.html',{'robots':robots})

def startRobot(request, strategy, ammount):
    robotInstance = Robot(strategy, ammount)
    robotInstance.start()
    return HttpResponse(f"ligou {robotInstance}")

def stopRobot(request):
    for obj in gc.get_objects():
        if isinstance(obj, Robot):
            del obj
    return HttpResponse(f"desligou")
    
