from django.db import transaction
from rest_framework import serializers

from .models import Course, Subject
from core.fields import UniqueKeyRelatedField


class SubjectSerializer(serializers.ModelSerializer):
    courses = UniqueKeyRelatedField(
        many=True, queryset=Course.objects.all(), lookup_field_name="slug"
    )

    @transaction.atomic()
    def update(self, instance, validated_data):
        instance.courses.update(subject=None)
        return super().update(instance, validated_data)

    class Meta:
        model = Subject
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Course
        depth = 1
        fields = "__all__"
