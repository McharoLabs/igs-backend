from rest_framework import serializers

from user.model.agent import Agent

class ResponseAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["user_id", "first_name", "middle_name", "last_name", "phone_number", "gender", "email", "avatar"]