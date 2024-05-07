from django.test import TestCase
from django.utils import timezone

from dishes.models import Category, Dish


class TestCategory(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name='test category', slug='test-category', position=8)
        cls.category2 = Category.objects.create(name='category', slug='category', position=5)

    def test_category_name(self):
        self.assertEquals(self.category1.__str__(), 'test category')
        self.assertEquals(self.category2.__str__(), 'category')


class TestDishes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='test category', slug='test-category', position=8)
        cls.dish1 = Dish.objects.create(name="test dish", slug="test-dish", description="some description", kitchen_type="Thai",
                                        composition="some composition", weight=200, caloric=190,
                                        image="", price=23, discount=0, spice=0, category=cls.category, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish2 = Dish.objects.create(name="season dish", slug="season-dish", description="some description",
                                        kitchen_type="Chinese", composition="some composition", weight=300, caloric=300,
                                        image="", price=19, discount=0, spice=1, category=cls.category, is_season=True,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish3 = Dish.objects.create(name="discount dish", slug="discount-dish", description="some description",
                                        kitchen_type="Thai", composition="some composition", weight=300, caloric=300,
                                        image="", price=19, discount=25, spice=3, category=cls.category, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())

    def test_dish_name(self):
        dish = Dish.objects.get(name="test dish")
        self.assertEquals(dish.__str__(), "test dish")

    def test_season_dish(self):
        dish = Dish.objects.filter(is_season=True)
        self.assertEquals(dish.count(), 1)

    def test_dish_price(self):
        dishes = Dish.objects.filter(discount=0)
        for item in dishes:
            self.assertEquals(item.get_price(), item.price)

    def test_dish_discount_price(self):
        dishes = Dish.objects.filter(discount__gt=0)
        for item in dishes:
            self.assertEquals(item.get_price(), item.price - item.price * item.discount / 100)

    def test_relationship(self):
        dishes_by_category_count = self.category.dishes.count()
        self.assertEquals(dishes_by_category_count, 3)
