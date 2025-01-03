from rest_framework import serializers

class StatusCodeSerializer(serializers.Serializer):
    """
    Serializer for returning a status code message
    """

    details = serializers.CharField()
