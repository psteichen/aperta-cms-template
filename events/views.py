
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.template.response import TemplateResponse
from django.conf import settings
from django.utils import timezone

from django_tables2  import RequestConfig
from formtools.wizard.views import SessionWizardView

from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk
	
from cms.functions import notify_by_email, group_required

from members.models import Member
from members.functions import get_active_members, gen_member_fullname, is_board
from attendance.functions import gen_invitation_message, gen_hash, gen_attendance_hashes

from .functions import gen_event_overview, gen_event_initial
from .models import Event, Invitation
from .forms import EventForm, ListEventsForm
from .tables  import EventTable, MgmtEventTable


################
# EVENTS VIEWS #
################

# list #
########
@group_required('MEMBER')
@crumb(u'Évènements')
def list(r):

  table = EventTable(Event.objects.all().order_by('-id'))
  if is_board(r.user):
    table = MgmtEventTable(Event.objects.all().order_by('-id'))

  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['template'], {
                   'title': settings.TEMPLATE_CONTENT['events']['title'],
                   'actions': settings.TEMPLATE_CONTENT['events']['actions'],
                   'table': table,
                })



# add #
#######
@group_required('BOARD')
@crumb(u'Ajouter un évènement',parent=list)
def add(r):

  if r.POST:

    ef = EventForm(r.POST)
    if ef.is_valid():
      Ev = ef.save(commit=False)
      Ev.save()
      
      if r.FILES:
        I = Invitation(event=Ev,message=ef.cleaned_data['additional_message'],attachement=r.FILES['attachement'])
      else:
        I = Invitation(event=Ev,message=ef.cleaned_data['additional_message'])
      I.save()

      # all fine -> done
      I.save()
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['add']['done']['template'], {
                	'title': settings.TEMPLATE_CONTENT['events']['add']['done']['title'], 
	                'message': settings.TEMPLATE_CONTENT['events']['add']['done']['message'].format(event=Ev,message=I.message,attachement=I.attachement,list=u' ; '.join([gen_member_fullname(m) for m in get_active_members()])),
		   })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in ef.errors]),
                })
  # no post yet -> empty form
  else:
    form = EventForm()
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['events']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['events']['add']['submit'],
                'form': form,
                })


# send #
########
@group_required('BOARD')
def send(r,event_id):

  e_template =  settings.TEMPLATE_CONTENT['events']['send']['done']['email']['template']

  Ev = Event.objects.get(id=event_id)
  I = Invitation.objects.get(event=Ev)

  title = settings.TEMPLATE_CONTENT['events']['send']['done']['title'] % unicode(Ev.title)
      
  email_error = { 'ok': True, 'who': (), }
  for m in get_active_members():
   
    #invitation email with "YES/NO button"
    subject = settings.TEMPLATE_CONTENT['events']['send']['done']['email']['subject'] % { 'title': unicode(Ev.title) }
    invitation_message = gen_invitation_message(e_template,Ev,Event.OTH,m)
    message_content = {
      'FULLNAME'    : gen_member_fullname(m),
      'MESSAGE'     : invitation_message,
    }
    #send email
    ok=notify_by_email(r.user.email,m.email,subject,message_content)
    if not ok: 
      email_error['ok']=False
      email_error['who'].add(m.email)

  # error in email -> show error messages
  if not email_error['ok']:
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
        	        'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                  })

  # all fine -> done
  else:
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
        	        'message': settings.TEMPLATE_CONTENT['events']['send']['done']['message'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                  })
 

# details #
###########
@group_required('MEMBER')
@crumb(u"Détail d'un évènement",parent=list)
def details(r, event_id):

  event = Event.objects.get(pk=event_id)
  title = settings.TEMPLATE_CONTENT['events']['details']['title'] % { 'event' : event.title, }
  message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['details']['overview']['template'],event)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['details']['template'], {
                   'title': title,
                   'message': message,
                })


# modify  #
###########
@group_required('BOARD')
@crumb(u"Modifier un évènement",parent=list)
def modify(r, event_id):

  E = Event.objects.get(pk=event_id)

  if r.POST:

    ef = EventForm(r.POST,instance=E)
    if ef.is_valid():
      Ev = ef.save(commit=False)
      Ev.save()
      
      # all fine -> done
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['modify']['done']['template'], {
                	'title': settings.TEMPLATE_CONTENT['events']['modify']['done']['title'].format(event=unicode(Ev)), 
		   })

    # form not valid -> error
    else:
      return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['modify']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['modify']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in ef.errors]),
                })

  # no post yet -> empty form
  else:
    form = EventForm()
    form.initial = gen_event_initial(E)
    return TemplateResponse(r, settings.TEMPLATE_CONTENT['events']['modify']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['modify']['title'],
                'desc': settings.TEMPLATE_CONTENT['events']['modify']['desc'],
                'submit': settings.TEMPLATE_CONTENT['events']['modify']['submit'],
                'form': form,
                })




