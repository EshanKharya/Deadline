from base.models import Project

def findAndValidateProject(pid, uid):
    try:
        project = Project.objects.get(pk=pid, leader=uid)
        return project
    except Project.DoesNotExist:
        return None