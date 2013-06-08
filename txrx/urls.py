from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os

admin.autodiscover()

_urls = lambda *ns: [url(r'^%s/'%n, include('%s.urls'%n, namespace=n, app_name=n)) for n in ns]

urlpatterns = patterns(
  '',
  url(r'^$','txrx.views.blog_home',name="home"),
  url(r'admin/event/edit_photoset/(\d+)/$','event.views.edit_photoset'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^blog/$','txrx.views.blog_home'),
  url(r'^blog/',include('codrspace.urls')),
  url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/([^/]+)/','codrspace.views.post_redirect'),
  url(r'^grappelli/', include('grappelli.urls')),
  url(r'^500/$','txrx.views.intentional_500'),
  url(r'^event/',include('event.urls',namespace="event",app_name="event")),
  url(r'^instagram/',include('instagram.urls',namespace="instagram",app_name="instagram")),

  # comments and javascript translation
  url(r'^comments/', include('mptt_comments.urls')),
  url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

#auth related
urlpatterns += patterns(
  '',
  url(r'^accounts/settings/$','membership.views.settings',name='account_settings'),
  url(r'^accounts/', include('registration.backends.default.urls')),
  url(r'^password-reset/', include('password_reset.urls')),
  url(r'^force_login/(\d+)/$', 'txrx.views.force_login'),
)

#class related
urlpatterns += patterns(
  'course.views',
  url(r'^classes/', include('course.urls',namespace='course',app_name='course')),
  url(r'^instructors/$','instructors',name='instructor_index'),
  url(r'^instructors/([^/]+)/$','instructor_detail',name='instructor_detail'),
  url(r'^tx/rx/ipn/handler/', include('paypal.standard.ipn.urls')),
)

#membership urls
urlpatterns += patterns(
  '',
  url(r'^join-us/$','membership.views.join_us'),
  url(r'^membership/$', include('membership.urls')),
  url(r'^minutes/$', 'membership.views.minutes_index', name='meeting_minutes_index',),
  url(r'^minutes/(\d+-\d+-\d+)/$', 'membership.views.minutes', name='meeting_minutes',),
)

# todo
urlpatterns += patterns(
  '',
  (r'^survey/$','txrx.views.survey'),
  url(r'^tools/',include('tool.urls')),
)

# flat pages
urlpatterns += patterns(
  '',
  url(r'^(schoolbot/|map/|about-us/|bylaws/)$','django.contrib.flatpages.views.flatpage',name='map'),
)

if settings.DEBUG:
  urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$',
      'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT,
       'show_indexes': True}),
    )

