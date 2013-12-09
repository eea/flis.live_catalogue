from django.conf.urls import patterns, include, url
from django.contrib import admin
from live_catalogue import views
from live_catalogue.auth import login_required


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'live_catalogue.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login_required(views.HomeView.as_view()), name='home'),
    url(r'^need/add$', login_required(views.CatalogueEdit.as_view()),
       {'kind': 'need'}, name='catalogue_add'),
    url(r'^need/(?P<pk>[\w\-]+)/edit$', login_required(views.CatalogueEdit.as_view()),
        {'kind': 'need'}, name='catalogue_edit'),
    url(r'^need/(?P<pk>[\w\-]+)/delete$', login_required(views.CatalogueDelete.as_view()),
        {'kind': 'need'}, name='catalogue_delete'),
    url(r'^need/(?P<pk>[\w\-]+)$', login_required(views.CatalogueView.as_view()),
        {'kind': 'need'}, name='catalogue_view'),

    url(r'^offer/add$', login_required(views.CatalogueEdit.as_view()),
        {'kind': 'offer'}, name='catalogue_add'),
    url(r'^offer/(?P<pk>[\w\-]+)/edit$', login_required(views.CatalogueEdit.as_view()),
        {'kind': 'offer'}, name='catalogue_edit'),
    url(r'^offer/(?P<pk>[\w\-]+)/delete$', login_required(views.CatalogueDelete.as_view()),
        {'kind': 'offer'}, name='catalogue_delete'),
    url(r'^offer/(?P<pk>[\w\-]+)$', login_required(views.CatalogueView.as_view()),
        {'kind': 'offer'}, name='catalogue_view'),

    url(r'my', login_required(views.MyEntries.as_view()), name='my_entries'),

    url(r'^crashme/', login_required(views.CrashMe.as_view())),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^select2/', include('django_select2.urls')),
)
