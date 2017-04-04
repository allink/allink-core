# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _


####################################################################################

#  BLANK

BLANK_CHOICE = (('', '---------'),)

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
KUNUNU = 'kununu'

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
    (KUNUNU, _(u'kununu')),
)

####################################################################################

# BUTTON / TEXT

# Used in the 'Button / Link' plugin

SIZE_CHOICES = (
    ('sm', _('Small'),),
    ('md', _('Medium'),),
    ('lg', _('Large'),),
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

NEW_WINDOW = 1
SOFTPAGE_LARGE = 2
SOFTPAGE_SMALL = 3
FORM_MODAL = 4
IMAGE_MODAL = 5

TARGET_CHOICES = (
    (NEW_WINDOW, _(u'New window')),
    (SOFTPAGE_LARGE, _(u'Softpage large')),
    (SOFTPAGE_SMALL, _(u'Softpage small')),
    (FORM_MODAL, _(u'Lightbox (Forms)')),
    (IMAGE_MODAL, _(u'Lightbox (Image)')),
)

SPECIAL_LINKS_CHOICES = (
    ('account_login', _(u'Member Login')),
    ('account_logout', _(u'Member Logout')),
    ('account_change_password', _(u'Member Change Passwort')),
    ('account_reset_password', _(u'Member Reset Passwort')),
    ('members:profile_edit', _(u'Member Edit Profile')),
    # ('members:register', _(u'Member Register')),
    # ('members:password_reset_recover', _(u'Member Reset Passwort')),
    ('contact:request', _(u'Contact Form')),
)

####################################################################################

# IMAGE

RATIO_CHOICES = (
    ('3-2', '3:2'),
    ('2-1', '2:1'),
    ('4-3', '4:3'),
    ('1-1', '1:1'),
    ('16-9', '16:9'),
    ('x-y', 'Original'),
)
