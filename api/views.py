from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
import stat
from blog.models import Blog
from blog.serializers import BlogSerializer, CommentSerializer
import employees
from students.models import Student
from employees.models import Employee
from blog.models import *
from django.http import Http404

from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter


from .paginations import CustomPagination
from employees.filters import EmployeeFilter




from api import serializers

@api_view(['GET', 'POST'])
def StudentsView(request):
    # get data from database using serializer
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK )
   
    # Storing data using serializer 
    elif request.method == 'POST':
        serializer = StudentSerializer(data = request.data) # incoming data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# fetching the single student data based on the primary key
@api_view(['GET', 'PUT', 'DELETE'])
def StudentDetailView(request,pk):
    try: 
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    # update the existing data
    elif request.method == 'PUT':
        serializer = StudentSerializer(student,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status = status.HTTP_200_OK)
        else: 
            return Response (serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    # Deleting the Existing Data
    elif request.method == 'DELETE':
        student.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
# def StudentsView(request):
#     students = Student.objects.all() # Query set
#     # serialize this data manually. convert query set to serialize list, 
#     # it is easy for convert it into Json
#     student_list = list(students.values())
#     return JsonResponse(student_list,safe=False)
#     # why we use safe=False, Json support Dict, but we are passing list, 
#     # so we declare the data is safe. 

##########----Class Based View----#########
# class Employees(APIView):
#     def get(self, request): # Instense Method
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many = True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self,request):
#         serializer = EmployeeSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
# class EmployeeDetails(APIView) :
#     def get_objects(self,pk):
#         try: 
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             raise Http404 
#     def get(self, request, pk):
#         employee = self.get_objects(pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request,pk):
#         employee = self.get_objects(pk)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     def delete(self, request,pk):
#         employee = self.get_objects(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


##########----Mixins----#########
# class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    
# class EmployeeDetails(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    def get(self, request,pk):
        return self.retrieve(request,pk)
    
    def put(self,request,pk):
        return self.update(request,pk)
    
    def delete(self,request, pk):
        return self.destroy(request,pk)

'''   
##########----Generics----#########
# class Employees(generics.ListAPIView,generics.CreateAPIView):
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# class EmployeeDetails(generics.RetrieveAPIView,generics.UpdateAPIView, generics.DestroyAPIView):
class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
''' 
##########----Viewset----#########
# class EmployeeViewset(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Employee.objects.all()
#         serializer = EmployeeSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def create (self, request):
#         serializer = EmployeeSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors)
    
#     def retrieve (self, request, pk):
#         employee = get_object_or_404(Employee, pk=pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status.HTTP_200_OK)
    
#     def update(self, request, pk): 
#         employee = get_object_or_404(Employee, pk=pk)
#         serializer = EmployeeSerializer(employee, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk=None):
#         employee= get_object_or_404(Employee,pk =pk)
#         employee.delete()
#         return Response (status=status.HTTP_204_NO_CONTENT)
    

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    # filterset_fields = ['designation']
    filterset_class = EmployeeFilter



class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['blog_title', 'blog_body']
    # search_fields = ['^blog_title']
    # ordering_fields = ['id']
    ordering_fields = ['id','blog_title']



# class BlogView(generics.ListCreateAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
    

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     lookup_field = 'pk'


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    pass
    

        
        
    





