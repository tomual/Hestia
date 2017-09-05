from datetime import datetime

from forums.models import Thread, Response
from django.contrib.auth.models import User

class RecentResponsesMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        request.recent_responses = Response.objects.order_by('-response_date')[:5]

        response = self.get_response(request)
        return response