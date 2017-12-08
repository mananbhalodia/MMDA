from django.conf.urls import url

from . import views

urlpatterns = [
url(r'^$', views.add_manually, name='add'),
url(r'^message/(?P<message>\w+)/$', views.message, name='message'),
url(r'^add/manually/$', views.add_manually, name='add_manually'),
url(r'^add/url/$', views.add_url, name='add_url'),
url(r'^add/file/$', views.add_file, name='add_file'),
url(r'^add/category/$', views.add_category, name="add_category"),
url(r'^add/keyword/$', views.add_keyword, name="add_keyword"),


#url(r'^queries/$', views.queries, name='dagr_queries'),
url(r'^metadata/$', views.metadata, name='metadata'),
url(r'^reach/$', views.reach, name='reach'),
url(r'^time/(?P<rang>\w+)/$', views.time_range, name='time-range'),
url(r'^time/$', views.time, name='time'),
url(r'^family/(?P<descendant>\w+)/$', views.descendant, name='descendant'),
url(r'^update/(?P<guid>\d+)/$', views.update_dagr, name='update_dagr'),
url(r'^delete/(?P<guid>\d+)/$', views.delete_dagr, name='delete_dagr'),
]
