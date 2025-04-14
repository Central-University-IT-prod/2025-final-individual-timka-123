import json
import random
import string
from uuid import uuid4

from django.test import Client, TestCase


class TestMlScores(TestCase):
    def setUp(self):
        self.client = Client()

    def __generate_adv_data(self):
        return {
            "advertiser_id": str(uuid4()),
            "name": ''.join(
                random.choice(
                    string.ascii_uppercase + string.digits
                ) for _ in range(7)
            )
        }

    def __generate_campaign_data(self):
        return {
            "impressions_limit": 10000,
            "clicks_limit": 10000,
            "cost_per_impression": 10,
            "cost_per_click": 40,
            "ad_title": "Гараж",
            "ad_text": "Продам гараж, недорого",
            "start_date": 1,
            "end_date": 100,
            "targeting": {
                "gender": "MALE",
                "age_from": 17,
                "age_to": 19,
                "location": "Метро Белорусская"
            }
        }

    def __generate_user_data(self) -> dict:
        return {
            "client_id": str(uuid4()),
            "login": ''.join(
                random.choice(
                    string.ascii_uppercase + string.digits
                ) for _ in range(7)
            ),
            "gender": "MALE",
            "age": 17,
            "location": "Kazan"
        }

    def create_client(self) -> str:
        user_data = self.__generate_user_data()
        self.client.post(
            "/clients/bulk",
            json.dumps([user_data]),
            content_type="application/json"
        )
        return user_data["client_id"]

    def create_advertiser(self) -> str:
        adv_data = self.__generate_adv_data()
        self.client.post(
            "/advertisers/bulk",
            json.dumps([adv_data]),
            content_type="application/json"
        )
        return adv_data["advertiser_id"]

    def test_correct_ml_score_set(self):
        advertiser_id = self.create_advertiser()
        client_id = self.create_client()

        response = self.client.post(
            "/ml-scores",
            data={
                "client_id": client_id,
                "advertiser_id": advertiser_id,
                "score": 100500
            },
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200"
        )

    def test_correct_ml_score_twice_set(self):
        advertiser_id = self.create_advertiser()
        client_id = self.create_client()

        for i in range(2):
            response = self.client.post(
                "/ml-scores",
                data={
                    "client_id": client_id,
                    "advertiser_id": advertiser_id,
                    "score": 100500
                },
                content_type="application/json"
            )

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200"
        )
