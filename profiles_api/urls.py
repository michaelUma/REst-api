from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
#router.register({name of API}, views.{viewset},base-name={name})
#no need of base name in case of models viewset

router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewset, base_name='login')

urlpatterns = [
    path('hello-view', views.HelloApiView.as_view(), name='hello-view'),
    path('', include(router.urls)),
    #router automatically generates urls for us
]