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
import json
from datetime import datetime,timedelta
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
        #print(serializer)
        email = request.data['useremail']
        print(email,"email 1")
        passwd = request.data['password']
        print(passwd)
          

        # Write your code for check email sssst in db

        user = Rnpdmodel.objects.get(useremail=email)
        print(user,"email 2")
         
        if user is not None:
            if user.password==passwd:
                print("Login successfull: ",)
                #Checking here token_key if already exists
                try:
                    rnpdtoken_object = Rnpdtoken.objects.get(useremail=email) #   puri row ko utha kr lata hselect query db se nikl rha h
                    print("rnpdtokenobject",rnpdtoken_object)
                except:
                        # assign none value for rnpd token object
                    rnpdtoken_object=None
                       # Check rnpdtoken_object is exist or not 
                if rnpdtoken_object:
                      # Create a jwt token if its here for updated
                    jwttoken = jwt.encode({'useremail': email,'datetime':str(datetime.now())}, 'secret', algorithm='HS256')
                    print("token_key genrate",jwttoken)
                    print(type(jwttoken))
                      # jwt token assing to db(rnpdtoken_object)
                    rnpdtoken_object.token_key=jwttoken 
                      # save jwt token
                    rnpdtoken_object.save()
                      # response success true and token key dictionary
                    return Response({"sucess":"true","token":rnpdtoken_object.token_key,"datetime":str(datetime.now().strftime("%D"))}, status=status.HTTP_200_OK)  
                else:
                    # if token is not here then create the token (first time)
                    jwttoken = jwt.encode({'useremail': email,"datetime":str(datetime.now())}, 'secret', algorithm='HS256')
                    # now we insert the jwttoken or useremail /db me insert kr rhe h
                    rnpdtoken_object=Rnpdtoken.objects.create(token_key=jwttoken,useremail=email)
                    # response we get token_key
                    return Response({"sucess":"true","token":rnpdtoken_object.token_key,"datetime":str(datetime.now().strftime("%D"))}, status=status.HTTP_200_OK)
        else:
            return Response({"sucess":"false","message":"password is  not match"}, status=status.HTTP_400_BAD_REQUEST)

               
        

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
        print(file_obj,"cheakpoint1")
        jwttoken = request.data['token_key']
        print(jwttoken,"cheakpoint2")

        #jsondic = json.loads(jwttoken)
        print("token_key",jwttoken)
        print(type(jwttoken))



        payload = jwt.decode(jwttoken,'secret',algorithm=['HS256'])
        print(payload,"cheakpoint3")
        print(type(payload))

        rnpdtoken_previousdatetime=payload['datetime']
        print(rnpdtoken_previousdatetime,"cheakpoint4")    

        rnpdtoken_nowdatetime=datetime.datetime.now()  # we hav to convert json str to dic
        print(rnpdtoken_nowdatetime,"cheakpoint5")
        print(type(rnpdtoken_nowdatetime))

        now_min = rnpdtoken_nowdatetime.hour*60+rnpdtoken_nowdatetime.minute
        print(now_min,"cheakpoint6")
        now_date = rnpdtoken_nowdatetime.date()
        print(now_date,"cheakpoint7")


        pre_min = rnpdtoken_previousdatetime.hour*60+rnpdtoken_previousdatetime.minute
        print(pre_min,"cheakpoint8")
        pre_date = rnpdtoken_previousdatetime.date()
        print(pre_date,"cheakpoint9")

        if str(pre_date)==str(now_date) and (now_min-pre_min)>15:

            rnpdtoken_object = Rnpdtoken.objects.get(useremail=email)
            print(rnpdtoken_object,"cheakpoint10")

            jwttoken_expire = jwt.encode({'useremail': email}, 'secret', algorithm='HS256')
            print(jwttoken_expire,"cheakpoint11")
            print(type(jwttoken_expire))
            rnpdtoken_object.token_key=jwttoken_expire 
            rnpdtoken_object.save()
            return Response({"massage":"token is expire","token":rnpdtoken_object.token_key,"datetime":str(datetime.now().strftime("%D"))}, status=status.HTTP_403_OK) 

        else:
            rnpduploadfile_obj=Rnpduploadfile.objects.create(filename=file_obj)
            print(rnpduploadfile_obj,"cheakpoint12")
            image_path=settings.BASE_DIR+'/'+str(rnpduploadfile_obj.filename) # Uploaded image complete path
            print(image_path,"cheakpoint13")
            # Call micro service call karni h
            files = {'media_file': open(image_path,'rb')}

            #  url="http://35.227.148.145:8890/api/v1/rnpd"
            # payload={"email":"visionrival.ai@gmail.com"}
            #r = requests.post(url, files=files,data=payload)
            # numresult=str(r.json())
            # numresult="22kaur14ijs2"

            plate_resultdb=NumplateResult.objects.create(image_id=rnpduploadfile_obj.id,plate_result="wer4311ssw11")

            #print("numresult",numresult) 
            print(plate_resultdb,"cheakpoint14")
            return Response({'message':'file uploaded sucessfully'},plate_resultdb, status=status.HTTP_200_OK)
        
        except:
           print("Exception jwt")
             
             


          






