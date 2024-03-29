from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def validate(self, data):
        password = data.get('password')
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {'password': serializer_errors['non_field_errors']}
            )

        return data

    def create(self, validated_data):
        """Create a new user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data): # a user instance
        """Update a user, setting the password correctly and return it (the user)"""
        password = validated_data.pop('password', None) # remove pw
        user = super().update(instance, validated_data) # super() is a serializers.ModelSerializer

        if password:
            user.set_password(password)
            user.save()

        return user


# class AuthTokenSerializer(serializers.Serializer):
#     """Serializer for the user authentication object"""
#     email = serializers.CharField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )

#     def validate(self,attrs):
#         """Overwriting the validate() fn"""
        
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(
#             request=self.context.get('request'),
#             username=email,
#             password=password
#         )

#         if not user:
#             msg = _('Unable to authenticate with provided credentials')
#             raise serializers.ValidationError(msg, code='authentication')

#         attrs['user'] = user
#         return attrs
 