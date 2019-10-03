# -*- coding: utf-8 -*-
import datetime
from django.test.testcases import TestCase
from ..models import News
from .factories import NewsFactory
from freezegun import freeze_time

today = datetime.date(2019, 3, 23)

@freeze_time(today)
class NewsManagerTestCase(TestCase):

    def setUp(self):
        # published
        self.active = NewsFactory.create_batch(3, title='active')
        self.active_and_published = NewsFactory.create_batch(3, title='active_and_published', start=datetime.date(2019, 3, 22), end=None)
        self.active_and_published_with_end = NewsFactory.create_batch(3, title='active_and_published_with_end', end=datetime.date(2019, 3, 23))
        self.active_and_published_start_is_today = NewsFactory.create_batch(3, title='active_and_published_start_is_today', start=datetime.date(2019, 3, 23), end=None)
        self.active_and_published_end_is_today = NewsFactory.create_batch(3, title='active_and_published_end_is_today', start=datetime.date(2019, 3, 22), end=datetime.date(2019, 3, 23))

        # not published
        self.inactive = NewsFactory.create_batch(2, title='inactive', status=News.INACTIVE)
        self.active_but_not_yet_published = NewsFactory.create_batch(2, title='active_but_not_yet_published', start=datetime.date(2019, 3, 24), end=datetime.date(2019, 3, 27))
        self.active_but_not_yet_published_no_end = NewsFactory.create_batch(2, title='active_but_not_yet_published_no_end', start=datetime.date(2019, 3, 24), end=None)
        self.active_but_outdated_no_start= NewsFactory.create_batch(2, title='active_but_outdated_no_start', start=datetime.date(2019, 3, 24), end=None)
        self.active_and_outdated = NewsFactory.create_batch(2, title='active_and_outdated', start=datetime.date(2019, 3, 21), end=datetime.date(2019, 3, 22))


    def test_active(self):
        all_active = self.active + self.active_and_published_with_end + self.active_and_published + self.active_and_published_start_is_today + self.active_and_published_end_is_today
        self.assertCountEqual(all_active, list(News.objects.active()))

    def test_published_fields_empty(self):
        expected_result =  self.active + self.inactive
        self.assertCountEqual(expected_result, list(News.objects.published_fields_empty()))

    def test_published_with_startdate_either_and_no_enddate(self):
        expected_result = self.active_and_published + self.active_and_published_start_is_today
        self.assertCountEqual(expected_result, list(News.objects.published_with_startdate(start=today)))

    def test_published_with_enddate_and_no_startdate(self):
        expected_result = self.active_and_published_with_end
        self.assertCountEqual(expected_result, list(News.objects.published_with_enddate(end=today)))
