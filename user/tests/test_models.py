from django.test import TestCase

from user.models import User

# Create your tests here.

class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        print(cls)
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

    def test_names_length(self):
        user = User.objects.get(id=1)
        first_name_length = user._meta.get_field('first_name').max_length
        last_name_length = user._meta.get_field('last_name').max_length
        
        self.assertEquals(first_name_length,50)
        self.assertEquals(last_name_length,50)

    def test_correct_names(self):
        user = User.objects.get(id=1)
        self.assertEquals(user.first_name,self.first_name)
        self.assertEquals(user.last_name,self.last_name)

    def test_not_null_fields(self):
        user = User.objects.get(id=1)
        
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.is_seller)