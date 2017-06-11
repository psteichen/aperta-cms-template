#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.utils import timezone

from django_tables2  import RequestConfig
from headcrumbs.decorators import crumb
from headcrumbs.util import name_from_pk

from cms.functions import notify_by_email, show_form, visualiseDateTime

from members.models import Member

from .models import Payment, BankExtract
from .forms import BankExtractForm
from .tables  import BankExtractTable


#################
# FINANCE VIEWS #
#################

# list #
########
#@permission_required('cms.BOARD',raise_exception=True)
#def list(r):
#
#  table = PaymentTable(Payment.objects.all().order_by('-sender'))
#  RequestConfig(r, paginate={"per_page": 75}).configure(table)
#
#  return render(r, settings.TEMPLATE_CONTENT['finance']['template'], {
#                   'title': settings.TEMPLATE_CONTENT['finance']['title'],
#                   'desc': settings.TEMPLATE_CONTENT['finance']['desc'],
#                   'actions': settings.TEMPLATE_CONTENT['finance']['actions'],
#                   'table': table,
##                })


# bank #
########
@permission_required('cms.BOARD',raise_exception=True)
@crumb(u'Bank')
def bank(r):

  table = BankExtractTable(BankExtract.objects.all().order_by('-year').order_by('-num'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return TemplateResponse(r, settings.TEMPLATE_CONTENT['finance']['bank']['template'], {
                   'title': settings.TEMPLATE_CONTENT['finance']['bank']['title'],
                   'desc': settings.TEMPLATE_CONTENT['finance']['bank']['desc'],
                   'actions': settings.TEMPLATE_CONTENT['finance']['bank']['actions'],
                   'table': table,
                })

# upload #
##########
@permission_required('cms.BOARD',raise_exception=True)
@crumb(u'Bank',parent=bank)
def upload(r):

  form_template	= settings.TEMPLATE_CONTENT['finance']['bank']['upload']['template']
  form_title	= settings.TEMPLATE_CONTENT['finance']['bank']['upload']['title']
  form_desc	= settings.TEMPLATE_CONTENT['finance']['bank']['upload']['desc']
  form_submit	= settings.TEMPLATE_CONTENT['finance']['bank']['upload']['submit']

  done_template	= settings.TEMPLATE_CONTENT['finance']['bank']['upload']['done']['template']
  done_url	= settings.TEMPLATE_CONTENT['finance']['bank']['upload']['done']['url']

  if r.POST:
    bef = BankExtractForm(r.POST,r.FILES)
    if bef.is_valid():
      BE = bef.save(commit=False)
      BE.save()
      
      # all fine -> done
      return redirect(done_url)

    # form not valid -> error
    else:
      return TemplateResponse(r, done_template, {
                	'title'		: done_title, 
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in bef.errors]),
                   })
  # no post yet -> empty form
  else:
    form = BankExtractForm()
    return TemplateResponse(r, form_template, {
                	'title'	: form_title,
                	'desc'	: form_desc,
                	'submit': form_submit,
                	'form'	: form,
                })


