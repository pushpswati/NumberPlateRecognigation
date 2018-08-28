from __future__ import unicode_literals

from django.db import models
class Rnpdmodel(models.Model):
      created = models.DateTimeField(auto_now_add=True)
      username = models.CharField(max_length=100, blank=True, default='')
      useremail=models.EmailField(unique=True,null=True,blank=True)
      password = models.CharField(max_length=10)
      

      class Meta:
          ordering = ('created',)

class Rnpdtoken(models.Model):
      created = models.DateTimeField(auto_now_add=True)
      token_key = models.CharField(unique=True, max_length=100, blank=True, default='')
      useremail=models.EmailField(null=True,blank=True)
 
      class Meta:
          ordering = ('created',)

class Rnpduploadfile(models.Model):
      created = models.DateTimeField(auto_now_add=True)
      filename = models.FileField(upload_to='documents/')
      useremail=models.EmailField(null=True,blank=True)

      
      class Meta:
          ordering = ('created',)

class NumplateResult(models.Model):
      plate_result = models.TextField(blank=True,null=True)
      created = models.DateTimeField(auto_now_add=True)
      payload = models.CharField(max_length=10, blank=True,default='')
      result = models.CharField(max_length=100, blank=True, null=True)
      image_id = models.CharField(max_length=300, blank=True, null=True)


      class Meta:
            ordering = ('created',)

