from .models import ActivityLog


def log_activity(organization, actor, action):
    ActivityLog.objects.create(
        organization=organization,
        actor=actor,
        action=action
    )
