from django.test import TestCase

from products.models import Product
from user.models import User

# Create your tests here.

class ProductsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.first_name = "Nícollas"
        cls.last_name = "Anderson"
        cls.email = 'teste@teste.com'
        cls.password = '1234'
        cls.is_seller = True

        cls.user = User.objects.create(
            first_name=cls.first_name,
            last_name=cls.last_name,
            email=cls.email,
            password=cls.password,
            is_seller=cls.is_seller
        )

        cls.description = "Uma descrição muito boa aqui."
        cls.price = 10
        cls.quantity = 5
        cls.seller = cls.user

        cls.product = Product.objects.create(
            description=cls.description,
            price=cls.price,
            quantity=cls.quantity,
            seller=cls.user,
        )
    def test_product_owner(self):
        user = User.objects.get(id=1)

        product = Product.objects.get(id=1)
        
        self.assertEquals(product.seller,user)

    def test_correct_names(self):
        ...

    def test_not_null_fields(self):
        product = Product.objects.get(id=1)

        self.assertIsNotNone(product.description)
        self.assertIsNotNone(product.price)
        self.assertIsNotNone(product.quantity)
        self.assertIsNotNone(product.seller)
