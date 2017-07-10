# -*- coding: utf-8 -*-
from allink_core.apps.testimonials.abstract_models import BaseTestimonials, BaseTestimonialsTranslation, BaseTestimonialsPlugin
from allink_core.core.loading import get_model
from allink_core.core.loading import is_model_registered

__all__ = []


if not is_model_registered('testimonials', 'Testimonials'):
    class Testimonials(BaseTestimonials):
        pass

    __all__.append('Testimonials')


if not is_model_registered('testimonials', 'TestimonialsTranslation'):
    class TestimonialsTranslation(BaseTestimonialsTranslation):
        pass

    __all__.append('TestimonialsTranslation')


if not is_model_registered('testimonials', 'TestimonialsAppContentPlugin'):
    class TestimonialsAppContentPlugin(BaseTestimonialsPlugin):
        data_model = get_model('testimonials', 'Testimonials')

    __all__.append('TestimonialsAppContentPlugin')
