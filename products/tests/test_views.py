from rest_framework.test import APITestCase

from user.models import User
from django.test import Client
from rest_framework.authtoken.models import Token
from products.models import Product


# Create your tests here.


class ViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

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

        seller = User.objects.create_user(
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

        cls.product = Product.objects.create(
            description="Smartband XYZ 3.0",
            price=100,
            quantity=10,
            seller=seller,
        )

    # def setUp(self) -> None:
    #     response = self.client.post("/api/login/", self.superuser)
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

    def test_only_seller_can_create_product(self):
        response = self.client.post(
            "/api/login/", {"email": "seller_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.post(
            "/api/products/",
            {"description": "Smartband XYZ 3.0", "price": 100.99, "quantity": 15},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data["seller"])

    def test_normal_user_can_not_create_product(self):
        response = self.client.post(
            "/api/login/", {"email": "user_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.post(
            "/api/products/",
            {"description": "Smartband XYZ 3.0", "price": 100.99, "quantity": 15},
        )

        self.assertEqual(response.status_code, 403)

    def test_only_product_owner_can_update(self):
        response = self.client.post(
            "/api/login/", {"email": "seller_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.patch(
            "/api/products/1/",
            {"description": "Smartband XYZ 99.0", "price": 100.99, "quantity": 15},
        )

        self.assertEqual(response.status_code, 200)

    def test_normal_user_can_not_update_product(self):
        response = self.client.post(
            "/api/login/", {"email": "user_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.patch(
            "/api/products/1/",
            {"description": "Smartband XYZ 99.0", "price": 100.99, "quantity": 15},
        )

        self.assertEqual(response.status_code, 403)

    def test_list_all_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)

    def test_specific_product_list(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["description"], "Smartband XYZ 3.0")
        self.assertEqual(response.data[0]["price"], "100.00")
        self.assertEqual(response.data[0]["quantity"], 10)

    def test_specific_product_create(self):
        response = self.client.post(
            "/api/login/", {"email": "seller_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.post(
            "/api/products/",
            {"description": "Smartband XYZ 22.0", "price": 69, "quantity": 69},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data["seller"])
        self.assertEqual(response.data["description"], "Smartband XYZ 22.0")
        self.assertEqual(response.data["price"], "69.00")
        self.assertEqual(response.data["quantity"], 69)

    def test_missing_keys(self):
        response = self.client.post(
            "/api/login/", {"email": "seller_teste@teste.com", "password": "password"}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

        response = self.client.post(
            "/api/products/",
            {},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["description"][0][0:], "This field is required.")
        self.assertEqual(response.data["price"][0][0:], "This field is required.")
        self.assertEqual(response.data["quantity"][0][0:], "This field is required.")
