from django.db import models
from django.urls import reverse

class status(models.Model):
    title=models.CharField(max_length=300)
    moisture=models.IntegerField(blank=True , null=True)
    def __str__(self):
        return '%s %s' % (self.title, self.moisture)
class led(models.Model) :
    order=models.CharField(max_length=50)
    position=models.CharField(max_length=50)
    #slug=models.SlugField(max_length=50)
    def __str__(self):
        return '%s %s' % (self.order, self.position)
    def get_absolute_url(self):
        return reverse('show', kwargs={"id": self.id})
