from django.test import TestCase
from menu.forms import MenuItemForm
from menu.models import Category

class MenuItemFormTests(TestCase):
    """Tests for the MenuItemForm in the menu app."""

    def setUp(self):
        """Create a sample category for form usage."""
        self.category = Category.objects.create(name="Dinner")

    def test_valid_form_data(self):
        """Form should be valid with correct data."""
        form = MenuItemForm(data={
            'name': 'Pizza',
            'description': 'Wood-fired pizza',
            'price': 12.50,
            'category': self.category.id,
            'meal_type': 'dinner'
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Form should be invalid if required fields are missing."""
        form = MenuItemForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('price', form.errors)

    def test_invalid_price_format(self):
        """Form should reject non-numeric price."""
        form = MenuItemForm(data={
            'name': 'Soda',
            'description': 'Cold soda',
            'price': 'abc',
            'category': self.category.id,
            'meal_type': 'lunch'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_invalid_meal_type(self):
        """Form should reject invalid meal_type choices."""
        form = MenuItemForm(data={
            'name': 'Cake',
            'description': 'Chocolate cake',
            'price': 4.50,
            'category': self.category.id,
            'meal_type': 'snack'  # invalid
        })
        self.assertFalse(form.is_valid())
        self.assertIn('meal_type', form.errors)