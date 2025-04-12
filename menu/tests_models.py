from django.test import TestCase
from menu.models import Category, MenuItem

# Create your tests here.

class MenuModelTests(TestCase):
    """Unit tests for the models in the menu app."""

    def setUp(self):
        """Set up a category and menu item for testing."""
        self.category = Category.objects.create(name="Breakfast")
        self.menu_item = MenuItem.objects.create(
            name="Pancakes",
            description="Fluffy pancakes with syrup",
            price=7.99,
            category=self.category,
            meal_type='breakfast'
        )

    def test_category_str(self):
        """Category __str__ should return the category name."""
        self.assertEqual(str(self.category), "Breakfast")

    def test_menu_item_str(self):
        """MenuItem __str__ should return the item name."""
        self.assertEqual(str(self.menu_item), "Pancakes")

    def test_menu_item_defaults(self):
        """MenuItem default values should be set and image should be optional."""
        self.assertEqual(self.menu_item.meal_type, 'breakfast')
        self.assertFalse(bool(self.menu_item.image))

    def test_menu_item_category_relationship(self):
        """MenuItem should appear in the related items of its category."""
        self.assertIn(self.menu_item, self.category.items.all())