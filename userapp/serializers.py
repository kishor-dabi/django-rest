from .models import User, UserProfile
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django_rest.userrole.serializer import UserRoleSerializer
# from post.serializers import UserAddressSerializer
from post.models import UserAddress
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
#
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']
#
#
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class UserDataSerializer(serializers.ModelSerializer):

    # profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('id')
        # extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(required=False)
    user = UserDataSerializer(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.IntegerField(required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)

    # user_address = UserAddressSerializer(many=True, required=False)
    class Meta:
        model = UserProfile
        fields = "__all__" # ('first_name', 'last_name', 'phone_number', 'age', 'gender', 'role')

class UserListSerializer(serializers.ModelSerializer):

    # user_address = UserAddressSerializer(many=True, required=False)
    class Meta:
        model = UserProfile
        fields = "__all__" # ('first_name', 'last_name', 'phone_number', 'age', 'gender', 'role')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(required=False)
    user = UserDataSerializer(required=False)
    # user_address = UserAddressSerializer(many=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'  # ('first_name', 'last_name', 'phone_number', 'age', 'gender', 'role')

    def update(self, instance, validated_data):
        print(instance,"-----", validated_data)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        # instance.role = validated_data.get('role', instance.role)
        # AL = validated_data.pop('user_address')
        # AddressData = UserAddress()
        # AddressData.save()
        print(instance, "---------------------")
        # for address in AL:
        #     ad = None
        #     if 'id' not in address:
        #         ad = UserAddress.objects.create(**address)
        #     else:
        #         UserAddress.objects.get(pk=address['id'])
        #
        #     if ad:
        #         AddressData.user_location.add(ad)
        print(instance)
        instance.save()
        print(instance, "-----------------------------------final")
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            phone_number=profile_data['phone_number'],
            age=profile_data['age'],
            gender=profile_data['gender']
        )
        return user

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }
