from __future__ import unicode_literals

from django.db import models
class Rnpdmodel(models.Model):
      created = models.DateTimeField(auto_now_add=True)
      username = models.CharField(max_length=100, blank=True, default='')
      useremail=models.EmailField(null=True,blank=True)
      password = models.CharField(max_length=10)
      

      class Meta:
          ordering = ('created',)

class Rnpdtoken(models.Model):
      created = models.DateTimeField(auto_now_add=True)
      token_key = models.CharField(max_length=100, blank=True, default='')
 
      class Meta:
          ordering = ('created',)

class Rnpduploadfile(models.Model):
      created = models.DateTimeField(auto_now_add=True)
      filename = models.FileField(upload_to='documents/')
      
 


      class Meta:
          ordering = ('created',)
