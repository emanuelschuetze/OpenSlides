from ..utils.access_permissions import BaseAccessPermissions


class ProjectorAccessPermissions(BaseAccessPermissions):
    """
    Access permissions container for Projector and ProjectorViewSet.
    """

    base_permission = "core.can_see_projector"


class TagAccessPermissions(BaseAccessPermissions):
    """
    Access permissions container for Tag and TagViewSet.
    """


class ChatMessageAccessPermissions(BaseAccessPermissions):
    """
    Access permissions container for ChatMessage and ChatMessageViewSet.
    """

    base_permission = "core.can_use_chat"


class ProjectorMessageAccessPermissions(BaseAccessPermissions):
    """
    Access permissions for ProjectorMessage.
    """

    base_permission = "core.can_see_projector"


class CountdownAccessPermissions(BaseAccessPermissions):
    """
    Access permissions for Countdown.
    """

    base_permission = "core.can_see_projector"


class ConfigAccessPermissions(BaseAccessPermissions):
    """
    Access permissions container for the config (ConfigStore and
    ConfigViewSet).
    """


class HistoryAccessPermissions(BaseAccessPermissions):
    """
    Access permissions container for the Histroy.
    """

    base_permission = "core.can_see_history"
