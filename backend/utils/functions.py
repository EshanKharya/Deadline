from base.models import Project, ProjectContributorMap

def findAndValidateProject(pid, uid):
    try:
        if not isAtleastContributor(pid, uid):
            return None
        project = Project.objects.get(pk=pid)
        return project
    except Project.DoesNotExist:
        return None
    
def findAndValidateContributor(pid, uid, cid):
    try:
        project = findAndValidateProject(pid, uid)
        if not project:
            return None
        contributor = ProjectContributorMap.objects.get(pid=pid, uid=cid)
        return contributor
    except ProjectContributorMap.DoesNotExist:
        return None

def isAtleastContributor(pid, cid):
    try:
        ProjectContributorMap.objects.get(pid=pid, uid=cid)
        return True
    except:
        return False        

def isAdmin(pid, cid):
    try:
        project_map = ProjectContributorMap.objects.get(pid=pid, uid=cid)
        return project_map.access == ProjectContributorMap.ADMIN
    except:
        return False
    
def isScribe(pid, cid):
    try:
        project_map = ProjectContributorMap.objects.get(pid=pid, uid=cid)
        return project_map.access == ProjectContributorMap.SCRIBE
    except:
        return False
    
def isBasic(pid, cid):
    try:
        project_map = ProjectContributorMap.objects.get(pid=pid, uid=cid)
        return project_map.access == ProjectContributorMap.BASIC
    except:
        return False
    
def isLeader(pid, cid):
    try:
        project_map = ProjectContributorMap.objects.get(pid=pid, uid=cid)
        return project_map.is_super
    except:
        return False
    