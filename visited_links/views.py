import json
import time

import redis
from django.http import JsonResponse

from rest_framework.views import APIView

from link_saver import settings
from visited_links.redis_services import save_link_visits, get_links_from
from visited_links.utils import handle_links


class VisitedLinksRegisterView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                                port=settings.REDIS_PORT, decode_responses=True)

    def post(self, request):
        current_timestamp = int(time.time())

        # Get parameters from request
        links = request.data.get('links')
        if not links:
            return JsonResponse(data={'status': "Links not found"}, status=422)

        # Filter links from garbage and leave only domains
        handled_links = handle_links(links)
        save_link_visits(self.redis_instance, handled_links, current_timestamp)
        return JsonResponse(data={'status': 'ok'}, status=200)


class GetLinksRegisterView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                                port=settings.REDIS_PORT, decode_responses=True)

    def get(self, request):
        # Get parameters from request
        from_timestamp = request.GET.get('from')
        to_timestamp = request.GET.get('to')

        # Validate timestamp values
        if from_timestamp is None:
            return JsonResponse(data={'status': "From timestamp not found"}, status=422)
        if to_timestamp is None:
            return JsonResponse(data={'status': "To timestamp not found"}, status=422)
        if not to_timestamp.isdigit() or not from_timestamp.isdigit():
            return JsonResponse(data={'status': "Timestamp Validation error"}, status=422)

        # Get links from redis service
        links = get_links_from(self.redis_instance, from_timestamp, to_timestamp)
        return JsonResponse(data={'domains': list(links), 'status': 'ok'})
