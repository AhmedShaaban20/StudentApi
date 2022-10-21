import email
from rest_framework import request, status, viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.shortcuts import  render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib import auth 
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.paginator import Paginator
from knox.models import AuthToken
from django.contrib.auth import login




# def register_request(request):
# 	if request.method == "POST":
# 		form = UserSerializer(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			login(request, user)
# 			messages.success(request, "Registration successful." )
# 			return redirect("momepage")ain:h
# 		messages.error(request, "Unsuccessful registration. Invalid information.")
# 	form = UserSerializer()
# 	return render (request=request, template_name="students/signup.html", context={"register_form":form})


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
class RegisterUser(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'students/signup.html'
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user).data,
        })
        
        
# class UserAddApi(APIView):
#     authentication_classes = [] #disables authentication
#     permission_classes = [] #disables permission
#     #    permission_classes = (PublicEndpoint,)
#     def post(self,request):
#         # request.data._mutable = True
#         request.data.update({"username": request.data.get("email")})
#         serializeobj= UserSerializer(data = request.data)
#         if serializeobj.is_valid():
#             serializeobj.save()
#             userObj = User.objects.get(pk=serializeobj.data["id"]) 
#             token = Token.objects.create(user=userObj)
#             return Response({"token":str(token)},status=status.HTTP_201_CREATED)
#         return Response(serializeobj.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginApi(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    #    permission_classes = (PublicEndpoint,)
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'students/students.html'
    def post(self,request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if User is not None:
            token = AuthToken.objects.get(user=user)
            return Response({"token":str(token)},status=status.HTTP_200_OK)
        else : return Response(status=status.HTTP_401_UNAUTHORIZED)

class StudentsListAPI(APIView):
    # permission_classes = (IsAuthenticated,)  
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'students/students.html'
    def get(self, request):
        students = Student.objects.all()
        paginator = Paginator(students, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = StudentSerializer(students, many = True)
        return Response({'students': page_obj})
class SearchListAPI(APIView):
    # permission_classes = (IsAuthenticated,)  
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'students/search.html'
    def get(self, request):
        if 'q' in request.GET:
            q=request.GET['q']
            students=Student.objects.filter(name__icontains=q)
        else:
            students=Student.objects.all()

        paginator = Paginator(students, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = StudentSerializer(students, many = True)
        return Response({'students': page_obj})
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class StudentApi(APIView):
    # permission_classes = (IsAuthenticated,)             # <-- And here
    def get_object(self,pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return None    
    def get(self,request,pk): 
        StudentObj=self.get_object(pk)
        if StudentObj :
            serializeobj= StudentSerializer(StudentObj)
            return Response(serializeobj.data,status=status.HTTP_200_OK)
        else : return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):
        obj=self.get_object(pk)
        serializedObj= StudentSerializer(obj,data=request.data)
        if serializedObj.is_valid():
            serializedObj.save()
            return Response(status=status.HTTP_200_OK)
        else : return Response(serializedObj.errors,status=status.HTTP_400_BAD_REQUEST)
          
    def delete(self,request,pk):
        obj=self.get_object(pk)
        if obj :
            try:
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as err_msg: 
                    return Response(data ="{}".format(str(err_msg)),status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else : return Response(status=status.HTTP_404_NOT_FOUND)
