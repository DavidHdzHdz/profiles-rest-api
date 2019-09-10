from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

# this is the way for register viewset default routes
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')


urlpatterns = [
  path('hello-apiview/', views.HelloApiView.as_view()),
  path('', include(router.urls))
]