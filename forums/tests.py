import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Thread

def create_thread(title, message, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Thread.objects.create(title=title, message=message, posted=time)

class ThreadModelTests(TestCase):
    # No threads
    def test_no_questions(self):
        response = self.client.get('/forums/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No threads")
        self.assertQuerysetEqual(response.context['latest_thread_list'], [])

    # Future thread
    def test_was_posted_recently_with_future_thread(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_thread = Thread(posted=time)
        self.assertIs(future_thread.was_posted_recently(), False)

    # Old thread
    def test_was_posted_recently_with_old_thread(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_thread = Thread(posted=time)
        self.assertIs(old_thread.was_posted_recently(), False)

    # Recent thread
    def test_was_posted_recently_with_recent_thread(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_thread = Thread(posted=time)
        self.assertIs(recent_thread.was_posted_recently(), True)

class ThreadDetailViewTests(TestCase):