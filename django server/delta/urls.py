from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from delta import views as vie
from delta.resources import statusResource,ledResource
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
status_resource = statusResource()
led_resource=ledResource()
app_name = 'delta'
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    #accounts/login/ [name='login']
    #accounts/logout/ [name='logout']
    #accounts/password_change/ [name='password_change']
    #accounts/password_change/done/ [name='password_change_done']
    #accounts/password_reset/ [name='password_reset']
    #accounts/password_reset/done/ [name='password_reset_done']
    #accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #accounts/reset/done/ [name='password_reset_complete']

    url(r'^delta/', include(status_resource.urls)),
    url(r'^delta/', include(led_resource.urls)),
    path('function/',vie.function, name="function"),
    path('delta/tele/led/',vie.show , name="show"),
    path('node/led/',vie.node , name="node"),
    path('',vie.homepage),
    path('on/',vie.on, name="on"),
    path('off/',vie.off, name="off")
]
urlpatterns += staticfiles_urlpatterns()

#mydata = json.loads(request.body.decode("utf-8"))
