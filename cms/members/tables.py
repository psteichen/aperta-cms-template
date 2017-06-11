#coding=utf-8

from datetime import date

from django.conf import settings
from django_tables2.tables import Table
from django_tables2 import Column, LinkColumn
from django_tables2.utils import A

from django.utils.safestring import mark_safe
from django.utils.html import escape

from attendance.models import Meeting_Attendance

from .models import Member, Role

#table for visualisation via django_tables2
class MemberTable(Table):
  role		= Column(verbose_name=u'Rôle',empty_values=())
  meetings	= Column(verbose_name=u'RS (présent / excusé)',empty_values=())

  def __init__(self, *args, **kwargs):
    if kwargs["username"]:
      self.username = kwargs["username"]
      kwargs.pop('username',False)
    super(Table, self).__init__(*args, **kwargs)

  def render_photo(self, value, record):
    picture = '''<i class="fa-stack fa-3x"><a href="#{id}Modal" data-toggle="modal"><img src="{pic}" alt="Photo" class="img-responsive img-circle" /></a></i>

<!-- Modal -->
<div class="modal fade" id="{id}Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">{name}</h4>
      </div> 
      <div class="modal-body">
        <center><img src="{pic}" alt="Photo" class="img-responsive img-rounded" /></center>
      </div>
    </div>
  </div>
</div>
'''.format(id=record.pk,name=unicode(record),pic=settings.MEDIA_URL+unicode(value))

    return mark_safe(picture)

  def render_last_name(self, value):
    return unicode.upper(value)

  def render_role(self, value, record):
    try:
      role = Role.objects.get(member__id=record.id)
      if role.end_date:
        return unicode(role.title) + ' (' + unicode(role.start_date) + ' - ' + unicode(role.end_date) +')'
      else:
        return unicode(role.title) + ' (depuis ' + unicode(role.start_date) + ')'
    except:
      return ''

  def render_meetings(self, record):
    MA = Meeting_Attendance.objects.filter(member=record)
    ma = ' {} / {} '.format(MA.filter(present=True).count(),MA.filter(present=False).count())
    mod = ''
    if self.username == record.user.username: 
      mod = '<a class="btn btn-danger btn-sm pull-right" href="/members/profile/modify/{}/"><i class="fa fa-pencil"></i></a>'.format(escape(record.user))
    return mark_safe(ma + mod)


  class Meta:
    model = Member
    fields = ( 'photo', 'first_name', 'last_name', 'address', 'email', 'mobile', 'status', 'role', 'meetings', )
    attrs = {"class": "table table-striped"}

#management table
class MgmtMemberTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  role		= Column(verbose_name=u'Rôle',empty_values=())
  meetings	= Column(verbose_name=u'RS (présent / excusé)',empty_values=())
  modify	= Column(verbose_name=u'Modifier',empty_values=())

  def render_row_class(self, value, record):
    cl = ''
    if record.status == Member.ACT:
      cl = 'success'
    if record.status == Member.WBE:
      cl = 'info'

    att = record.attendance.all().count()
    exc = record.excused.all().count()
    if att == 0:
      cl = 'warning'
    if record.end_date or record.status == Member.STB or (att == 0 and exc == 0):
      cl = 'danger'

    return cl

  def render_photo(self, value, record):
    picture = u'''<i class="fa-stack fa-3x"><a href="#{id}Modal" data-toggle="modal"><img src="{pic}" alt="Photo" class="img-responsive img-circle" /></a></i>

<!-- Modal -->
<div class="modal fade" id="{id}Modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">{name}</h4>
      </div> 
      <div class="modal-body">
        <center><img src="{pic}" alt="Photo" class="img-responsive img-rounded" /></center>
      </div>
    </div>
  </div>
</div>
'''.format(id=record.pk,name=unicode(record),pic=settings.MEDIA_URL+unicode(value))

    return mark_safe(picture)

  def render_last_name(self, value):
    return unicode.upper(value)

#  def render_start_date(self, value):
#    return format_datetime(value)

#  def render_end_date(self, value):
#    return format_datetime(value)

  def render_role(self, value, record):
    try:
      role = Role.objects.get(member__id=record.id)
      if role.end_date:
        return unicode(role.title) + ' (' + unicode(role.start_date) + ' - ' + unicode(role.end_date) +')'
      else:
        return unicode(role.title) + ' (depuis ' + unicode(role.start_date) + ')'
    except:
      return ''

  def render_meetings(self, record):
    MA = Meeting_Attendance.objects.filter(member=record)
    return '{} / {}'.format(MA.filter(present=True).count(),MA.filter(present=False).count())

  def render_modify(self, record):
    link = '<a class="btn btn-danger btn-sm" href="/members/modify/{}/"><i class="fa fa-pencil"></i></a>'.format(escape(record.pk))
    return mark_safe(link)


  class Meta:
    model = Member
    fields = ( 'photo', 'first_name', 'last_name', 'email', 'start_date', 'end_date', 'status', 'role', 'meetings', )
    attrs = {"class": "table table-striped"}
