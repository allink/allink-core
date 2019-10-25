# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from allink_core.core.utils import get_additional_choices

####################################################################################

#  BLANK

BLANK_CHOICE = (('', '---------'),)


####################################################################################

#  SALUTATION

MR = 1
MRS = 2

SALUTATION_CHOICES = (
    (MR, _('Mr.')),
    (MRS, _('Mrs.')),
)

####################################################################################

# POSITIONING

LEFT = 'left'
CENTER = 'center'
RIGHT = 'right'

HORIZONTAL_ALIGNMENT_CHOICES = (
    (LEFT, 'Left'),
    (CENTER, 'Center'),
    (RIGHT, 'Right'),
)

TOP = 'top'
MIDDLE = 'middle'
BOTTOM = 'bottom'

VERTICAL_ALIGNMENT_CHOICES = (
    (TOP, 'Top'),
    (MIDDLE, 'Middle'),
    (BOTTOM, 'Bottom'),
)


####################################################################################

# TYPOGRAPHY

# Used for section headings for our 'Content Plugin' and 'App Content Plugin'

# H1 = 'h1'
# H2 = 'h2'
# H3 = 'h3'
#
# TITLE_CHOICES = (
#     (H1, _('Title Large')),
#     (H2, _('Title Medium')),
#     (H3, _('Title Small')),
# )


####################################################################################

# VIDEO SERVICES
YOUTUBE = 'youtube'
VIMEO = 'vimeo'

VIDEO_SERVICE_CHOICES = (
    (YOUTUBE, 'Youtube'),
    (VIMEO, 'Vimeo'),
)


####################################################################################

# BUTTON / TEXT

# Used in the 'Button / Link' plugin

SIZE_CHOICES = (
    ('sm', 'Small'),
    ('md', 'Medium'),
    ('lg', 'Large'),
)

CONTEXT_CHOICES = get_additional_choices('BUTTON_CONTEXT_CHOICES')

CONTEXT_DEFAULT = 'default'

BUTTON_CONTEXT_CHOICES = (
    (CONTEXT_DEFAULT, 'Default',),
) + CONTEXT_CHOICES

BUTTON_CONTEXT_DEFAULT = 'default'

TEXT_LINK_CONTEXT_CHOICES = (
    ('', 'Default',),
) + CONTEXT_CHOICES + (
    ('muted ', 'Muted',),
)

TEXT_LINK_CONTEXT_DEFAULT = ''

NEW_WINDOW = 1
SOFTPAGE = 2
FORM_MODAL = 4
IMAGE_MODAL = 5
DEFAULT_MODAL = 6

TARGET_CHOICES = (
    (NEW_WINDOW, 'New window'),
    (SOFTPAGE, 'Softpage'),
    (FORM_MODAL, 'Lightbox (Forms)'),
    (IMAGE_MODAL, 'Lightbox (Image)'),
    (DEFAULT_MODAL, 'Lightbox (Default)'),
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

IMAGE_WIDTH_ALIAS_CHOICES = ()
