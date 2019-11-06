import django
import redis
from django.core.cache import caches
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.http import JsonResponse
from delta.models import status,led
from django.db import connection
from django.views.decorators.csrf import csrf_protect
redis = redis.Redis(db=12)
pubsub = redis.pubsub() #for publish and subscribe database
pipeline = redis.pipeline() #for send order to database
def node(request):
    response={'moisture':678
    }
    return JsonResponse(response)
    #queryset = led.objects.all()

    #Django’s cache framework is very flexible and allows you to cache your entire site
    #or individual views. You can control the behavior of the cache using the @cache_page decorator.
    #For instance to cache the results of my_view for 15 minutes, you can use the following code:
#from django.views.decorators.cache import cache_page

#@cache_page(60 * 15)
#def my_view(request):


# cache.set("key", "value1", nx=True)    #for work with redis database
# cache.set("key", "value2", nx=True)

def show(request):
    ##form=nodemcu(request.POST or None)
    obj=get_object_or_404(status, id=1)
    ##if form.is_valid():
    ##    form.save()
    #obj= status.objects.get(id=5)
    ##x=len(request.POST)
    mydata=json.loads(request.body.decode('utf-8'))
    ##obj.moisture=json.loads(receiveddata)
    obj.moisture=mydata["moisture"]
    obj.title=mydata["state"]
    obj.save()
    obj2=get_object_or_404(led,id=1)
    ##m=json.loads(f)
    #id_ = self.kwargs.get("id")
    if request.method =='POST':
        response={
        'method':request.method,
        'moisture':obj.moisture,
        'state':obj2.order
        }
        return JsonResponse(response)
    elif request.method =='GET':
        response={
        'method':request.method,
        'moisture':m["moisture"],
        'state':obj2.order
        }
        return JsonResponse(response)

##    response={
##    'abas':f,
##    'state':'on',
##    }
    ##return JsonResponse(response)
    ##if request.headers['connection'] =='close':
        ##connection.close()
@login_required
#def redis():
    #config redis client
#        redis = redis.Redis(db=12,socket_timeout=2000)
#        pubsub = redis.pubsub() #for publish and subscribe database
#        pipeline = redis.pipeline() #for send order to database
#        return redis,pubsub,pipeline
#redis()
def function(request):
    #pubsub.subscribe('testchannel')
    #r=redis.hvals('publisher2pd')
    r=redis.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
    obj= status.objects.get(id=1)
    obj2= led.objects.get(id=1)
    content={
    'title': obj.title ,
    'state': obj.moisture,
    'position': obj2.position,
    'test': r ,
    }
    #pubsub.unsubscribe('testchannel')
    return render(request,'delta/show.html',content)
@login_required
def off(request):
    f=json.loads(str(redis.hvals("publisher2pd")))
    print(f)
    obj= led.objects.get(id=1)
    obj.order='off'
    obj.position='off'
    obj2= status.objects.get(id=1)
    #obj.slug='on to off'
    obj.save( )
#    post=led.objects.create(order='off',position='off')
#    post.save()
    content={
    'order': obj.order ,
    'position': obj.position,
    'title': obj2.title ,
    'state': obj2.moisture,
    'test':f
    }
    return render(request,'delta/show.html',content)
@login_required
def on(request):
    obj= led.objects.get(id=1)
    obj.order='on'
    obj.position='on'
    obj2= status.objects.get(id=1)
    #obj.slug='off to on'
    obj.save()
    content={
    'order': obj.order ,
    'position': obj.position,
    'title': obj2.title ,
    'state': obj2.moisture
    }
    return render(request,'delta/show.html',content)
def homepage(request):
#    person= {'firstname': 'farzin', 'lastname': 'Daniels'}
#    weather= "sunny"
#    context= {
#        'person': person,
#        'weather': weather,
#        }

    return render(request,'delta/base.html')
