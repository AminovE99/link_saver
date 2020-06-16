import ast
import json
import time
import unittest

import redis
from django.test import TestCase, Client

# Create your tests here.
from link_saver import settings
from visited_links.apps import VisitedLinksConfig
from visited_links.views import VisitedLinksRegisterView


class TestVisitedLinks(unittest.TestCase):
    def setUp(self):
        self.test_client = Client()
        self.request_1 = '''
        {
            "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
        '''
        self.request_2 = '''
                {
                    "links": [
                    "https://google.com",
                    "https://vk.com/news",
                    "aminovE99.github.io"
                    ]
                }
                '''
        self.request_empty = '''
                        {
                            "links": [
                            ],
                            "entity":[
                            "Another entity"
                            ]
                        }
                        '''
        self.request_1_json = json.loads(self.request_1)
        self.request_2_json = json.loads(self.request_2)
        self.request_empty = json.loads(self.request_empty)
        self.redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                                port=settings.REDIS_PORT, db=0, decode_responses=True)

    def tearDown(self):
        self.redis_instance.flushall()

    def test_VisitedLinksRegisterView_success(self):
        response = self.test_client.post('/visited_links', self.request_1_json, content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_VisitedLinksRegisterView_refuse_get(self):
        response = self.test_client.get('/visited_links', content_type="application/json")

        self.assertEqual(response.status_code, 405)

    def test_VisitedLinksRegisterView_check_db(self):
        self.test_client.post('/visited_links', self.request_1_json, content_type="application/json")
        links = self.redis_instance.zrange('links', 0, -1)[0]
        links_set = ast.literal_eval(links)

        self.assertIn('ya.ru', links_set)
        self.assertIn('funbox.ru', links_set)
        self.assertIn('stackoverflow.com', links_set)

    def test_VisitedLinksRegisterView_empty_links(self):
        response = self.test_client.post('/visited_links', self.request_empty, content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_GetLinksRegisterView_check_db(self):
        from_timestamp = int(time.time())
        self.test_client.post('/visited_links', self.request_1_json, content_type="application/json")
        self.test_client.post('/visited_links', self.request_2_json, content_type="application/json")
        to_timestamp = int(time.time())
        response = self.test_client.get('/visited_domains?from={}&to={}'.format(from_timestamp, to_timestamp))
        response_dict = response.json()

        self.assertTrue('aminovE99.github.io', response_dict['domains'])
        self.assertTrue('stackoverflow.com', response_dict['domains'])
        self.assertTrue('google.com', response_dict['domains'])
        self.assertTrue('funbox.ru', response_dict['domains'])
        self.assertTrue('ya.ru', response_dict['domains'])
        self.assertTrue('vk.com', response_dict['domains'])

    def test_GetLinksRegisterView_empty_list(self):
        self.test_client.post('/visited_links', self.request_1_json, content_type="application/json")
        response = self.test_client.get('/visited_domains?from={}&to={}'.format("10000", "20000"))
        response_dict = response.json()

        self.assertEqual(response_dict['domains'], [])

    def test_GetLinksRegisterView_invalid_from_timestamp(self):
        response = self.test_client.get('/visited_domains')
        self.assertEqual(response.json()['status'], "From timestamp not found")
        self.assertEqual(response.status_code, 422)

    def test_GetLinksRegisterView_invalid_to_timestamp(self):
        from_timestamp = int(time.time())
        response = self.test_client.get('/visited_domains?from={}'.format(from_timestamp))

        self.assertEqual(response.json()['status'], "To timestamp not found")
        self.assertEqual(response.status_code, 422)

    def test_GetLinksRegisterView_invalid_format(self):
        response = self.test_client.get('/visited_domains?from={}'.format("symbols"))

        self.assertEqual(response.json()['status'], "To timestamp not found")
        self.assertEqual(response.status_code, 422)
