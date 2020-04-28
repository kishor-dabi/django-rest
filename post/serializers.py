from .models import UserAddress
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django_rest.userrole.serializer import UserRoleSerializer
from userapp.serializers import UserSerializer, UserListSerializer
from userapp.models import UserProfile


class UserAddressSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    user_location = UserListSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = UserAddress
        fields = "__all__" #('id', 'user_address')


class UserAddressCreateSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    user_location = UserSerializer(many=True, required=False)
    # user_location = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = UserAddress
        fields = "__all__"  #('location', 'user_location')#

    def create(self, validated_data):
        UserLocation = validated_data.pop("user_location")
        print(UserLocation,"-----", validated_data)
        # print(dict(UserLocation))
        # userList = UserSerializer(data=UserLocation)
        addressLocatio = UserAddress.objects.create(**validated_data)
        print(addressLocatio, "---------------------")

        for address in UserLocation:
            print(address, "{{{{{{{{{{{{{{{{{{{{{{",address['id'])
            uuser = UserProfile.objects.get(pk=address['id'])
            addressLocatio.user_location.add(uuser)
        addressLocatio.save()
        print(addressLocatio, "-----------------------------------final")
        return addressLocatio

    def update(self, instance, validated_data):
        UserLocation = validated_data.pop("user_location")

        print(instance,"------------------------", validated_data, )
        instance.location = validated_data.get('location', instance.location)
        for address in UserLocation:
            print(address, "{{{{{{{{{{{{{{{{{{{{{{",address['id'])
            uuser = UserProfile.objects.get(pk=address['id'])
            instance.user_location.add(uuser)
        # instance.role_name = validated_data.get('role_name', instance.role_name)
        instance.save()
        print(instance, instance.location)
        return instance
