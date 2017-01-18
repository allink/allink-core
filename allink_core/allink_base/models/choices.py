# -*- coding: utf-8 -*-
from functools import partial
import datetime
from django.utils.translation import ugettext_lazy as _

####################################################################################

# YEARS (past and near future)

YEAR_CHOICES = [(r, r) for r in list(reversed(range(1930, datetime.date.today().year + 5)))]


####################################################################################

#  GENDER

MALE = 1
FEMALE = 2

GENDER_CHOICES = {
    (MALE, _(u'Male')),
    (FEMALE, _(u'Female'))
}


####################################################################################

# POSITIONING

LEFT = 'left'
CENTER = 'center'
RIGHT = 'right'

HORIZONTAL_ALIGNMENT_CHOICES = (
    (LEFT, _(u'Left')),
    (CENTER, _(u'Center')),
    (RIGHT, _(u'Right')),
)

TOP = 'top'
MIDDLE = 'middle'
BOTTOM = 'bottom'

VERTICAL_ALIGNMENT_CHOICES = (
    (TOP, _(u'Top')),
    (MIDDLE, _(u'Middle')),
    (BOTTOM, _(u'Bottom')),
)


####################################################################################

# TYPOGRAPHY

# Used for section headings for our 'Content Plugin' and 'App Content Plugin'

H1 = 'h1'
H2 = 'h2'

TITLE_CHOICES = (
    (H1, _(u'Title Large')),
    (H2, _(u'Title Medium')),
)


####################################################################################

# SOCIAL ICONS

# Used in the 'Social Icon' plugin

# Important: These keys have to match the map defined in the CSS variables

FACEBOOK = 'facebook'
INSTAGRAMM = 'instagram'
PINTEREST = 'pinterest'
TWITTER = 'twitter'
SNAPCHAT = 'snapchat'
SPOTIFY = 'spotify'
LINKEDIN = 'linkedin'
XING = 'xing'
YOUTUBE = 'youtube'
VIMEO = 'vimeo'
GOOGLEPLUS = 'googleplus'
TRIPADVISOR = 'tripadvisor'

SOCIAL_ICONS_CHOICES = (
    (FACEBOOK, _(u'Facebook')),
    (INSTAGRAMM, _(u'Instagram')),
    (PINTEREST, _(u'Pinterest')),
    (TWITTER, _(u'Twitter')),
    (SNAPCHAT, _(u'Snapchat')),
    (LINKEDIN, _(u'Linkedin')),
    (SPOTIFY, _(u'Spotify')),
    (XING, _(u'Xing')),
    (YOUTUBE, _(u'Youtube')),
    (VIMEO, _(u'Vimeo')),
    (GOOGLEPLUS, _(u'Google Plus')),
    (TRIPADVISOR, _(u'TripAdvisor')),
)

####################################################################################

# Button/ Text

# Used in the 'Button / Link' plugin

SIZE_CHOICES = (
    ('lg', _('Large'),),
    ('md', _('Medium'),),
    ('sm', _('Small'),),
)

CONTEXT_CHOICES = (
    ('primary', 'Primary',),
    ('success', 'Success',),
    ('info', 'Info',),
    ('warning', 'Warning',),
    ('danger', 'Danger',),
)

CONTEXT_DEFAULT = 'default'

BUTTON_CONTEXT_CHOICES = (
    ('default', 'Default',),
) + CONTEXT_CHOICES + (
    ('link', 'Link',),
)

BUTTON_CONTEXT_DEFAULT = 'default'

TEXT_LINK_CONTEXT_CHOICES = (
    ('', 'Default',),
) + CONTEXT_CHOICES + (
    ('muted ', 'Muted',),
)

TEXT_LINK_CONTEXT_DEFAULT = ''
