from rest_framework import serializers

from settings.models import SiteSettings

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'