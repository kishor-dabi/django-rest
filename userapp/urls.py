from django.urls import path, include
from django.conf.urls import url
from userapp.views import UserRegistrationView, UserLoginView, UserProfileView, UserProfileUpdate

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^login', UserLoginView.as_view()),
    url(r'^profile', UserProfileView.as_view()),
    path('update-profile/<int:pk>', UserProfileUpdate.as_view()),
    path('permission/', include('django_rest.userrole.urls')),
    url(r'^address/', include('post.urls')),
]