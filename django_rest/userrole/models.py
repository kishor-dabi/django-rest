from django.db import models

# Create your models here.
class PermissionGroup(models.Model):
    permission_group_name = models.CharField(max_length=100)

    class Meta:
        """
        to set table name in database
        """
        db_table = "permission_group"

class AllPermission(models.Model):
    permission_name = models.CharField(max_length=100)
    permission_group = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE,blank=True, null=True, related_name='permission_set')
    class Meta:
        """
        to set table name in database
        """
        db_table = "all_permissions"

class UserRole(models.Model):
    role_name = models.CharField(max_length=100)
    permission = models.TextField()
    # = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE, related_name='permission_set')
    class Meta:
        """
        to set table name in database
        """
        db_table = "user_role"


#
# class UserRolePermission(models.Model):
#     user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
#     permission = models.ForeignKey(AllPermission, on_delete=models.CASCADE)