"""
URL Configuration for izanami project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('challenges/', include('challenges.urls')),
    path('scoreboard/', include('scoreboard.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # Add a direct path to izanami-status for compatibility with existing links
    path('core/izanami-status/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
