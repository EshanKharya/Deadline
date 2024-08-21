from rest_framework import serializers
from base.models import Project, ProjectContributorMap


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
            
    def create(self, validated_data):
        user = self.context["request"].user
        project = Project.objects.create(leader=user, **validated_data)
        ProjectContributorMap.objects.create(pid=project, uid=user, is_super=True, access=ProjectContributorMap.ADMIN)
        return project
    

class ProjectContributorMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectContributorMap
        fields = '__all__'