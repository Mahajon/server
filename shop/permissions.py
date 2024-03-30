from rest_framework.permissions import BasePermission

class IsShopOwnerOrManager(BasePermission):
    """
    Allows access only to shop owners or managers for specific shop.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user is owner or manager of the shop object (obj)
        if not request.user.is_authenticated:
            return False  # Handle unauthenticated users
        
        # return true if method is get and user is owner or manager of the shop
        if request.method == 'GET':
            return (obj.owner == request.user or obj.managers.filter(pk=request.user.pk).exists())
        
        if request.method in ['PUT', 'DELETE']:
            return obj.owner == request.user


