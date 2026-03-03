from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for Company model.
    Owner is read-only because it is automatically assigned
    from the logged-in user.
    """

    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Company
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "website",
            "logo",
            "created_at",
            "updated_at",
        ]