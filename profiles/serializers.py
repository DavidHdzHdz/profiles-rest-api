from rest_framework import serializers

from . import models


class HelloSerializer(serializers.Serializer):
    """ Serializes a name field for testing our APIView """
    name =  serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile object """

    class Meta:
        model = models.UserProfile
        fields = ('id', 'name', 'email' ,'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """ create and return a new user """
        user = models.UserProfile.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
