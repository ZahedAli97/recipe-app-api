"""
Serializes for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
# Serializer takes our JSON input validates it and converts it into
# Either Python object or into a model in our database


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        """define the fields and args we want to pass to serializer."""
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # We dont want users to set is_staff etc so we don't specify them above
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        # setting extra params/config for above fields

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # overiding create method of user because it save password as text and
        # not hash
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        # Overriding update method from serializer
        password = validated_data.pop('password', None)
        # get will leave password in dictionary, if password is not
        # present then default ot None
        user = super().update(instance, validated_data)
        # call update method from ModelSerializer Base Class

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        # view calls the validation after passing data to serializer
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        # request contains the header metadata
        # if authenticate fails it returns empty object
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
            # view changes the above raised error to HTTP 400 BAD REQUEST

        attrs['user'] = user
        return attrs
