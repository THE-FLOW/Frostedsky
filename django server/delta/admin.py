from django.contrib import admin
from .models import status,led
@admin.register(status)
class statusAdmin(admin.ModelAdmin):
    list_display=('title','moisture')
    list_filter=('title','moisture')
    pass
@admin.register(led)
class ledAdmin(admin.ModelAdmin):
    list_display=('order','position')
    list_filter=('order','position')
    pass
# Register your models here.
