import json
import random
import string
from uuid import uuid4

from django.test import Client, TestCase


class TestCampaignCreate(TestCase):
    def setUp(self):
        self.__client = Client()

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

    def test_with_empty_targeting_campaign_create(self):
        campaign_data = self.__generate_campaign_data()
        campaign_data["targeting"] = {
            "gender": None,
            "age_from": None,
            "age_to": None,
            "location": None
        }
        adv_data = self.__generate_adv_data()
        adv_id = adv_data["advertiser_id"]

        self.__client.post(
            "/advertisers/bulk",
            json.dumps([adv_data]),
            content_type="application/json"
        )

        response = self.__client.post(
            f"/advertisers/{adv_id}/campaigns",
            data=campaign_data,
            content_type="application/json"
        )
        resp_data = json.loads(response.content.decode())
        del resp_data["campaign_id"]
        campaign_data["advertiser_id"] = adv_id
        self.assertEqual(
            resp_data,
            campaign_data,
            "Response body (without campaign id) are noe same"
        )
        self.assertEqual(
            response.status_code,
            201,
            "Status code is not 201"
        )

    def test_incorrect_targeting_age_from_lower(self):
        campaign_data = self.__generate_campaign_data()
        campaign_data["targeting"] = {
            "gender": None,
            "age_from": 19,
            "age_to": 17,
            "location": None
        }
        adv_data = self.__generate_adv_data()
        adv_id = adv_data["advertiser_id"]

        self.__client.post(
            "/advertisers/bulk",
            json.dumps([adv_data]),
            content_type="application/json"
        )

        response = self.__client.post(
            f"/advertisers/{adv_id}/campaigns",
            data=campaign_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            400,
            "Status code is not 400"
        )

    def test_incorrect_gender(self):
        campaign_data = self.__generate_campaign_data()
        campaign_data["targeting"] = {
            "gender": "Attack helicopter"
        }
        adv_data = self.__generate_adv_data()
        adv_id = adv_data["advertiser_id"]

        self.__client.post(
            "/advertisers/bulk",
            json.dumps([adv_data]),
            content_type="application/json"
        )

        response = self.__client.post(
            f"/advertisers/{adv_id}/campaigns",
            data=campaign_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            400,
            "Status code is not 400"
        )

    def test_without_clicks_cost(self):
        campaign_data = self.__generate_campaign_data()
        del campaign_data["cost_per_click"]
        adv_data = self.__generate_adv_data()
        adv_id = adv_data["advertiser_id"]

        self.__client.post(
            "/advertisers/bulk",
            json.dumps([adv_data]),
            content_type="application/json"
        )

        response = self.__client.post(
            f"/advertisers/{adv_id}/campaigns",
            data=campaign_data,
            content_type="application/json"
        )
        self.assertEqual(
            response.status_code,
            400,
            "Status code is not 400"
        )

    def test_correct_campaign_create(self):
        campaign_data = self.__generate_campaign_data()
        adv_data = self.__generate_adv_data()
        adv_id = adv_data["advertiser_id"]

        self.__client.post(
            "/advertisers/bulk",
            json.dumps([adv_data]),
            content_type="application/json"
        )

        response = self.__client.post(
            f"/advertisers/{adv_id}/campaigns",
            data=campaign_data,
            content_type="application/json"
        )
        resp_data = json.loads(response.content.decode())
        # del resp_data["campaign_id"]
        campaign_data["advertiser_id"] = adv_id
        self.assertEqual(
            resp_data,
            campaign_data,
            "Response body (without campaign id) are noe same"
        )
        self.assertEqual(
            response.status_code,
            201,
            "Status code is not 201"
        )


class TestCampaignGet(TestCase):
    def setUp(self):
        self.__client = Client()

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

    def create_advertiser(self) -> str:
        adv_data = self.__generate_adv_data()
        self.__client.post(
            "/advertisers/bulk",
            json.dumps([adv_data]),
            content_type="application/json"
        )
        return adv_data["advertiser_id"]

    def create_campaign(self, adv_id: str) -> dict:
        campaign_data = self.__generate_campaign_data()
        response = self.__client.post(
            f"/advertisers/{adv_id}/campaigns",
            data=campaign_data,
            content_type="application/json"
        )
        data = json.loads(response.content.decode())
        return data

    def test_correct_get_adv(self):
        advertiser_id = self.create_advertiser()
        campaign = self.create_campaign(advertiser_id)
        campaign_id = campaign["campaign_id"]

        response = self.__client.get(
            f"/advertisers/{advertiser_id}/campaigns/{campaign_id}"
        )

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200"
        )
        self.assertEqual(
            json.loads(response.content.decode()),
            campaign,
            "Body is not valid"
        )

    def test_get_adv_by_invalid_id(self):
        advertiser_id = self.create_advertiser()
        response = self.__client.get(
            f"/advertisers/{advertiser_id}/campaigns/{str(uuid4())}"
        )

        self.assertEqual(
            response.status_code,
            404,
            "Status code is not 404"
        )

    def test_get_by_random_str(self):
        advertiser_id = self.create_advertiser()
        response = self.__client.get(
            f"/advertisers/{advertiser_id}/campaigns/123231"
        )

        self.assertEqual(
            response.status_code,
            400,
            "Status code is not 400"
        )
