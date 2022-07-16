from rest_framework.test import APITestCase

from user.models import User
from django.test import Client
from rest_framework.authtoken.models import Token

# Create your tests here.


class ViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.seller = {
            "email": "teste222@teste.com",
            "password": "1234",
            "is_seller": True,
            "first_name": "Teste",
            "last_name": "Outro Teste",
        }
        cls.normal_user = {
            "email": "teste222@teste.com",
            "password": "1234",
            "is_seller": False,
            "first_name": "Teste",
            "last_name": "Outro Teste",
        }

        cls.superuser = {
            "email": "admin@teste.com",
            "password": "1234",
        }

        User.objects.create_user(
            email="user_teste@teste.com",
            password="password",
            first_name="Teste",
            last_name="Teste",
        )

        User.objects.create_user(
            email="seller_teste@teste.com",
            password="password",
            first_name="Teste",
            last_name="Teste",
            is_seller=True,
        )

        User.objects.create_superuser(
            email="admin@teste.com",
            password="1234",
            first_name="Teste",
            last_name="Teste",
        )

    def setUp(self) -> None:
        response = self.client.post("/api/login/", self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

    def test_user_seller_create(self):
        response = self.client.post("/api/accounts/", self.seller)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], self.seller["email"])
        self.assertEqual(response.data["is_seller"], self.seller["is_seller"])
        self.assertEqual(response.data["first_name"], self.seller["first_name"])
        self.assertEqual(response.data["last_name"], self.seller["last_name"])
        self.assertIsNotNone(response.data["id"])

    def test_normal_user_create(self):
        response = self.client.post("/api/accounts/", self.normal_user)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], self.normal_user["email"])
        self.assertEqual(response.data["is_seller"], self.normal_user["is_seller"])
        self.assertEqual(response.data["first_name"], self.normal_user["first_name"])
        self.assertEqual(response.data["last_name"], self.normal_user["last_name"])
        self.assertIsNotNone(response.data["id"])

    def test_wrong_keys(self):
        response = self.client.post("/api/accounts/", {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0][0:], "This field is required.")
        self.assertEqual(response.data["first_name"][0][0:], "This field is required.")
        self.assertEqual(response.data["last_name"][0][0:], "This field is required.")

    def test_user_token_login_return(self):
        response = self.client.post(
            "/api/login/", {"email": "user_teste@teste.com", "password": "password"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["token"])

    def test_seller_token_login_return(self):
        response = self.client.post(
            "/api/login/", {"email": "seller_teste@teste.com", "password": "password"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["token"])

    def test_seller_token_login_return_nothing(self):
        response = self.client.post(
            "/api/login/", {"email": "seller_teste@teste.com", "password": "password1"}
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "invalid username or password")

    def test_only_admin_can_activate_accounts(self):
        response = self.client.patch("/api/accounts/2/management/", {"is_active": True})

        self.assertEqual(response.status_code, 200)

    def test_only_admin_can_deactivate_accounts(self):
        response = self.client.post(
            "/api/login/", {"email": "user_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.patch(
            "/api/accounts/2/management/", {"is_active": False}
        )

        self.assertEqual(response.status_code, 403)

    def test_account_is_owner_to_update(self):
        response = self.client.post(
            "/api/login/", {"email": "user_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.patch("/api/accounts/2/", {"first_name": "teste"})

        self.assertEqual(response.status_code, 403)

    def test_list_users(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, 200)
