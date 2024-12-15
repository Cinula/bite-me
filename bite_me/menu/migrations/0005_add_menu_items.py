from django.db import migrations

def add_menu_items(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    MenuItem = apps.get_model('menu', 'MenuItem')

    # Create categories
    starters = Category.objects.get_or_create(name='Starters')[0]
    mains = Category.objects.get_or_create(name='Main Course')[0]
    desserts = Category.objects.get_or_create(name='Desserts')[0]

    # Breakfast Items
    MenuItem.objects.create(
        name='Full English Breakfast',
        description='Two eggs, bacon, sausages, baked beans, mushrooms, grilled tomato, and toast',
        price=14.99,
        category=mains,
        meal_type='breakfast'
    )

    MenuItem.objects.create(
        name='Eggs Benedict',
        description='Poached eggs on toasted English muffins with hollandaise sauce and ham',
        price=12.99,
        category=mains,
        meal_type='breakfast'
    )

    MenuItem.objects.create(
        name='Avocado Toast',
        description='Smashed avocado on sourdough with poached eggs and chili flakes',
        price=11.99,
        category=mains,
        meal_type='breakfast'
    )

    # Lunch Items
    MenuItem.objects.create(
        name='Caesar Salad',
        description='Crisp romaine lettuce with parmesan, croutons and classic Caesar dressing',
        price=10.99,
        category=starters,
        meal_type='lunch'
    )

    MenuItem.objects.create(
        name='Gourmet Burger',
        description='Angus beef patty with caramelized onions, bacon, and cheddar cheese',
        price=16.99,
        category=mains,
        meal_type='lunch'
    )

    MenuItem.objects.create(
        name='Grilled Salmon',
        description='Fresh salmon fillet with seasonal vegetables and lemon butter sauce',
        price=18.99,
        category=mains,
        meal_type='lunch'
    )

    # Dinner Items
    MenuItem.objects.create(
        name='French Onion Soup',
        description='Classic soup with caramelized onions, beef broth, and melted Gruyère cheese',
        price=8.99,
        category=starters,
        meal_type='dinner'
    )

    MenuItem.objects.create(
        name='Beef Wellington',
        description='Prime beef fillet wrapped in mushroom duxelles and puff pastry',
        price=32.99,
        category=mains,
        meal_type='dinner'
    )

    MenuItem.objects.create(
        name='Lobster Thermidor',
        description='Lobster in a rich brandy cream sauce, gratinated with cheese',
        price=39.99,
        category=mains,
        meal_type='dinner'
    )

    MenuItem.objects.create(
        name='Crème Brûlée',
        description='Classic French vanilla custard with caramelized sugar top',
        price=8.99,
        category=desserts,
        meal_type='dinner'
    )

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0004_menuitem_meal_type'),
    ]

    operations = [
        migrations.RunPython(add_menu_items),
    ] 