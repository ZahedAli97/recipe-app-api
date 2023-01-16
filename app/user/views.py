"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    # Create API View handles a HTTP Post request thats
    # designed for creating objects in the db.
    # It hanldes all logic for us, we just need to set serializer
    # serializer has the model defined with it so it takes from there
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    # ObtainAuthToken uses username and password so we set
    # our own serializer
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # used to make this api browsable, since its not on its own


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    # specifying view that authentication should be done with token
    permission_classes = [permissions.IsAuthenticated]
    # specifies the permission that this user can have to use this API
    # specifying that only is authenticated permission is needed

    def get_object(self):
        """Retrieve and return the autheticated user."""
        return self.request.user
