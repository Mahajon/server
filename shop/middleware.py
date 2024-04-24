from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import HttpResponseNotFound, Http404, JsonResponse
from django.db import connection
from django.urls import set_urlconf
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import (
    get_public_schema_name,
    get_public_schema_urlconf,
    get_tenant_types,
    has_multi_type_tenants,
    remove_www,
)
from shop.models import Shop

class ShopMainMiddleware(MiddlewareMixin):
    TENANT_NOT_FOUND_EXCEPTION = Http404

    @staticmethod
    def hostname_from_request(request):
        return remove_www(request.get_host().split(":")[0])

    def process_request(self, request):
        connection.set_schema_to_public()
        try:
            hostname = self.hostname_from_request(request)
        except DisallowedHost:
            return HttpResponseNotFound()

        # Check the Shop from headers to change the schema for each request.
        shop_slug = request.headers.get("Shop")
        try:
            shop = Shop.objects.get(slug__iexact=shop_slug)
        except Shop.DoesNotExist:
            if not settings.DEBUG and not request.path.startswith("/auth/"):
                return JsonResponse({"detail": "Shop not found"}, status=400)            
            # If no shop is found, then set to public Shop and return
            request = self.no_shop_found(request, hostname)  
            return request
        shop.domain_url = hostname
        request.tenant = shop
        connection.set_tenant(request.tenant)
        self.setup_url_routing(request)

    def no_shop_found(self, request, hostname):
        if hasattr(settings, "SHOW_PUBLIC_IF_NO_TENANT_FOUND") and settings.SHOW_PUBLIC_IF_NO_TENANT_FOUND:
            self.setup_url_routing(request=request, force_public=True)
        else:
            raise self.TENANT_NOT_FOUND_EXCEPTION('No shop for hostname "%s"' % hostname)

    @staticmethod
    def setup_url_routing(request, force_public=False):
        public_schema_name = get_public_schema_name()
        if has_multi_type_tenants():
            shop_types = get_tenant_types()
            if not hasattr(request, "shop") or ((force_public or request.shop.schema_name == get_public_schema_name()) and "URLCONF" in shop_types[public_schema_name]):
                request.urlconf = get_public_schema_urlconf()
            else:
                shop_type = request.shop.get_shop_type()
                request.urlconf = shop_types[shop_type]["URLCONF"]
            set_urlconf(request.urlconf)
        else:
            # Do we have a public-specific urlconf?
            if hasattr(settings, "PUBLIC_SCHEMA_URLCONF") and (force_public or request.shop.schema_name == get_public_schema_name()):
                request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
