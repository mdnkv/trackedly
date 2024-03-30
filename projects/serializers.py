from rest_framework import serializers

from projects.models import Project
from customers.serializers import CustomerSerializer
from customers.models import Customer


class ProjectCreateSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'is_billable', 'customer', 'weekly_goal']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        project = Project.objects.create(owner=user, **validated_data)
        return project


class ProjectListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'is_billable', 'customer', 'weekly_goal']
