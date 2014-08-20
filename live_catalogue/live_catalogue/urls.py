from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from live_catalogue import views


admin.autodiscover()

settings_urls = patterns(
    '',
    url(r'^categories/$',
        views.SettingsCategoriesView.as_view(),
        name='categories'),

    url(r'^categories/new/$',
        views.SettingsCategoriesAddView.as_view(),
        name='categories_add'),

    url(r'^categories/(?P<pk>.*)/edit$',
        views.SettingsCategoriesEditView.as_view(),
        name='categories_edit'),

    url(r'^categories/(?P<pk>.*)/delete$',
        views.SettingsCategoriesDeleteView.as_view(),
        name='categories_delete'),

)


urlpatterns = patterns(
    '',

    url(r'^$', views.HomeView.as_view(), name='home',
        kwargs={'show': 'open'}),
    url(r'^closed/$', views.HomeView.as_view(), name='closed',
        kwargs={'show': 'closed'}),

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

    url(r'^settings/', include(settings_urls, namespace='settings')),

    url(r'^crashme/', views.CrashMe.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^select2/', include('django_select2.urls')),

    url(r'^notifications/',
        include('notifications.urls', namespace='notifications')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
