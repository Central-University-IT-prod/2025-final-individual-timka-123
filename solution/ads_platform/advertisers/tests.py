import json
import random
import string
from uuid import uuid4

from django.test import Client, TestCase


class TestAdvertiserBulActions(TestCase):
    def __generate_adv_data(self):
        return {
            "advertiser_id": str(uuid4()),
            "name": ''.join(
                random.choice(
                    string.ascii_uppercase + string.digits
                ) for _ in range(7)
            )
        }

    def setUp(self):
        self.__client = Client()

    def __reg_request(self, data: list):
        return self.__client.post(
            path="/advertisers/bulk",
            data=json.dumps(data),
            content_type="application/json"
        )

    def __get_advertiser_request(self, adv_id: str):
        return self.__client.get(
            path=f"/advertisers/{adv_id}"
        )

    def test_correct_reg_one_company(self):
        data = self.__generate_adv_data()
        response = self.__reg_request([data])
        self.assertEqual(
            response.status_code,
            201,
            "Status code is not 201"
        )
        self.assertEqual(
            json.loads(response.content.decode()),
            [data],
            "Body is not correct"
        )

    def test_reg_with_invalid_id(self):
        data = self.__generate_adv_data()
        data["advertiser_id"] = "123"
        response = self.__reg_request([data])
        self.assertEqual(
            response.status_code,
            400,
            "Status code is not 400"
        )

    def test_correct_reg_of_multiply_advertisers(self):
        data = self.__generate_adv_data()
        data2 = self.__generate_adv_data()
        response = self.__reg_request([data, data2])
        self.assertEqual(
            response.status_code,
            201,
            "Status code is not 201"
        )
        self.assertEqual(
            json.loads(response.content.decode()),
            [data, data2],
            "Body is not correct"
        )

    def test_correct_edit_company(self):
        data = self.__generate_adv_data()
        response = self.__reg_request([data])
        # test correct reg
        self.assertEqual(
            response.status_code,
            201,
            "Status code is not 201"
        )
        self.assertEqual(
            json.loads(response.content.decode()),
            [data],
            "Body is not correct"
        )

        # test editing
        data["name"] = "NeTinkoff"
        response = self.__reg_request([data])
        self.assertEqual(
            response.status_code,
            201,
            "Status code is not 201"
        )
        resp_data = json.loads(response.content.decode())
        self.assertEqual(
            resp_data[0]["name"],
            data["name"],
            "Name has not been changed"
        )

    def test_correct_editing_company_info(self):
        data = self.__generate_adv_data()
        self.__reg_request([data])

        fetched_advertiser_info = json.loads(
            self.__get_advertiser_request(
                adv_id=data["advertiser_id"]
            ).content.decode()
        )
        self.assertEqual(
            data["name"],
            fetched_advertiser_info["name"],
            "Names in initial state are not equal..."
        )

        # test with editing
        data["name"] = "NeTinkoff"
        self.__reg_request([data])
        fetched_advertiser_info = json.loads(
            self.__get_advertiser_request(
                adv_id=data["advertiser_id"]
            ).content.decode()
        )
        self.assertEqual(
            "NeTinkoff",
            fetched_advertiser_info["name"],
            "Names has not beed changed"
        )
