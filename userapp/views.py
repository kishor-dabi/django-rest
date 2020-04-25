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
from userapp.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.generics import RetrieveAPIView

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from userapp.models import UserProfile
from .auth import JWTAuthentication


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

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    jWTAuthentication = JWTAuthentication()

    def get(self, request):
        try:
            # ur = UserSerializer(data=request.user)
            # print(ur, ur.is_valid())
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            print(user_profile.role, '{===========================', user_profile.role.id)
            roledata = UserRole.objects.get(pk=user_profile.role.id)
            serializer = UserRoleSerializer(roledata)
            print(serializer,serializer.data )
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
                    'role': serializer.data
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
    def put(self, request):

        print(request.data)
        user_profile = UserProfile.objects.filter(user=request.user).update(role_id=request.data['role_id'])

        jwtdata = self.jWTAuthentication.authenticate(request=request)
        print(jwtdata, '------------------', user_profile)
        # profile = request.data
        # profile['user_id'] = jwtdata[0]['user_id']
        # print(profile)
        # role = UserRole.objects.get(pk=request.data['role_id'])
        # rser = UserRoleSerializer(data=role)
        # print(role, '-----role', rser.is_valid())
        # user_profile.role = role
        # uu = UserSerializer(user_profile, data=request.data)
        # print(uu)
        # print(uu.is_valid())
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

class UserProfileUpdate(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    def put(self, request):
        print(request.data)
        response = {
            'success': 'true',
            'status code': status.HTTP_200_OK,
            'message': 'User update successfully',
            'data': [{
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'phone_number': user_profile.phone_number,
                'age': user_profile.age,
                'gender': user_profile.gender,
            }]
        }
        return Response(response, status=status.HTTP_200_OK)

