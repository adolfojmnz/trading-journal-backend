from rest_framework import serializers

from operations.models import ForexOperation


class ForexOperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForexOperation
        fields = "__all__"