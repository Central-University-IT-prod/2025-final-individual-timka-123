import json
import string
import random
from uuid import uuid4

from django.test import Client, TestCase


class TestClientsApi(TestCase):
    def setUp(self):
        self.__client = Client()

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

    def test_correct_user_reg(self):
        user_data = self.__generate_user_data()
        response = self.__client.post(
            path="/clients/bulk",
            data=json.dumps([user_data]),
            content_type='application/json'
        )

        self.assertEqual(
            first=response.status_code,
            second=201,
            msg="Status code is not 201"
        )
        self.assertEqual(
            first=json.loads(response.content.decode(encoding="utf-8")),
            second=[user_data],
            msg="Response body is not equal with initial"
        )

    def test_user_reg_with_invalid_id(self):
        user_data = self.__generate_user_data()
        user_data["client_id"] = "123"
        response = self.__client.post(
            path="/clients/bulk",
            data=json.dumps([user_data]),
            content_type='application/json'
        )

        self.assertEqual(
            first=response.status_code,
            second=400,
            msg="Status code is not 400"
        )

    def test_correct_user_multiply(self):
        user_data = self.__generate_user_data()
        user_data2 = self.__generate_user_data()
        response = self.__client.post(
            path="/clients/bulk",
            data=json.dumps([user_data, user_data2]),
            content_type='application/json'
        )

        self.assertEqual(
            first=response.status_code,
            second=201,
            msg="Status code is not 201"
        )
        self.assertEqual(
            first=json.loads(response.content.decode(encoding="utf-8")),
            second=[user_data, user_data2],
            msg="Response body is not equal with initial"
        )

    def test_correct_user_edit(self):
        user_data = self.__generate_user_data()

        # register user
        response = self.__client.post(
            path="/clients/bulk",
            data=json.dumps([user_data]),
            content_type='application/json'
        )
        self.assertEqual(
            first=response.status_code,
            second=201,
            msg="Status code is not 201"
        )
        self.assertEqual(
            first=json.loads(response.content.decode(encoding="utf-8")),
            second=[user_data],
            msg="Response body is not equal with initial"
        )

        # edit user data
        user_data['location'] = "Moscow"
        response = self.__client.post(
            path="/clients/bulk",
            data=json.dumps([user_data]),
            content_type='application/json'
        )
        self.assertEqual(
            first=response.status_code,
            second=201,
            msg="Status code is not 201"
        )
        self.assertEqual(
            first=json.loads(response.content.decode(encoding="utf-8")),
            second=[user_data],
            msg="Response body is not equal with initial"
        )

    def test_user_getinfo(self):
        # register user
        user_data = self.__generate_user_data()
        response = self.__client.post(
            path="/clients/bulk",
            data=json.dumps([user_data]),
            content_type='application/json'
        )
        self.assertEqual(
            first=response.status_code,
            second=201,
            msg="Status code is not 201"
        )
        self.assertEqual(
            first=json.loads(response.content.decode(encoding="utf-8")),
            second=[user_data],
            msg="Response body is not equal with initial"
        )

        # get user
        response = self.__client.get(
            path=f"/clients/{user_data.get("client_id")}"
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
            msg="Status code is not 200"
        )
        self.assertEqual(
            first=json.loads(response.content.decode(encoding="utf-8")),
            second=user_data,
            msg="Response body is not equal with generated"
        )

    def test_get_invalid_user(self):
        random_id = str(uuid4())
        response = self.__client.get(
            path=f"/clients/{random_id}"
        )
        self.assertEqual(
            first=response.status_code,
            second=404,
            msg="Status code is not 404"
        )
