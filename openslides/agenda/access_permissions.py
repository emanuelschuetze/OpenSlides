from ..utils.access_permissions import BaseAccessPermissions


class ItemAccessPermissions(BaseAccessPermissions):
    """
    Access permissions container for Item and ItemViewSet.
    """
    def can_retrieve(self, user):
        """
        Returns True if the user has read access model instances.
        """
        return user.has_perm('agenda.can_see')

    def get_serializer_class(self, user):
        """
        Returns serializer class.
        """
        from .serializers import ItemSerializer

        return ItemSerializer
