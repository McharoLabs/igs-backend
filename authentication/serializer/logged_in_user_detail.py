from rest_framework import serializers

from user.model.user import User

class LoggedInUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'middle_name', 'last_name', 'phone_number', 'gender', 
            'username', 'email', 'password', 'avatar', 'is_verified', 'is_active', 
            'is_staff', 'is_admin', 'is_superuser'
        ]