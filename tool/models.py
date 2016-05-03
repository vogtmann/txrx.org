from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from geo.models import Room
from lablackey.db.models import SlugModel, OrderedModel
from lablackey.utils import cached_property, cached_method
from media.models import Photo, PhotosMixin
from wmd.models import MarkDownField

from colorful.fields import RGBColorField
import json, os, datetime

class Lab(PhotosMixin,OrderedModel):
  name = models.CharField(max_length=128)
  __unicode__ = lambda self: self.name
  slug = property(lambda self: slugify(self.name))
  photo = models.ForeignKey(Photo,null=True,blank=True)
  description = models.TextField(null=True,blank=True)
  url = lambda self: reverse("lab_detail",args=[self.slug,self.id])
  class Meta:
    ordering = ("order",)

_help = "Will default to %s photo if blank"

class Tool(PhotosMixin,OrderedModel):
  name = models.CharField(max_length=128)
  __unicode__ = lambda self: self.name
  value = property(lambda self: self.pk)
  slug = property(lambda self: slugify(self.name))
  lab = models.ForeignKey(Lab)
  make = models.CharField(max_length=64,null=True,blank=True)
  model = models.CharField(max_length=32,null=True,blank=True)
  description = MarkDownField(blank=True,null=True)
  est_price = models.FloatField(null=True,blank=True)
  links = lambda self: self.toollink_set.all()
  materials = models.ManyToManyField("thing.Material",blank=True)
  room = models.ForeignKey(Room,null=True,blank=True)
  get_absolute_url = lambda self: reverse("tool_detail",args=[self.slug,self.id])
  functional = models.BooleanField(default=True)
  repair_date = models.DateField(null=True,blank=True)
  permission = models.ForeignKey("Permission",null=True,blank=True)
  get_status = lambda self: "Functional" if self.functional else "Non-functional"
  @property
  def choice_name(self):
    if self.room:
      return "(%s) %s"%(self.room.name,self.name)
    return self.name
  class Meta:
    ordering = ("lab","order")
  # Abstract the next two!
  @cached_property
  def courses(self):
    ct_id = ContentType.objects.get(model="course").id
    tagged = list(TaggedTool.objects.filter(content_type__id=ct_id,tool=self))
    return [t.content_object for t in tagged]
  @cached_property
  def ordered_courses(self):
    singles = []
    groups = []
    for criterion in self.permission.criteria.all():
      if criterion.courses.count() == 1:
        singles.append(criterion.courses.all()[0])
      elif criterion.courses.all():
        groups.append(criterion.courses.all())
    return singles,groups
  single_courses = property(lambda self: self.ordered_courses[0])
  group_courses = property(lambda self: self.ordered_courses[1])
  number_required_courses = property(lambda self: len(self.single_courses) + len(self.group_courses))
  @cached_property
  def things(self):
    ct_id = ContentType.objects.get(model="thing").id
    tagged = list(TaggedTool.objects.filter(content_type__id=ct_id,tool=self))
    return [t.content_object for t in tagged]
  @property
  def as_json(self):
    fields = ['id','name']
    return {field:getattr(self,field) for field in fields}

class ToolLink(OrderedModel):
  tool = models.ForeignKey(Tool)
  title = models.CharField(max_length=64)
  url = models.URLField()
  __unicode__ = lambda self: self.title
  class Meta:
    ordering = ("order",)

# This and ToolsMixin could probably be combined into some sort of generic foreign key factory
class TaggedTool(models.Model):
  tool = models.ForeignKey(Tool)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  order = models.IntegerField(default=9999)

class ToolsMixin(object):
  @cached_property
  def first_tool(self):
    return self.get_tools()[0]
  @cached_property
  def _ct_id(self):
    return ContentType.objects.get_for_model(self.__class__).id
  @cached_method
  def get_tools(self):
    return self._get_tools()
  def _get_tools(self):
    return list(Tool.objects.filter(
      taggedtool__content_type_id=self._ct_id,
      taggedtool__object_id=self.id).order_by("taggedtool__order"))
  class Meta:
    abstract = True

