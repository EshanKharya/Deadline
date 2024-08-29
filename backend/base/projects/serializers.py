from rest_framework import serializers
from base.models import Project, ProjectContributorMap, CustomUser


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "objective", "documentation"]

    def create(self, validated_data):
        user = self.context["request"].user
        project = Project.objects.create(leader=user, **validated_data)
        ProjectContributorMap.objects.create(
            pid=project, uid=user, is_super=True, access=ProjectContributorMap.ADMIN
        )
        return project


class ContributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectContributorMap
        fields = ["pid", "uid", "is_super", "access"]


class ProjectContributorMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectContributorMap
        fields = ["uid", "access"]

    def create(self, validated_data):
        # Retrieve Project instance using the provided pid from context
        pid = self.context["pid"]
        try:
            project = Project.objects.get(
                pk=pid
            )  # Ensure pid matches the project's primary key
        except Project.DoesNotExist:
            raise serializers.ValidationError({"pid": "Project not found."})

        # Create and return the contributor instance
        contributor = ProjectContributorMap.objects.create(
            pid=project, **validated_data
        )
        return contributor
