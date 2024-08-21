from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import ProjectSerializer
from base.models import Project, ProjectContributorMap
from utils.functions import findAndValidateProject


class ProjectView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProjectSerializer(user.projects_led, many=True)
        return Response({"count": len(serializer.data), "projects": serializer.data})
    
    def post(self, request):
        user = request.user
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        print(request.data)
        existing = Project.objects.filter(title=request.data["title"], leader=request.user)
        if existing:
            return Response({"error": "A project with the given name already exists!"}, status=status.HTTP_409_CONFLICT)
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            project = serializer.save()
            return Response({
                'id': project.pid,
                'title': project.title,
                'objective': project.objective,
                'documentation': project.documentation,
                'is_open': project.is_open,
                'leader': project.leader.id
            }, status=status.HTTP_200_OK)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ProjectDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pid):
        user = request.user
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        project = findAndValidateProject(pid, user)
        if not project:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pid):
        user = request.user
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        project = findAndValidateProject(pid, user)
        if not project:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pid):
        user = request.user
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        project = findAndValidateProject(pid, user)
        if not project:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        project.delete()
        return Response({"Project deleted!"}, status=status.HTTP_204_NO_CONTENT)
    

class ProjectContributors(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pid):
        user = request.user
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED)
        project = findAndValidateProject(pid, user)
        if not project:
            return Response({"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)
        contributors = ProjectContributorMap.objects.filter(pid=project.pid)
        