from django.urls import URLResolver
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_methods(request, **kwargs):
    from .urls import urlpatterns

    def remove_signs(url_info):
        return str(url_info).replace('^', '').replace('$', '')

    urls = []
    for url_obj in urlpatterns:
        if isinstance(url_obj, URLResolver):
            for url in url_obj.url_patterns:
                urls.append({str(url.name): remove_signs(url_obj.pattern) + remove_signs(url.pattern)})
        else:
            url_line = url_obj.pattern
            urls.append({url_line.name: remove_signs(url_line).replace('^', '')})
    return Response(data=urls, status=status.HTTP_200_OK)
