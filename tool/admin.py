from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth import get_user_model

from media.admin import TaggedPhotoInline
from lablackey.db.admin import OrderedModelAdmin
from .models import Lab, Tool, ToolLink, TaggedTool, Group, Permission, Criterion, UserCriterion

@admin.register(Lab)
class LabAdmin(OrderedModelAdmin):
  inlines = (TaggedPhotoInline,)
  raw_id_fields = ('photo',)

class ToolLinkInline(admin.TabularInline):
  extra = 0
  model = ToolLink
  fields = ("title","url","order")

@admin.register(Tool)
class ToolAdmin(OrderedModelAdmin):
  inlines = (ToolLinkInline,TaggedPhotoInline)
  list_display = ('__unicode__','has_links','has_description','_materials',"room","lab",'order','permission')
  list_filter = ('lab','functional')
  filter_horizontal = ('materials',)
  list_editable = ('permission',)
  readonly_fields = ('has_links','has_description')
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "permission":
      kwargs["queryset"] = Permission.objects.all().order_by("name")
    return super(ToolAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
  def has_links(self,obj):
    return bool(obj.links())
  has_links.boolean = True
  def has_description(self,obj):
    return bool(obj.description)
  has_description.boolean = True
  def _materials(self,obj):
    m = obj.materials
    if not m.count():
      return'<img src="/static/admin/img/icon-no.gif" alt="False">'
    return "%s (%s)"%(m.filter(parent__isnull=True).count(),m.filter(parent__isnull=False).count())
  _materials.allow_tags = True

#See note above corresponding model
class TaggedToolInline(GenericTabularInline):
  model = TaggedTool
  raw_id_fields = ('tool',)
  extra = 0

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
class GroupedToolForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super(GroupedToolForm,self).__init__(*args,**kwargs)
    """choices = {}
    for tool in Tool.objects.all():
      room = unicode(tool.room)
      choices[room] = choices.get(room,[])
      choices[room].append((tool.pk,unicode(tool)))
    choices = tuple(sorted(choices.items()))"""
    choices = [(tool.pk,tool.choice_name) for tool in Tool.objects.all()]
    choices = sorted(choices,key=lambda i:i[1])
    self.fields["tools"].choices = choices

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','row','column','color')
  list_editable = ('row','column','color')

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
  filter_horizontal = ('criteria',)
  list_editable = ('group',"order",)
  list_display = ('__unicode__','abbreviation','group','order','_criteria')
  fields = (('name','abbreviation'),('group','room'),'tools','criteria')
  _criteria = lambda self,obj: '<br/>'.join([unicode(criteria) for criteria in obj.criteria.all()])
  _criteria.allow_tags = True
  _criteria.short_description = "Required Criteria"
  form = GroupedToolForm

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
  filter_horizontal = ("courses",)

@admin.register(UserCriterion)
class UserCriterionAdmin(admin.ModelAdmin):
  raw_id_fields = ('user',)
  readonly_fields = ("content_type","object_id",'criterion')
