from projectapp.models import Rnpdmodel
from projectapp.models import Rnpdtoken
from projectapp.models import Rnpduploadfile
from projectapp.serializers import RnpdmodelSerializer
from projectapp.serializers import RnpdtokenSerializer
from projectapp.serializers import RnpduploadfileSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework import generics,permissions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import jwt
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser,JSONParser


class UserSinup(APIView):
      def post(self, request, format=None):
          serializer = RnpdmodelSerializer(data=request.data)
          if serializer.is_valid():
             serializer.save()
             return Response(serializer.data,status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Rnpd_Login(APIView):
     
      # This is login api
      def post(self,request, format=None):
          
          serializer = RnpdmodelSerializer(data=request.data)

          email = request.data['useremail']
          
          passwd = request.data['password']
          

          # Write your code for check email sssst in db

          user = Rnpdmodel.objects.get(useremail=email)
         
          if user is not None:
              if user.password==passwd:
                 print("Login successfull: ",)

                 token_key = jwt.encode({'email': 'useremail'}, 'secret', algorithm='HS256')
                 
                 Rnpdtoken_obj = Rnpdtoken.objects.create(token_key=token_key)
                 
                 return Response({"sucess":"true","token":token_key}, status=status.HTTP_200_OK)
              else:
                  return Response({"sucess":"false","message":"Login not successfull"}, status=status.HTTP_400_BAD_REQUEST)

          else:
               return Response({"sucess":"false","message":"Login not successfull"}, status=status.HTTP_400_BAD_REQUEST)




class Rnpduserlist(APIView):
      def get(self,request,format=None):
          print("checkpoint 1")
          Rnpdmodel_obj = Rnpdmodel.objects.all()
          serializer = RnpdmodelSerializer(Rnpdmodel_obj,many=True)
          return Response(serializer.data, status=status.HTTP_201_CREATED)

class Rnpduploadfileview(APIView):

     parser_classes = (MultiPartParser,)
     def post(self,request,format=None):
          
          file_obj = request.data['filename']
          
          token_key_obj = request.data['token_key']
          print("token_key_obj",token_key_obj)
          
          
          tokenrnpd = Rnpdtoken.objects.filter(token_key_obj=token_key)# field name (token_key h)
          
          if tokenrnpd is not None:
               if tokenrnpd.token_key==token_key_obj:
                  Rnpduploadfile.objects.create(filename=file_obj)
                  print("image uploaded succesfully",filename)
             
                  return Response({"sucess":"true","decoded_token":tokenrnpd}, status=status.HTTP_200_OK)
               else:
                   return Response({"sucess":"false","message":"token is not match"}, status=status.HTTP_400_BAD_REQUEST)

          else:
               return Response({"sucess":"false","message":"Invalid user authentication"}, status=status.HTTP_400_BAD_REQUEST)


             
             


          






