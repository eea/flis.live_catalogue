from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from live_catalogue import views


admin.autodiscover()


urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name='home'),

    url(r'^need/add$', views.CatalogueEdit.as_view(),
        {'kind': 'need'}, name='catalogue_add'),
    url(r'^need/(?P<pk>[\w\-]+)/edit$', views.CatalogueEdit.as_view(),
        {'kind': 'need'}, name='catalogue_edit'),
    url(r'^need/(?P<pk>[\w\-]+)/delete$', views.CatalogueDelete.as_view(),
        {'kind': 'need'}, name='catalogue_delete'),
    url(r'^need/(?P<pk>[\w\-]+)$', views.CatalogueView.as_view(),
        {'kind': 'need'}, name='catalogue_view'),

    url(r'^offer/add$', views.CatalogueEdit.as_view(),
        {'kind': 'offer'}, name='catalogue_add'),
    url(r'^offer/(?P<pk>[\w\-]+)/edit$', views.CatalogueEdit.as_view(),
        {'kind': 'offer'}, name='catalogue_edit'),
    url(r'^offer/(?P<pk>[\w\-]+)/delete$', views.CatalogueDelete.as_view(),
        {'kind': 'offer'}, name='catalogue_delete'),
    url(r'^offer/(?P<pk>[\w\-]+)$', views.CatalogueView.as_view(),
        {'kind': 'offer'}, name='catalogue_view'),

    url(r'^catalogue/(?P<catalogue_id>\d+)/document/(?P<doc_id>\d+)',
        views.CatalogueDocumentDelete.as_view(),
        name='catalogue_document_delete'),

    url(r'my', views.MyEntries.as_view(), name='my_entries'),

    url(r'^crashme/', views.CrashMe.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^select2/', include('django_select2.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
