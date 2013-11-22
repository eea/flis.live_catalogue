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
    url(r'^api/keywords$', login_required(views.ApiKeywords.as_view()), name='api_keywords'),
    url(r'^need/add$', login_required(views.NeedEdit.as_view()), name='need_edit'),
    url(r'^need/(?P<pk>[\w\-]+)/edit$', login_required(views.NeedEdit.as_view()), name='need_edit'),
    url(r'^need/(?P<pk>[\w\-]+)$', login_required(views.CatalogueView.as_view()),
        {'kind': 'need'}, name='catalogue_view'),

    url(r'^offer/add$', login_required(views.OfferEdit.as_view()), name='offer_edit'),
    url(r'^offer/(?P<pk>[\w\-]+)/edit$', login_required(views.OfferEdit.as_view()), name='offer_edit'),
    url(r'^offer/(?P<pk>[\w\-]+)$', login_required(views.CatalogueView.as_view()),
        {'kind': 'offer'}, name='catalogue_view'),

    url(r'^crashme/', login_required(views.CrashMe.as_view())),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^select2/', include('django_select2.urls')),
)
