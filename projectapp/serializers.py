from rest_framework import serializers
from projectapp.models import Rnpdmodel
from projectapp.models import Rnpdtoken
from projectapp.models import Rnpduploadfile


class RnpdmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rnpdmodel
        fields=('id','created','username','password','useremail')

class RnpdtokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rnpdtoken
        fields=('id','created','token_key')

class RnpduploadfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rnpduploadfile
        fields=('id','created','filename')
