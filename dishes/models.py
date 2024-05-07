from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    position = models.PositiveIntegerField(default=1, null=False, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'
        ordering = ['position']

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    kitchen_type = models.CharField(max_length=255, unique=False, null=False)
    composition = models.TextField(null=True, blank=True)
    weight = models.PositiveIntegerField(default=0)
    caloric = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="dish_images", blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    spice = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="dishes")
    is_season = models.BooleanField(default=False)
    start_period = models.DateField(null=True)
    end_period = models.DateField(null=True)

    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'
        db_table = 'dish'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount/100, 2)
        return self.price



