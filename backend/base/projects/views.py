from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (
    ProjectSerializer,
    ProjectContributorMapSerializer,
    ContributionsSerializer,
)
from base.models import Project, ProjectContributorMap
from utils.functions import (
    findAndValidateProject,
    findAndValidateContributor,
    isAdmin,
    isBasic,
    isLeader,
    isAtleastContributor,
)


class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        contributions = ContributionsSerializer(user.projects, many=True)
        return Response(
            {"count": len(contributions.data), "projects": contributions.data}
        )

    def post(self, request):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        existing = Project.objects.filter(
            title=request.data["title"], leader=request.user
        )
        if existing:
            return Response(
                {"error": "A project with the given name already exists!"},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = ProjectSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            project = serializer.save()
            return Response(
                {
                    "id": project.pid,
                    "title": project.title,
                    "objective": project.objective,
                    "documentation": project.documentation,
                    "is_open": project.is_open,
                    "leader": project.leader.id,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ProjectDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        project = findAndValidateProject(pid, user)
        if not project:
            return Response(
                {"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(project)
        contributors = ProjectContributorMapSerializer(
            ProjectContributorMap.objects.filter(pid=pid), many=True
        )
        return Response(
            {"details": serializer.data, "contributors": contributors.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        project = findAndValidateProject(pid, user)
        if not isAdmin(pid, user):
            return Response(
                {"error": "You are not authorized to modify project details!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        project = findAndValidateProject(pid, user)
        if isBasic(pid, user):
            return Response(
                {"error": "You are not authorized to modify project details!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        project.documentation = request.data.get("documentation", project.documentation)
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        project = findAndValidateProject(pid, user)
        if not project:
            return Response(
                {"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        if not isLeader(pid, user):
            return Response(
                {"error": "You are not authorized to delete this project!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        project.delete()
        return Response(
            {"message": "Project deleted!"}, status=status.HTTP_204_NO_CONTENT
        )


class ProjectContributors(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        project = findAndValidateProject(pid, user)
        if not project:
            return Response(
                {"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        contributors = ProjectContributorMap.objects.filter(pid=project.pid)
        serializer = ProjectContributorMapSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        project = findAndValidateProject(pid, user)
        if not project:
            return Response(
                {"error": "Project not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        if not isAdmin(pid, user):
            return Response(
                {"error": "You can not add contributors to this project!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ProjectContributorMapSerializer(
            data=request.data, context={"pid": pid}
        )
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        if isAtleastContributor(pid, request.data["uid"]):
            return Response(
                {"error": "Contributor already exists!"},
                status=status.HTTP_409_CONFLICT,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectContributorDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pid, cid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        contributor = findAndValidateContributor(pid, user, cid)
        if not contributor:
            return Response(
                {"error": "Contributor not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectContributorMapSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pid, cid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        contributor = findAndValidateContributor(pid, user, cid)
        if not contributor:
            return Response(
                {"error": "Contributor not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        if not isAdmin(pid, user):
            return Response(
                {
                    "error": "You are not authorized to make changes to contributor access!"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ProjectContributorMapSerializer(
            contributor, request.data, partial=True
        )
        if not serializer.is_valid():
            return Response({"error": serializer.errors})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pid, cid):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found!"}, status=status.HTTP_401_UNAUTHORIZED
            )
        contributor = findAndValidateContributor(pid, user, cid)
        if not contributor:
            return Response(
                {"error": "Contributor not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        if not isAdmin(pid, user):
            return Response(
                {"error": "You are not authorized to delete contributors!"},
                status=status.HTTP_403_FORBIDDEN,
            )
        contributor.delete()
        return Response({"message": "Contributor removed!"}, status=status.HTTP_200_OK)
