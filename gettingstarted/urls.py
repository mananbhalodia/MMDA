from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
#import hello.views
from django.conf import settings
from django.conf.urls.static import static

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    #url(r'^$', hello.views.index, name='index'),
    #url(r'^hello/', include('hello.urls', namespace='hello')),
    #url(r'^db', hello.views.db, name='db'),

    url(r'^dagr/', include('dagr.urls', namespace='dagr')),

    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
