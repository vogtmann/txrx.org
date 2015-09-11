from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms

from models import (Group, Membership, Feature, MembershipFeature, UserMembership, Product,
                    Subscription, Status, MeetingMinutes, Proposal, Officer, Area, Container)

from lablackey.db.admin import RawMixin
from lablackey.db.forms import StaffMemberForm

admin.site.register(Feature)
admin.site.register(Group)

class ContainerInline(admin.TabularInline):
  model = Container

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
  pass

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
  inlines = [ContainerInline]

class MembershipFeatureInline(RawMixin,admin.TabularInline):
  extra = 0
  raw_id_fields = ('membership','feature')
  model = MembershipFeature

class ProductInline(admin.TabularInline):
  extra = 0
  model = Product
  exclude = ('slug',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
  list_display = ("name","order")
  list_editable = ("order",)
  inlines = (MembershipFeatureInline, ProductInline)

class StatusInline(admin.TabularInline):
  model = Status
  raw_id_fields = ('paypalipn',)
  extra = 0

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
  inlines = [StatusInline]

class SubscriptionInline(admin.TabularInline):
  model = Subscription
  readonly_fields = ('edit','subscr_id','created','canceled','paid_until','product','amount','owed')
  ordering = ('-canceled',)
  raw_id_fields = ('container',)
  extra = 0
  has_add_permission = lambda self,obj: False
  def edit(self,obj):
    return "<a class='related-widget-wrapper-link change-related' href='/admin/membership/subscription/%s/'></a>"%obj.pk
  edit.allow_tags = True

class UserMembershipInline(admin.StackedInline):
  list_display = ("__unicode__",'photo')
  list_editable = ('photo',)
  list_filter = ('user__is_staff',)
  search_fields = ('user__email','user__username','paypal_email')
  readonly_fields = ('start','end','membership')
  raw_id_fields = ('photo',)
  fields = (
    'membership','bio','paypal_email',
    ('voting_rights','suspended'),
    ('photo','waiver'),
    ('start','end')
  )
  model = UserMembership

class ProposalInline(admin.StackedInline):
  model = Proposal
  fields = ('order','title','user','original','ammended')
  extra = 0

class MeetingMinutesForm(forms.ModelForm):
  User = get_user_model()
  kwargs = dict(widget=forms.CheckboxSelectMultiple(),required=False)
  _q = User.objects.filter(usermembership__voting_rights=True,usermembership__suspended=False)
  voters_present = forms.ModelMultipleChoiceField(queryset=_q,**kwargs)
  _q = User.objects.filter(usermembership__voting_rights=True,usermembership__suspended=True)
  kwargs = dict(widget=forms.CheckboxSelectMultiple(),required=False)
  inactive_present = forms.ModelMultipleChoiceField(queryset=_q,**kwargs)
  class Meta:
    model = MeetingMinutes
    exclude = ()

@admin.register(MeetingMinutes)
class MeetingMinutesAdmin(admin.ModelAdmin):
  form = MeetingMinutesForm
  inlines = [ProposalInline]
  fields = ('date','content',('voters_present','inactive_present'),'nonvoters_present')
  filter_horizontal = ('nonvoters_present',)

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
  form = StaffMemberForm
