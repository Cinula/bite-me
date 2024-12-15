from django.db import migrations

def add_menu_items(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    MenuItem = apps.get_model('menu', 'MenuItem')

    # Create categories
    starters = Category.objects.get_or_create(name='Starters')[0]
    mains = Category.objects.get_or_create(name='Main Course')[0]
    desserts = Category.objects.get_or_create(name='Desserts')[0]
    sides = Category.objects.get_or_create(name='Sides')[0]

    # Breakfast Items
    breakfast_items = [
        {
            'name': 'Full English Breakfast',
            'description': 'Two eggs, bacon, sausages, baked beans, mushrooms, grilled tomato, and toast',
            'price': 14.99,
            'category': mains,
            'meal_type': 'breakfast'
        },
        {
            'name': 'French Toast',
            'description': 'Brioche bread dipped in vanilla custard, served with caramelized bananas and maple syrup',
            'price': 13.99,
            'category': mains,
            'meal_type': 'breakfast'
        },
        {
            'name': 'Eggs Benedict',
            'description': 'Poached eggs on toasted English muffins with hollandaise sauce and ham',
            'price': 12.99,
            'category': mains,
            'meal_type': 'breakfast'
        },
        {
            'name': 'Avocado Toast',
            'description': 'Smashed avocado on sourdough with poached eggs and chili flakes',
            'price': 11.99,
            'category': mains,
            'meal_type': 'breakfast'
        },
        {
            'name': 'Acai Bowl',
            'description': 'Blended acai, granola, fresh fruits, honey, and chia seeds',
            'price': 11.99,
            'category': mains,
            'meal_type': 'breakfast'
        }
    ]

    # Lunch Items
    lunch_items = [
        {
            'name': 'Caesar Salad',
            'description': 'Crisp romaine lettuce with parmesan, croutons and classic Caesar dressing',
            'price': 10.99,
            'category': starters,
            'meal_type': 'lunch'
        },
        {
            'name': 'Tom Yum Soup',
            'description': 'Spicy and sour Thai soup with prawns and mushrooms',
            'price': 8.99,
            'category': starters,
            'meal_type': 'lunch'
        },
        {
            'name': 'Gourmet Burger',
            'description': 'Angus beef patty with caramelized onions, bacon, and cheddar cheese',
            'price': 16.99,
            'category': mains,
            'meal_type': 'lunch'
        },
        {
            'name': 'Poke Bowl',
            'description': 'Fresh tuna, sushi rice, edamame, avocado, and ponzu sauce',
            'price': 16.99,
            'category': mains,
            'meal_type': 'lunch'
        },
        {
            'name': 'Mediterranean Pasta',
            'description': 'Penne with sun-dried tomatoes, olives, feta, and pine nuts',
            'price': 14.99,
            'category': mains,
            'meal_type': 'lunch'
        }
    ]

    # Dinner Items
    dinner_items = [
        {
            'name': 'Beef Carpaccio',
            'description': 'Thinly sliced beef with truffle oil, rocket, and parmesan',
            'price': 13.99,
            'category': starters,
            'meal_type': 'dinner'
        },
        {
            'name': 'Tempura Prawns',
            'description': 'Crispy prawns with sweet chili dipping sauce',
            'price': 12.99,
            'category': starters,
            'meal_type': 'dinner'
        },
        {
            'name': 'Beef Wellington',
            'description': 'Prime beef fillet wrapped in pastry with mushroom duxelles',
            'price': 29.99,
            'category': mains,
            'meal_type': 'dinner'
        },
        {
            'name': 'Rack of Lamb',
            'description': 'Herb-crusted lamb rack with mint jus and roasted vegetables',
            'price': 31.99,
            'category': mains,
            'meal_type': 'dinner'
        },
        {
            'name': 'Seafood Linguine',
            'description': 'Mixed seafood in white wine and garlic sauce',
            'price': 24.99,
            'category': mains,
            'meal_type': 'dinner'
        }
    ]

    # Sides
    side_items = [
        {
            'name': 'Sweet Potato Fries',
            'description': 'Crispy sweet potato fries with chipotle mayo',
            'price': 6.99,
            'category': sides,
            'meal_type': 'dinner'
        },
        {
            'name': 'Truffle Mac and Cheese',
            'description': 'Creamy macaroni cheese with truffle oil',
            'price': 8.99,
            'category': sides,
            'meal_type': 'dinner'
        },
        {
            'name': 'Garlic Bread',
            'description': 'Sourdough with garlic butter and herbs',
            'price': 5.99,
            'category': sides,
            'meal_type': 'lunch'
        }
    ]

    # Desserts
    dessert_items = [
        {
            'name': 'Crème Brûlée',
            'description': 'Classic vanilla custard with caramelized sugar top',
            'price': 8.99,
            'category': desserts,
            'meal_type': 'dinner'
        },
        {
            'name': 'Chocolate Fondant',
            'description': 'Warm chocolate cake with a melting center, served with vanilla ice cream',
            'price': 8.99,
            'category': desserts,
            'meal_type': 'dinner'
        }
    ]

    # Create all menu items
    for item in breakfast_items + lunch_items + dinner_items + side_items + dessert_items:
        MenuItem.objects.create(**item)

class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_menu_items),
    ] 