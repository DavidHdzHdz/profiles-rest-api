from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models
from . import permissions
from profiles_rest_api.settings import ENVIRONMENT

import requests
import os


class HelloApiView(APIView):
    """ A basic ApiView for test  """
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of APIview features """
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)'
            'Is similar to a traditional django view',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs'
        ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """ receive a name data and validate it with its serializer """
        serializer = self.serializer_class(data=request.data)
        if  serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'name': name, 'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """ Handle updating an object """
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """ Handle a partial update of an object """
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """ Delete an object """
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """ A basic api ViewSet """
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """ Return a list of ViewSet features """
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update, destroy)',
            'Automatically maps URLs using Routers',
            'Provides more functionality with less code'
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """ Return a customized hello world message """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'name': name, 'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """ Handle get data by pk """
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """ Handle update data by pk """
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """ Handle update some fields of data by pk """
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """ Handle delete an objec """
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

    def create(self, request, *args, **kwargs):
        """ override create method of api view for return token when an user is created """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        email, password = [serializer.validated_data[k] for k in ('email', 'password')]
        # change path by an enviroment path var, ** fix enviroment var **
        url = f'{ENVIRONMENT}/api/login/'
        # url = 'http://ec2-54-187-205-38.us-west-2.compute.amazonaws.com/api/login/'
        r = requests.post(url, data={'username': email, 'password': password})
        if r.status_code == 200:
            return Response({'user': serializer.data, 'token': r.json()['token']}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class LoginAPIView(ObtainAuthToken):
    """ Handle loging, get email and password and returns token """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileFeedItemViewSet(viewsets.ModelViewSet):
    """ Set of views for profile feed item objects """
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnFeedStatus, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """ this method is executed after method crete for doing aditional acrtions """
        serializer.save(user_profile=self.request.user)
