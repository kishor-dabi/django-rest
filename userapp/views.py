# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django_rest.userrole.models import UserRole
from django_rest.userrole.serializer import UserRoleSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from userapp.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileUpdateSerializer
from rest_framework.generics import RetrieveAPIView

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from userapp.models import UserProfile
from .auth import JWTAuthentication
from post.serializers import UserAddressSerializer

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        print(request, "---------------------")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserProfileView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()

    def get(self, request):
        try:
            # ur = UserSerializer(data=request.user)
            # print(ur, ur.is_valid())
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            print(user_profile, '{===========================')
            serializer = None
            if user_profile.role is not None:
                roledata = UserRole.objects.get(pk=user_profile.role.id)
                serializer = UserRoleSerializer(roledata)
            # print(serializer,serializer.data )
            # ad = UserAddressSerializer(user_profile.user_location)
            # print(ad)
            # userroleser = UserRoleSerializer(data=user_profile.role)
            # print(userroleser.is_valid())
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    'role': serializer,
                    # 'profile':user_profile.data
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class UserProfileUpdate(UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()
    serializer_class = UserProfileUpdateSerializer
    def put(self, request, pk, format=None):
        # pk = request.user
        if 'id' not in request.data:
            request.data['id'] = pk
        print(request.data, "request.data.id")
        instance = self.get_object()
        print(instance)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("serializer", status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'success': 'true',
            'status code': status.HTTP_200_OK,
            'message': 'User update successfully',
            'data': [{
                # 'first_name': user_profile.first_name,
                # 'last_name': user_profile.last_name,
                # 'phone_number': user_profile.phone_number,
                # 'age': user_profile.age,
                # 'gender': user_profile.gender,
            }]
        }
        return Response(response, status=status.HTTP_200_OK)

