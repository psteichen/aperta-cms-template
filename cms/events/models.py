# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField, FileField

from cms.functions import rmf

from members.models import Member
from locations.models import Location

class Event(Model):
  MEET = 0
  OTH = 1
  TYPES = (
    (MEET, 'Réunion statutaire'),
    (OTH,  'Autre Evénement/Rencontre'),
  )

  title		= CharField(verbose_name='Titre',max_length=100)
  when		= DateField(verbose_name='Date')
  time		= TimeField(verbose_name='Heure de début')
  location	= ForeignKey(Location,verbose_name='Lieu')
  deadline	= DateTimeField(verbose_name='Deadline')
  
  def __unicode__(self):
    return unicode(self.title) + ' du ' + unicode(self.when)


def rename_attach(i, f):
  fn = rmf('events', f, str(i.event.pk) + '-attachement')

  from os import sep
  return fn['name'] + fn['ext']


class Invitation(Model):
  event		= ForeignKey(Event)
  message	= CharField(max_length=5000,blank=True,null=True)
  attachement   = FileField(verbose_name='Annexe(s)', upload_to=rename_attach,blank=True,null=True)
  sent		= DateTimeField(blank=True,null=True)

  def __unicode__(self):
    if self.sent:
      return u'Invitations pour: ' + unicode(self.event) + u' envoyées à: ' + self.sent.strftime('%Y-%m-%d %H:%M')
    else:
      return u'Invitations pour: ' + unicode(self.event) + u' non encore envoyées.'



