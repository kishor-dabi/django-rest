from rest_framework import serializers
from .models import PermissionGroup, AllPermission, UserRole


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AllPermission
        fields = '__all__'# ('id', 'permission_group_name')
        extra_kwargs = {
            # 'permission_group': {'allow_null': True, 'required': False},
        }

class PermissionGroupSerializer(serializers.ModelSerializer):
    permission_set = PermissionSerializer(many=True)

    class Meta:
        model = PermissionGroup
        fields =  ('id', 'permission_group_name', 'permission_set')#'__all__'


class PermissionGroupCreateSerializer(serializers.ModelSerializer):
    permission_set = PermissionSerializer(many=True)

    class Meta:
        model = PermissionGroup
        fields = ('id', 'permission_group_name', 'permission_set')  # '__all__'


    def create(self, validated_data):
        print(validated_data, "-----------------------permission_group")
        permission_sets = validated_data.pop('permission_set')
        permission_group = PermissionGroup.objects.create(**validated_data)
        permission_set_serializer = self.fields['permission_set']

        print(permission_group)
        for permission in permission_sets:
            print(permission, "----------------------inside for loop")
            AllPermission.objects.create(permission_group=permission_group, **permission)
        print(permission_group,"---==========----------------- permission_group.data")
        return permission_group


class UserRoleSerializer(serializers.ModelSerializer):
    # permission = PermissionSerializer(many=True)

    class Meta:
        model = UserRole
        fields = '__all__'# ('id', 'permission_group_name')#
    def update(self, instance, validated_data):
        print(instance, validated_data)
        instance.permission = validated_data.get('permission', instance.permission)
        instance.role_name = validated_data.get('role_name', instance.role_name)
        instance.save()
        print(instance)
        return instance


class UserRoleCreateSerializer(serializers.ModelSerializer):
    # permission = PermissionSerializer(many=True)
    # permission = UserRoleSerializer(required=False)

    class Meta:
        model = UserRole
        fields = '__all__'  # ('id', 'permission_group_name')#

    def create(self, validated_data):
        print(validated_data, "-----------------------s", validated_data['permission'].toString())
        permissions = validated_data.pop('permission')
        user_role = UserRole.objects.create(role_name=validated_data['role_name'], permission=validated_data['permission'].toString())
        # for permission in permissions:
        #     per = AllPermission.objects.create(user_role=user_role, **permission)
        #     user_role.permission.add(per)
        #
        print(user_role,"---==========-----------------")
        return user_role
