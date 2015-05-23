from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'practicafinal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS}),
    #url(r'^./static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "actividades.views.inicio"),
    url(r'^todas$', "actividades.views.todas"),
    url(r'^login$', "actividades.views.login"),
    url(r'^logout$', "actividades.views.logout"),
    url(r'^actualizar$', "actividades.views.actualizar"),
    url(r'^ayuda$', "actividades.views.ayuda"),
    url(r'^actividad/(.*)$', "actividades.views.actividad"),
    url(r'^(.*)/rss$', "actividades.views.rss"),
    url(r'^(.*)$', "actividades.views.usuario"),
)
