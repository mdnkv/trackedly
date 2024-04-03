from rest_framework import serializers

from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        return Customer.objects.create(owner=user, **validated_data)