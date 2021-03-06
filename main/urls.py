from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset
from django.contrib.flatpages.models import FlatPage
from django.contrib.sitemaps.views import sitemap
from django.db.utils import ProgrammingError

from main.sitemaps import sitemaps
from main.feeds import AllFeed
import main.views, main.dashboard

import lablackey.blog.views
import store.urls, media.urls, event.urls, thing.views, tool.urls, tool.views
import paypal.standard.ipn.urls
import social.apps.django_app.urls
import unrest_comments.urls
import course.urls, course.views
import djstripe.urls
import contact.views, lablackey.geo.views, user.views
import redtape.urls
import membership.urls
import course.views.classes
import airbrake.urls
import txrx.urls
from lablackey.sms import urls as sms_urls
from lablackey.decorators import activate_user

import os

_urls = lambda *ns: [url(r'^%s/'%n, include('%s.urls'%n, namespace=n, app_name=n)) for n in ns]

_pages = [
  'checkin',
  'checkout',
  'todays-checkins',
  'my-permissions',
  'needed-sessions',
  'rooms',
  'toolmaster',
  'week-hours',
  'me',
  'admin/dashboard',
  'notify',
  'event/bulk',
  'auth/login'
]

urlpatterns = [
  url(r'^(%s)/$'%('|'.join(_pages)),main.views.beta),
  url(r'^$',main.views.index,name="home"),
  url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
  url(r'^dashboard/totals.(json|csv|table)$', main.dashboard.totals_json),
  url(r'^admin/', include(admin.site.urls)),
  url(r'arst/(?P<pk>\d+)',main.views.intentional_500,name="order_detail"),
  url(r'^(\d{4})/(\d{1,2})/(\d{1,2})/([^/]+)/',lablackey.blog.views.post_redirect),
  url(r'^500/$',main.views.intentional_500),
  url(r'^event/',include(event.urls,namespace="event",app_name="event")),
  url(r'^media_files/',include(media.urls)),
  url(r'^shop/',include(store.urls)),
  url(r'^product_is_a_fail/(.*)/$',main.views.index,name="product_detail"),
  url(r'^comments/',include(unrest_comments.urls)),
  url(r'^rss/$', AllFeed()),
  url(r'^favicon.ico$',main.views.predirect,
      kwargs={'url':getattr(settings,'FAVICON','/static/favicon.ico')}),
  url(r'^sculpturemonth$',main.views.predirect,
      kwargs={'url':"/classes/221/3d-modeling-with-rhino/?rhino10"}),
  url(r'^rapidfabstudio$',main.views.predirect,
      kwargs={'url':"/event/detail/133/rapid-fab-studio-hours/"}),
  url(r'^3dprinting/$',main.views.predirect,
      kwargs={'url':"/classes/37/3d-printing-i/"}),
  url(r'^thing/$',thing.views.thing_index,name='thing_index'),
  url(r'^thing/add/$',thing.views.add_thing,name='add_thing'),
  url(r'^thing/(\d+)/([\w\d\-\_]+)/$',thing.views.thing_detail,name='thing_detail'),
  url(r'^gfycat/$',main.views.gfycat,name='gfycat'),
  url(r'^tools/',include(tool.urls)),
  url(r'^borrow/$',tool.views.checkout_items,name='checkout_items'),
  url('', include(social.apps.django_app.urls, namespace='social')),
  url(r'perfect-programming',main.views.intentional_500),
  url(r'^classes/', include(course.urls,namespace='course',app_name='course')),
  url(r'^gift/$',course.views.classes.index),
  url(r'^tx/rx/ipn/handler/', include(paypal.standard.ipn.urls)),
  url(r'^tx/rx/return/$',course.views.paypal_return,name='paypal_redirect'),
  url(r'^payments/', include(djstripe.urls, namespace="djstripe")),
  url(r'^contact/$',contact.views.contact,name='contact'),
  url(r'^contact/(\w+).(\w+)_(\d+)-(.*).png$',contact.views.tracking_pixel,name="tracking_pixel"),
  url(r'^dxfviewer/$',lablackey.geo.views.dxfviewer,name='dxfviewer'),
  url(r'^geo/events.json',lablackey.geo.views.events_json),
  url(r'^geo/locations.json$',lablackey.geo.views.locations_json),
  url(r'^checkin_ajax/$', user.views.checkin_ajax, name='checkin_ajax'),
  url(r'^checkin_email/$', user.views.checkin_email, name='checkin_email'),
  url(r'^checkin_register/$', user.views.checkin_register, name='checkin_register'),
  url(r'^add_rfid/$', user.views.add_rfid, name='add_rfid'),
  url(r'^user.json',user.views.user_json),
  url(r'^todays_checkins.json',user.views.todays_checkins_json),
  url(r'^redtape/',include(redtape.urls)),
  url(r'',include(airbrake.urls)),
  url(r'',include(txrx.urls)),
  url(r'',include(sms_urls)),
]

def _include(s):
  return include(__import__(s).urls)

import membership.views
import django.contrib.auth.urls
import lablackey.urls
import notify.urls
from user.forms import PasswordResetForm

#auth related
urlpatterns += [
  url(r'^accounts/settings/$',membership.views.user_settings,name='account_settings'),
  url(r'^accounts/register/$',membership.views.register,name="account_register"),
  url(r'^accounts/(cancel)_subscription/',membership.views.change_subscription,name="cancel_subscription"),
  #! TODO Move the following to lablackey.registration, write test, and make activate AFTER password is reset
  url(r'^auth/password_reset/$',activate_user(password_reset),kwargs={'password_reset_form': PasswordResetForm}),
  url(r'^auth/',include(django.contrib.auth.urls)),
  url(r'^force_login/([\d\w]+)/$', main.views.force_login),
  url(r'^api/remove_rfid/$',user.views.remove_rfid),
  url(r'^api/change_rfid/$',user.views.set_rfid),
  url(r'^api/user_checkin/$',user.views.user_checkin),
  url(r'^api/change_(headshot|id_photo)/$',user.views.change_headshot),
  url(r'',_include('membership.urls')),
  url(r'',_include('rfid.urls')),
  url(r'',include(lablackey.urls)),
  url(r'^notify/',include(notify.urls)),
  #url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
]

if hasattr(settings,"STAFF_URL"):
  urlpatterns += [url(settings.STAFF_URL[1:],user.views.hidden_image)]

urlpatterns += [
  url(r'^(about-us)/$',main.views.to_template),
]

from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test

is_superuser = lambda user:user.is_superuser
urlpatterns += [
    url(r'^media/(?P<path>signatures/.*)$',user_passes_test(is_superuser)(serve),
        {'document_root': settings.MEDIA_ROOT,'show_indexes': False})
]
if settings.DEBUG:
  urlpatterns += [
    url(r'^media/(?P<path>.*)$',serve,
        {'document_root': settings.MEDIA_ROOT,'show_indexes': True})
  ]

# Turn me on to enable "maintenance mode"
if False:
  urlpatterns = [
    url(r'^(maintenance)/$',main.views.beta),
    url(r'^admin/', include(admin.site.urls)),
    url(r'',main.views.predirect,kwargs={'url': "/maintenance/"},name="logout"),
  ]
