from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from  .models import PermissionGroup, AllPermission, UserRole
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializer import PermissionGroupSerializer, PermissionSerializer, UserRoleSerializer, UserRoleCreateSerializer, PermissionGroupCreateSerializer

# Create your views here.


class AllPermissionView(ListAPIView):
    model = PermissionGroup
    queryset = PermissionGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    # jWTAuthentication = JWTAuthentication()
    serializer_class = PermissionGroupSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PermissionGroupSerializer(queryset, many=True)
        # permission = PermissionGroup.objects.all()
        status_code = status.HTTP_200_OK
        print(serializer)
        response = {
            'success': 'true',
            'status code': status_code,
            'message': 'Permission fetched successfully',
            'data': serializer.data
        }
        return Response(response, status=status_code)

    def post(self, request):
        print(request)
        return Response({"message": 'Post request send'}, status=200)


class AllRolesView(ListAPIView):
    model = UserRole
    queryset = UserRole.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    # jWTAuthentication = JWTAuthentication()
    serializer_class = UserRoleSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserRoleSerializer(queryset, many=True)
        # permission = PermissionGroup.objects.all()
        status_code = status.HTTP_200_OK
        print(serializer)
        response = {
            'success': 'true',
            'status code': status_code,
            'message': 'Roles fetched successfully',
            'data': serializer.data
        }
        return Response(response, status=status_code)

class RolesDetailView(RetrieveUpdateDestroyAPIView):
    model = UserRole
    queryset = UserRole.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserRoleSerializer

    def get(self, request, pk, format=None):
        print(pk, "--------------------------")
        try:
            role = UserRole.objects.get(pk=pk)
            serializer = UserRoleSerializer(role)
            print(serializer)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Roles fetched successfully',
                'data': serializer.data
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'Roles not fetch',
                'data': str(e)
            }
        return Response(response, status=status_code)

    def put(self, request,pk , format=None):
        print(request.data,"-------------------------------role post",pk, request.data, 'id' not in request.data)
        if 'id' not in request.data:
            request.data['id'] = pk
        print(request.data, "request.data.id")
        instance = self.get_object()
        print(instance)
        serializer = UserRoleSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreatePermissionGroupView(CreateAPIView):
    serializer_class = PermissionGroupCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        print(request.data)
        serializer = PermissionGroupCreateSerializer(data=request.data)
        print(serializer, serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data)
            status_code = status.HTTP_201_CREATED
            response = {
                'success': 'True',
                'status code': status_code,
                'message': 'Permission Group created  successfully',
            }
        else:
            response = {
                "message":"error"
            }

        return Response(response, status=status_code)

class CreateRoleView(CreateAPIView):
    serializer_class = UserRoleCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        print(request.data, request.data['permission'])
        userrole = UserRole.objects.create(role_name=request.data['role_name'],
                                permission=request.data['permission'])
        # serializer = self.serializer_class(data=request.data)
        # print(serializer,"----", serializer.is_valid(raise_exception=True))
        # serializer.is_valid(raise_exception=True)
        print(userrole)
        # serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'Role created  successfully',
        }

        return Response(response, status=status_code)





# class PermissionView():
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)