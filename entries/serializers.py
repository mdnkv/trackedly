from rest_framework import serializers

from entries.models import Entry
from projects.models import Project
from projects.serializers import ProjectListSerializer


class EntryCreateSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), allow_null=True)

    class Meta:
        model = Entry
        fields = ['id', 'start_time', 'start_date', 'finish_date', 'finish_time',
                  'project', 'description', ]
        read_only_fields = ['id']

    def validate(self, data):
        start_date = data.get('start_date')
        finish_date = data.get('finish_date')
        if finish_date < start_date:
            raise serializers.ValidationError('Finish date should be after start date or same day')
        start_time = data.get('start_time')
        finish_time = data.get('finish_time')
        if finish_time < start_time:
            raise serializers.ValidationError("Finish time should be after start time")
        return data

    def create(self, validated_data):
        owner = self.context['request'].user
        return Entry.objects.create(owner=owner, **validated_data)


class EntryListSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Entry
        fields = ['id', 'start_time', 'start_date', 'finish_date', 'finish_time',
                  'project', 'description']
