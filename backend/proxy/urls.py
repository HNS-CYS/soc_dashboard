from django.urls import path, re_path
from . import views

urlpatterns = [
    # Main proxy endpoints
    path('wazuh/', views.proxy_view, {'service': 'wazuh'}, name='proxy_wazuh'),
    path('shuffle/', views.proxy_view, {'service': 'shuffle'}, name='proxy_shuffle'),
    path('iris/', views.proxy_view, {'service': 'iris'}, name='proxy_iris'),
    path('velociraptor/', views.proxy_view, {'service': 'velociraptor'}, name='proxy_velociraptor'),
    
    # Catch-all paths for nested routes
    re_path(r'^wazuh/(?P<path>.*)$', views.proxy_view, {'service': 'wazuh'}),
    re_path(r'^shuffle/(?P<path>.*)$', views.proxy_view, {'service': 'shuffle'}),
    re_path(r'^iris/(?P<path>.*)$', views.proxy_view, {'service': 'iris'}),
    re_path(r'^velociraptor/(?P<path>.*)$', views.proxy_view, {'service': 'velociraptor'}),
]