# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

####################################################################################

#  BLANK

BLANK_CHOICE = (('', '---------'),)


####################################################################################

#  SALUTATION

MR = 1
MRS = 2

SALUTATION_CHOICES = (
    (MR, _(u'Mr.')),
    (MRS, _(u'Mrs.')),
)

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

# H1 = 'h1'
# H2 = 'h2'
# H3 = 'h3'
#
# TITLE_CHOICES = (
#     (H1, _(u'Title Large')),
#     (H2, _(u'Title Medium')),
#     (H3, _(u'Title Small')),
# )


####################################################################################

# VIDEO SERVICES
YOUTUBE = 'youtube'
VIMEO = 'vimeo'

VIDEO_SERVICE_CHOICES = (
    (YOUTUBE, u'Youtube'),
    (VIMEO, u'Vimeo'),
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
    (SOFTPAGE_LARGE, _(u'Softpage (large)')),
    (SOFTPAGE_SMALL, _(u'Softpage (small)')),
    (FORM_MODAL, _(u'Lightbox (Forms)')),
    (IMAGE_MODAL, _(u'Lightbox (Image)')),
)

####################################################################################

# IMAGE

RATIO_CHOICES = (
    ('3-2', '3:2'),
    ('2-1', '2:1'),
    ('4-3', '4:3'),
    ('1-1', '1:1'),
    ('16-9', '16:9'),
)
RATIO_CHOICES_ORIG = RATIO_CHOICES + (('x-y', 'Original'),)
