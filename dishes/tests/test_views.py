import datetime

from django.test import TestCase
from parameterized import parameterized
from django.utils import timezone
from dishes.models import Dish, Category


class TestMenuView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.all = Category.objects.create(name='all', slug='all', position=1)
        cls.meat_and_poultry = Category.objects.create(name='meat and poultry', slug='meat-and-poultry', position=2)
        cls.fish_and_seafood = Category.objects.create(name='fish and seafood', slug='fish-and-seafood', position=3)
        cls.rice_and_noodles = Category.objects.create(name='rice and noodles', slug='rice-and-noodles', position=4)
        cls.soups = Category.objects.create(name='soups', slug='soups', position=5)
        cls.starters_and_salads = Category.objects.create(name='starters and salads', slug='starters-and-salads',
                                                          position=6)
        cls.vegetables_and_tofu = Category.objects.create(name='vegetables and tofu', slug='vegetables-and-tofu',
                                                          position=7)
        cls.desserts = Category.objects.create(name='desserts', slug='desserts', position=8)
        cls.drinks = Category.objects.create(name='drinks', slug='drinks', position=9)

        cls.dish1 = Dish.objects.create(name="test dish1", slug="test-dish1", description="some description",
                                        kitchen_type="Thai", composition="some composition", weight=200, caloric=190,
                                        image="media/dish_images/dish_1.jpg", price=13, discount=0, spice=0,
                                        category=cls.meat_and_poultry, is_season=True,
                                        start_period=datetime.date(2024, 4, 30), end_period=datetime.date(2024, 5, 30))
        cls.dish2 = Dish.objects.create(name="test dish2", slug="test-dish2", description="some description",
                                        kitchen_type="Japanese", composition="some composition", weight=200,
                                        caloric=190, image="media/dish_images/dish_1.jpg", price=20, discount=0, spice=1,
                                        category=cls.fish_and_seafood, is_season=False, start_period=timezone.now().date(),
                                        end_period=timezone.now().date())
        cls.dish3 = Dish.objects.create(name="test dish3", slug="test-dish3", description="some description",
                                        kitchen_type="Chinese", composition="some composition", weight=200, caloric=190,
                                        image="media/dish_images/dish_1.jpg", price=15, discount=25, spice=0,
                                        category=cls.rice_and_noodles, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish4 = Dish.objects.create(name="test dish4", slug="test-dish4", description="some description",
                                        kitchen_type="Thai", composition="some composition", weight=200, caloric=190,
                                        image="media/dish_images/dish_1.jpg", price=29, discount=0, spice=2,
                                        category=cls.soups, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish5 = Dish.objects.create(name="test dish5", slug="test-dish5", description="some description",
                                        kitchen_type="Korean", composition="some composition", weight=200, caloric=190,
                                        image="media/dish_images/dish_1.jpg", price=23,
                                        discount=0, spice=0, category=cls.starters_and_salads, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish6 = Dish.objects.create(name="test dish6", slug="test-dish6", description="some description",
                                        kitchen_type="Thai", composition="some composition", weight=200, caloric=190,
                                        image="media/dish_images/dish_1.jpg", price=10, discount=10, spice=1,
                                        category=cls.vegetables_and_tofu, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish7 = Dish.objects.create(name="test dish7", slug="test-dish7", description="some description",
                                        kitchen_type="Chinese", composition="some composition", weight=200, caloric=190,
                                        image="media/dish_images/dish_1.jpg", price=25, discount=0, spice=3,
                                        category=cls.desserts, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish8 = Dish.objects.create(name="test dish8", slug="test-dish8", description="some description",
                                        kitchen_type="Chinese", composition="some composition", weight=200, caloric=190,
                                        image="media/dish_images/dish_1.jpg", price=15, discount=30, spice=2,
                                        category=cls.drinks, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish9 = Dish.objects.create(name="test dish9", slug="test-dish9", description="some description",
                                        kitchen_type="Japanese", composition="some composition", weight=200,
                                        caloric=190, image="media/dish_images/dish_1.jpg", price=18, discount=0, spice=0,
                                        category=cls.meat_and_poultry, is_season=False,
                                        start_period=timezone.now().date(), end_period=timezone.now().date())
        cls.dish10 = Dish.objects.create(name="test dish10", slug="test-dish10", description="some description",
                                         kitchen_type="Korean", composition="some composition", weight=200,
                                         caloric=190, image="media/dish_images/dish_1.jpg", price=30, discount=0,
                                         spice=3, category=cls.meat_and_poultry, is_season=True,
                                         start_period=datetime.date(2024, 7, 23),
                                         end_period=datetime.date(2024, 8, 29))

    @parameterized.expand([
        ('all', 200),
        ('meat-and-poultry', 200),
        ('fish-and-seafood', 200),
        ('rice-and-noodles', 200),
        ('soups', 200),
        ('starters-and-salads', 200),
        ('vegetables-and-tofu', 200),
        ('desserts', 200),
        ('drinks', 200)
    ])
    def test_menu(self, category_slug, status_code):
        base_dir = '/menu/'
        response = self.client.get(base_dir + category_slug + '/')
        category = Category.objects.get(slug=category_slug)
        dishes = Dish.objects.exclude(name='test dish10')
        if category_slug != 'all':
            dishes = dishes.filter(category=category)
        self.assertEquals(response.status_code, status_code)
        self.assertQuerySetEqual(response.context['dishes'], dishes)

    @parameterized.expand([
        ('/menu/meat-and-poultry/test-dish1/', 'test dish1', 200),
        ('/menu/fish-and-seafood/test-dish2/', 'test dish2', 200),
        ('/menu/rice-and-noodles/test-dish3/', 'test dish3', 200),
        ('/menu/soups/test-dish4/', 'test dish4', 200),
        ('/menu/starters-and-salads/test-dish5/', 'test dish5', 200),
        ('/menu/vegetables-and-tofu/test-dish6/', 'test dish6', 200),
        ('/menu/desserts/test-dish7/', 'test dish7', 200),
        ('/menu/drinks/test-dish8/', 'test dish8', 200),
        ('/menu/meat-and-poultry/test-dish9/', 'test dish9', 200),
    ])
    def test_dish(self, url, dish_name, status_code):
        dish = Dish.objects.get(name=dish_name)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status_code)
        self.assertIn(dish.name, response.context['dish'].name)
        self.assertEquals(dish.price, response.context['dish'].price)
        self.assertIn(dish.description, response.context['dish'].description)
        self.assertIn(dish.kitchen_type, response.context['dish'].kitchen_type)
        self.assertEquals(dish.weight, response.context['dish'].weight)
        self.assertEquals(dish.caloric, response.context['dish'].caloric)
        self.assertIn(dish.composition, response.context['dish'].composition)
        self.assertEquals(dish.spice, response.context['dish'].spice)

    def test_price_filter(self):
        url = '/menu/all/?price_min=10&price_max=20'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context['dishes'], [repr(self.dish1), repr(self.dish2), repr(self.dish3),
                                                              repr(self.dish6), repr(self.dish8), repr(self.dish9)], transform=repr)

    @parameterized.expand([
        ('/menu/all/?order_by=default', 200),
        ('/menu/all/?order_by=exp_to_cheap', 200),
        ('/menu/all/?order_by=cheap_to_exp', 200),
    ])
    def test_order_by_filter(self, url, status_code):
        response = self.client.get(url)
        dishes = Dish.objects.exclude(name='test dish10')
        if 'order_by=exp_to_cheap' in url:
            dishes = Dish.objects.exclude(name='test dish10').order_by('-price')
        elif 'order_by=cheap_to_exp' in url:
            dishes = Dish.objects.exclude(name='test dish10').order_by('price')
        self.assertEquals(response.status_code, status_code)
        self.assertQuerySetEqual(response.context['dishes'], dishes)

    @parameterized.expand([
        ('/menu/all/?cuisine_type=Chinese', 200, ['test dish3', 'test dish7', 'test dish8']),
        ('/menu/all/?cuisine_type=Japanese', 200, ['test dish2', 'test dish9']),
        ('/menu/all/?cuisine_type=Thai', 200, ['test dish1', 'test dish4', 'test dish6']),
        ('/menu/all/?cuisine_type=Korean', 200, ['test dish5'])
    ])
    def test_cuisine_type(self, url, status_code, dishes):
        response = self.client.get(url)
        self.assertEquals(response.status_code, status_code)
        items = []
        for name in dishes:
            items.append(Dish.objects.get(name=name))
        self.assertQuerySetEqual(response.context['dishes'], items)

    @parameterized.expand([
        ("/menu/all/?spice=zero", 200, ['test dish1', 'test dish3', 'test dish5', 'test dish9']),
        ("/menu/all/?spice=mild", 200, ['test dish2', 'test dish6']),
        ("/menu/all/?spice=medium", 200, ['test dish4', 'test dish8']),
        ("/menu/all/?spice=hot", 200, ['test dish7']),
    ])
    def test_spice_filter(self, url, status_code, dishes):
        response = self.client.get(url)
        self.assertEquals(response.status_code, status_code)
        items = []
        for item in dishes:
            items.append(Dish.objects.get(name=item))
        self.assertQuerySetEqual(response.context['dishes'], items)

    def test_discount_filter(self):
        response = self.client.get('/menu/all/?discount=discount')
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context['dishes'], [repr(self.dish3), repr(self.dish6),
                                                              repr(self.dish8)], transform=repr)

    def test_season_filter(self):
        response = self.client.get('/menu/all/?season=season')
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context['dishes'], [repr(self.dish1)], transform=repr)