class Criterion(models.Model):
  name = models.CharField(max_length=32)

  # These fields will eventually need to be a generic many to many field but we don't have a ui for that
  courses = models.ManyToManyField('course.Course',blank=True)
  documents = models.ManyToManyField('redtape.Document',blank=True)
  __unicode__ = lambda self: self.name
  def user_can_grant(self,user):
    if user.is_toolmaster:
      return True
    for course in self.courses.all():
      if course.session_set.filter(user=user):
        return True
  @property
  def as_json(self):
    course_fields = ['id','name']
    courses_json = [{f:getattr(c,f) for f in course_fields} for c in self.courses.all()]
    return {
      'id': self.id,
      'name': self.name,
      'course_ids': list(self.courses.all().values_list('id',flat=True)),
      'courses': courses_json
    }
  class Meta:
    ordering = ('name',)

class UserCriterion(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  criterion = models.ForeignKey(Criterion)
  created = models.DateTimeField(auto_now_add=True)
  content_type = models.ForeignKey("contenttypes.ContentType")
  object_id = models.IntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  __unicode__ = lambda self: "%s for %s"%(self.user,self.criterion)

class CriterionModel(models.Model):
  """A model that will generate a user criterion upon completion"""
  datetime = models.DateTimeField(default=datetime.datetime.now)
  completed = models.DateTimeField(null=True,blank=True)
  automatic = False # If true criterion will be granted without completion
  def save(self,*args,**kwargs):
    if not self.pk and self.automatic:
      self.completed = datetime.datetime.now()
    super(CriterionModel,self).save(*args,**kwargs)
    if self.user and self.completed:
      for criterion in self.get_criteria():
        defaults = {'content_object':self}
        u,new = UserCriterion.objects.get_or_create(user=self.user,criterion=criterion,defaults=defaults)
        u.content_object = self
        u.save()
    else:
      m = self.__class__.__name__.lower()
      UserCriterion.objects.filter(content_type__model=m,object_id=self.id).delete()
  class Meta:
    abstract = True

class Group(models.Model):
  name = models.CharField(max_length=32)
  color = RGBColorField()
  column = models.IntegerField(choices=[(0,"left"),(1,"right")])
  row = models.IntegerField()
  @property
  def as_json(self):
    return {key:getattr(self,key) for key in ['id','name','color','row','column']}
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class Permission(models.Model):
  name = models.CharField(max_length=32)
  abbreviation = models.CharField(max_length=16,help_text="For badge.")
  room = models.ForeignKey(Room)
  group = models.ForeignKey(Group,null=True,blank=True)
  tools = models.ManyToManyField(Tool,blank=True,related_name="+")
  _ht = "Requires all these criteria to access these tools."
  criteria = models.ManyToManyField(Criterion,blank=True,help_text=_ht)
  order = models.IntegerField(default=999)
  __unicode__ = lambda self: self.name
  tools_json = property(lambda self: [t.as_json for t in self.tools.all()])
  criteria_json = property(lambda self: [c.as_json for c in self.criteria.all()])
  @property
  def as_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'abbreviation': self.abbreviation,
      'room_id': self.room_id,
      'tool_ids': list(self.tools.all().values_list('id',flat=True)),
      'criterion_ids': list(self.criteria.all().values_list('id',flat=True)),
      'criteria_json': self.criteria_json,
      'group_id': self.group_id,
      'tools_json': self.tools_json
    }
  def check_for_user(self,user):
    return all([UserCriterion.objects.filter(user=user,criterion=c).count() for c in self.criteria.all()])
  def get_all_user_ids(self,fieldname='user_id'):
    groups = []
    for criterion in self.criteria.all():
      groups.append(set(criterion.usercriterion_set.all().values_list(fieldname,flat=True)))
    return set.union(*groups)
  def get_grantable_criteria(self,user):
    return [c for c in self.criteria.all() if c.user_can_grant(user)]
  class Meta:
    ordering = ('group','order')

def reset_tools_json(context="no context provided"):
  values = {
    'permissions_json': json.dumps([p.as_json for p in Permission.objects.all()]),
    'groups_json': json.dumps([g.as_json for g in Group.objects.all().order_by("row","column")]),
    'criteria_json': json.dumps([c.as_json for c in Criterion.objects.all()])
  }
  text = render_to_string('tool/tools.json',values)
  f = open(os.path.join(settings.STATIC_ROOT,'_tools.json'),'w')
  f.write(text)
  f.close()
  os.rename(os.path.join(settings.STATIC_ROOT,'_tools.json'),os.path.join(settings.STATIC_ROOT,'tools.json'))

  dt = datetime.datetime.now()
