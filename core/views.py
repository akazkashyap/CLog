from rest_framework.generics import ( CreateAPIView) 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
# Create your views here.

class UserRegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

class UserLoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        
        if username == "" or password == "":
            return Response({"details":"Username/password can't be empty"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username = username)
            if not user.check_password(password):
                raise AuthenticationFailed("Wrong credentials")
                
            token, created = Token.objects.get_or_create(user=user)
            return Response({'details':"logged in successfully",'token':token.key}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"details":"User doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed:
            return Response({"details":"Wrong credentials"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"details":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            

