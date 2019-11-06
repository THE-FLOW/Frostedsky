from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from delta.models import status,led
class  statusResource(ModelResource):
    class Meta:
        queryset = status.objects.all()
        resource_name = 'state'
        authorization = Authorization()
        fields=['title','moisture']
class  ledResource(ModelResource):
    class Meta:
        queryset = led.objects.all()
        resource_name = 'led'
        authorization = Authorization()
        fields=['order','position']
