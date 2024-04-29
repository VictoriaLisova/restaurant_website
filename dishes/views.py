from django.shortcuts import render
from django.utils import timezone

from dishes.models import Category, Dish


def get_request(request):
    price_min = request.GET.get('price_min', None)
    price_max = request.GET.get('price_max', None)
    order_by = request.GET.get('order_by', None)
    cuisine_type = request.GET.getlist('cuisine_type', None)
    spice = request.GET.get('spice', None)
    discount = request.GET.get('discount', None)
    season = request.GET.get('season', None)
    return price_min, price_max, order_by, cuisine_type, spice, discount, season


def filter_by_price(dishes, url, price_max, price_min):
    price_min_r = 0
    price_max_r = 0

    if price_max and price_min:
        if int(price_max) > 0 and 0 < int(price_min) < int(price_max):
            dishes = dishes.filter(price__gte=int(price_min)).filter(price__lte=int(price_max))
            price_min_r = price_min
            price_max_r = price_max
            url += f'price_min={price_min}&price_max={price_max}'
    return dishes, url, price_min_r, price_max_r


def filter_by_order_by(dishes, url, order_by):
    if order_by:
        if order_by == "exp_to_cheap":
            dishes = dishes.order_by("-price")
        elif order_by == "cheap_to_exp":
            dishes = dishes.order_by("price")
        url += f'&order_by={order_by}'
    return dishes, url


def filter_by_spice(dishes, url, spice):
    if spice:
        if spice == 'zero':
            dishes = dishes.filter(spice=0)
        elif spice == 'mild':
            dishes = dishes.filter(spice=1)
        elif spice == 'medium':
            dishes = dishes.filter(spice=2)
        elif spice == 'hot':
            dishes = dishes.filter(spice__gte=3)
        url += f'&spice={spice}'
    return dishes, url


def filter_dy_discount(dishes, url, discount):
    if discount:
        dishes = dishes.filter(discount__gt=0)
        url += f'&discount={discount}'
    return dishes, url


def filter_by_cuisine_type(dishes, url, cuisine_type):
    cuisine_type_ = []
    if cuisine_type:
        for item in dishes:
            if item.kitchen_type in cuisine_type:
                cuisine_type_.append(item)
        dishes = cuisine_type_
        for c in cuisine_type:
            url += f'&cuisine_type={c}'
    return dishes, url


def get_items_to_show(dishes):
    dishes_to_show = []
    for item in dishes:
        if item.is_season and item.start_period <= timezone.now().date() <= item.end_period:
            dishes_to_show.append(item)
        elif item.is_season and not (item.start_period <= timezone.now().date() <= item.end_period):
            continue
        elif not item.is_season:
            dishes_to_show.append(item)
    return dishes_to_show


def get_season_dishes_and_items_in_cuisine_category(category_slug):
    items_in_category_cuisine = {}
    season_dishes = []
    for item in Dish.objects.all():
        if not item.is_season or (item.is_season and item.start_period <= timezone.now().date() <= item.end_period):
            if item.kitchen_type in items_in_category_cuisine:
                items_in_category_cuisine[item.kitchen_type] += 1
            else:
                items_in_category_cuisine[item.kitchen_type] = 1
        if item.is_season and item.start_period <= timezone.now().date() <= item.end_period:
            season_dishes.append(item)
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        for item in season_dishes:
            if item.category != category and category_slug != 'all':
                season_dishes.remove(item)
    return season_dishes, items_in_category_cuisine


def filter_by_season(season_dishes, dishes_to_show, url, season):
    if season:
        dishes_to_show = season_dishes.copy()
        url += f'&season={season}'
    return dishes_to_show, url


def menu(request, category_slug=None):
    categories = Category.objects.all()
    dishes = Dish.objects.all()
    category_slug_ = 'all'

    price_min, price_max, order_by, cuisine_type, spice, discount, season = get_request(request)

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        dishes = Dish.objects.filter(category=category)
        category_slug_ = category.slug

    url = '?'

    dishes, url, price_min_r, price_max_r = filter_by_price(dishes, url, price_max, price_min)
    dishes, url = filter_by_order_by(dishes, url, order_by)
    dishes, url = filter_by_spice(dishes, url, spice)
    dishes, url = filter_dy_discount(dishes, url, discount)
    dishes, url = filter_by_cuisine_type(dishes, url, cuisine_type)

    dishes_to_show = get_items_to_show(dishes)
    season_dishes, items_in_category_cuisine = get_season_dishes_and_items_in_cuisine_category(category_slug)

    dishes_to_show, url = filter_by_season(season_dishes, dishes_to_show, url, season)

    if discount:
        for item in dishes_to_show:
            if not item.discount:
                dishes_to_show.remove(item)

    if url == '?':
        url = ''

    context = {
        'title': 'Menu',
        'categories': categories,
        'dishes': dishes_to_show,
        'category_slug': category_slug_,
        'items_in_category': items_in_category_cuisine.items(),
        'season_dishes': len(season_dishes),
        'price_min': price_min_r,
        'price_max': price_max_r,
        'url': url,
    }
    if cuisine_type:
        context['cuisine_type'] = cuisine_type
    return render(request, "dishes/menu.html", context)


def create_url_to_return_to_menu(price_min, price_max, order_by, cuisine_type, spice, discount, season):
    url = '?'
    if price_min and price_max:
        url += f'price_min={price_min}&price_max={price_max}'
    if order_by:
        url += f'&order_by={order_by}'
    if cuisine_type:
        for item_c in cuisine_type:
            url += f'&cuisine_type={item_c}'
    if spice:
        url += f'&spice={spice}'
    if discount:
        url += f'&discount={discount}'
    if season:
        url += f'&season={season}'
    return url


def dish(request, category_slug=None, dish_slug=None):
    item = Dish.objects.get(slug=dish_slug)

    price_min, price_max, order_by, cuisine_type, spice, discount, season = get_request(request)
    url = create_url_to_return_to_menu(price_min, price_max, order_by, cuisine_type, spice, discount, season)

    if category_slug is None:
        category_slug = 'all'
    else:
        category = Category.objects.get(slug=category_slug)
        category_slug = category.slug
    spice_range = range(item.spice)

    if url == '?':
        url = ''

    context = {
        'title': item.name,
        'category_slug': category_slug,
        'dish': item,
        'spice_range': spice_range,
        'url': url,
    }
    return render(request, 'dishes/dish.html', context)
