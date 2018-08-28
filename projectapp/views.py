from projectapp.models import Rnpdmodel
from projectapp.models import Rnpdtoken,NumplateResult

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
from project import settings




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
          serializer = RnpdtokenSerializer(Rnpdmodel_obj,many=True)
          return Response(serializer.data, status=status.HTTP_201_CREATED)

class Rnpdtokenlistview(APIView):
      def get(self,request,format=None):
          print("token aya h kya")
          Rnpdtoken_obj = Rnpdtoken.objects.all()
          serializer = RnpdtokenSerializer(Rnpdtoken_obj,many=True)
          return Response(serializer.data, status=status.HTTP_201_CREATED)




class Rnpduploadfileview(APIView):

     parser_classes = (MultiPartParser,)
     def post(self,request,format=None):
          
          file_obj = request.data['filename']
          token_key = request.data['token_key']
          print("token_key",token_key)
         
          tokenrnpduser = Rnpdtoken.objects.get(token_key=token_key)
          print("oooooouj6tyyyhhhhhhhhtyytytytyutyutyutytyt")
          #print("token_key----------------------",[t.token_key for t in tokenrnpduser  ]) 
                                   # field name (token_key h) models ka
         
    
          if tokenrnpduser is not None:
                if tokenrnpduser.token_key==token_key:
                    rnpduploadfile_obj=Rnpduploadfile.objects.create(filename=file_obj)
                    image_path=settings.BASE_DIR+'/'+str(rnpduploadfile_obj.filename) # Uploaded image complete path
   
                    # Call micro service call karni h
                    files = {'media_file': open(image_path,'rb')}

                    url="http://35.227.148.145:8890/api/v1/rnpd"
                    payload={"email":"visionrival.ai@gmail.com"}
                    r = requests.post(url, files=files,data=payload)
                    numresult=str(r.json())
                   # numresult="22kaur14ijs2"
                    plate_resultdb=NumplateResult.objects.create(image_id=rnpduploadfile_obj.id,plate_result=numresult)
        
                    print("numresult",numresult) 
                    print("number palet",plate_resultdb)

                
                   
                    
                    response={"sucess":"image uploaded","image_path":image_path,"plate_resultdb":plate_resultdb.plate_result,"image_id":rnpduploadfile_obj.id,"result_id": plate_resultdb.id}
                    result_dic={"success": "True",
                                "response": response}
         
                    
                    return Response(result_dic, status=status.HTTP_200_OK)
                else:
                    return Response({"sucess":"image is not upload","token": token_key}, status=status.HTTP_400_BAD_REQUEST)
          else:
                return Response({"sucess":"false","token":tokenrnpduser is none }, status=status.HTTP_400_BAD_REQUEST)
             


             
             


          






