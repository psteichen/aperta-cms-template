# coding=utf-8

from .core_settings import *

######################
## (LOCAL) SETTINGS ##
######################

SECRET_KEY = '[GENERATE SECRET KEY]'
DEBUG = True

DOMAIN = 'example.org'
ALLOWED_HOSTS = [ 'your-host.'+DOMAIN, ]

# Email settings
SERVER_EMAIL = 'admin@'+DOMAIN
DEFAULT_FROM_EMAIL = 'board@'+DOMAIN

ADMINS = (
  ('Admin', SERVER_EMAIL),
)
MANAGERS = ADMINS

EMAILS = {
  'sender' : {
    'default'	: '"FIFTY-ONE Aperta" <board@'+DOMAIN+'>',
  },
  'footer' 	: '''Amicalement,
Le comité APERTA
''',
}

#content for templates and views
TEMPLATE_CONTENT = {
  #basic/generic content for all templates/views:
  'meta' : {
    'author'            : 'Pascal Steichen - pst@libre.lu',
    'copyright'         : 'FIFTY-ONE Luxembourg APERTA a.s.b.l.',
    'title'             : 'Club Management System',
    'logo' : {
      'title'		: 'FIFTY-ONE<br/><strong><em>APERTA</em></strong>',
      'img'		: 'https://'+DOMAIN+'/pics/logo-51-aperta_picto.png',
      'url'             : '/',
    },
    'description'       : '',
    'keywords'          : '',
    'favicon'		: STATIC_URL + '/favicon.ico',
    'css' : {
        'bt'      	: '//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css',
        'bt_theme'      : '//maxcdn.bootstrapcdn.com/bootswatch/3.3.4/yeti/bootstrap.min.css',
        'own'           : STATIC_URL + 'css/own.css',
        'dtpicker'      : '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/css/bootstrap-datetimepicker.min.css',
    },
    'js' : {
        'jq'      	: '//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min.js',
        'bt'       	: '//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js',
        'fontawesome'   : '//use.fontawesome.com/c8a990aa54.js',
        'momentjs'      : '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.3/moment-with-locales.min.js',
        'dtpicker'      : '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.7.14/js/bootstrap-datetimepicker.min.js',
    },
  },
  'error' : {
    400 : {
      'template'	: 'error400.html',
    },
    403 : {
      'template'	: 'error403.html',
    },
    404 : {
      'template'	: 'error404.html',
    },
    500 : {
      'template'	: 'error500.html',
    },
    'gen'               : u'Error dans la saisie!',
    'email'             : u'Error dans l\'envoi d\'e-mail!',
    'import'            : u'Error dans l\'import!',
    'no-data'           : u'Pas de données!',
    'duplicate'         : u'Doublon, vérifiez votre saisie!',
  },
  'auth' : {
    'title': u'Authentification',
    'submit': u'Se connecter',
    'chgpwd' : {
      'title': u'Changer le mot de passe pour: ',
      'submit': u'Changer',
      'done' : {
        'title': u'Changement du mot de passe réussi.',
        'message': u'Ton mot de passe a été changé avec succès. Merci de te reconnecter avec le nouveau mot de passe.',
        'backurl': '/',
        'backurl_txt': u'Retour vers l\'applicaion.',
      },
    },
  },
}
#add env badge
try:
  TEMPLATE_CONTENT['meta']['badge'] = APP_ENV
except:
  pass

# home
ACTIONS = (
  {
    'has_perms' 	: 'cms.MEMBER',
    'heading' 		: 'Association',
    'grade' 		: 'success',
    'icon' 		: 'users',
    'actions' : (
      {         
        'label'         : u'Réunions Statutaires', 
        'icon'     	: 'calendar',
        'desc'          : 'Outil de gestion des réunions statutaires.',
        'url'           : '/meetings/',
    	'has_perms' 	: 'cms.MEMBER',
      },
      {         
        'label'         : u'Membres', 
        'icon'     	: 'user',
        'desc'          : 'Gérer les members et leurs affiliations.',
        'url'           : '/members/',
    	'has_perms' 	: 'cms.MEMBER',
      },
      {         
        'label'         : u'Trésorerie', 
        'icon'     	: 'euro',
        'desc'          : 'Gérer les comptes et autres aspects financiers.',
        'url'           : '/finance/',
   	'has_perms' 	: 'cms.MEMBER',
     },

    ),
  },
  {
    'has_perms' 	: 'cms.MEMBER',
    'heading' 		: 'Activités',
    'grade' 		: 'info',
    'icon' 		: 'globe',
    'actions'   : (
      { 
        'label'         : 'Évènements', 
        'icon'     	: 'glass',
        'desc'          : 'Gérer les actvitiés et évènements (hors réunions statutaires).',
        'url'           : '/events/',
    	'has_perms' 	: 'cms.MEMBER',
      },
      { 
        'label'        	: u'Lieux de Rencontres', 
        'icon'     	: 'home',
        'desc'         	: u'Gérer (ajouter/modifier) les lieux de rencontre.', 
        'url'          	: '/locations/', 
        'has_perms'    	: 'cms.MEMBER',
      },
      {         
	'label'		: 'DISTRICT', 
	'icon'		: 'building',
	'desc'		: 'Redirection vers le site du DISTRICT 104.',
	'url'		: 'https://d104.fifty-one.club/',
	'has_perms'	: 'cms.MEMBER',
      },
    ),
  },
)

TEMPLATE_CONTENT['home'] = {
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
}

#setup
from setup.settings import *
TEMPLATE_CONTENT['setup'] = SETUP_TMPL_CONTENT

#members
from members.settings import *
TEMPLATE_CONTENT['members'] = MEMBERS_TMPL_CONTENT

#attendance
from attendance.settings import *
TEMPLATE_CONTENT['attendance'] = ATTENDANCE_TMPL_CONTENT
ATTENDANCE_BASE_URL = 'https://' + ALLOWED_HOSTS[0] + '/attendance/'

#locations
from locations.settings import *
TEMPLATE_CONTENT['locations'] = LOCATIONS_TMPL_CONTENT

#meetings
from meetings.settings import *
TEMPLATE_CONTENT['meetings'] = MEETINGS_TMPL_CONTENT
MEETINGS_ATTENDANCE_URL = ATTENDANCE_BASE_URL + 'meetings/'

#events
from events.settings import *
TEMPLATE_CONTENT['events'] = EVENTS_TMPL_CONTENT
EVENTS_ATTENDANCE_URL = ATTENDANCE_BASE_URL + 'events/'

#finance
from finance.settings import *
TEMPLATE_CONTENT['finance'] = FINANCE_TMPL_CONTENT

#upload
from upload.settings import *
TEMPLATE_CONTENT['upload'] = UPLOAD_TMPL_CONTENT

