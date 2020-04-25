from django.urls import path, include
from django.conf.urls import url
from .views import AllPermissionView, AllRolesView, RolesDetailView, CreateRoleView, CreatePermissionGroupView

urlpatterns = [
    url(r'^all-permissions', AllPermissionView.as_view()),
    url(r'^permission-group', CreatePermissionGroupView.as_view()),
    url(r'^roles', AllRolesView.as_view()),
    path('role', CreateRoleView.as_view()),
    path('role/<int:pk>', RolesDetailView.as_view()),
]













































































