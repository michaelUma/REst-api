from rest_framework import serializers
from . import models


class HelloSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for user profile objects"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user with a hashed password."""
        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update profile fields and hash a new password when supplied."""
        password = validated_data.pop('password', None)
        instance = super(UserProfileSerializer, self).update(
            instance, validated_data
        )

        if password:
            instance.set_password(password)
            instance.save(update_fields=['password'])

        return instance
