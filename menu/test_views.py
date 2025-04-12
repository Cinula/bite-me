from django.test import TestCase
from django.urls import reverse
from menu.models import Category, MenuItem

from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import resolve_url


# Create your tests here.

class PublicMenuViewTests(TestCase):
    """Tests for the publicly visible menu view (menu_view)."""

    def setUp(self):
        """Set up a sample category and menu item for testing."""
        self.category = Category.objects.create(name="Mains")
        MenuItem.objects.create(
            name="Pizza",
            description="Cheesy and delicious",
            price=9.99,
            category=self.category,
            meal_type="lunch"
        )

    def test_menu_view_status_code(self):
        """The menu page should return HTTP 200."""
        response = self.client.get(reverse('menu'))  # Update 'menu' if your URL name differs
        self.assertEqual(response.status_code, 200)

    def test_menu_view_uses_correct_template(self):
        """The menu page should use the correct template."""
        response = self.client.get(reverse('menu'))
        self.assertTemplateUsed(response, 'menu/menu.html')

    def test_menu_view_context_contains_categories(self):
        """The view should include categories in the context."""
        response = self.client.get(reverse('menu'))
        self.assertIn(self.category, response.context['categories'])


class MenuEditViewTests(TestCase):
    """Tests for the staff-only menu editing view (menu_edit_view)."""

    def setUp(self):
        """Create a staff and non-staff user for access control tests."""
        self.staff_user = User.objects.create_user(username='admin', password='pass')
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.non_staff_user = User.objects.create_user(username='user', password='pass')

    def test_edit_redirects_for_anonymous(self):
        """Anonymous users should be redirected (likely to login)."""
        response = self.client.get(reverse('menu_edit'))
        self.assertEqual(response.status_code, 302)

    def test_edit_redirects_for_non_staff(self):
        """Non-staff users should be redirected to login page."""
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('menu_edit'))

        self.assertEqual(response.status_code, 302)

        login_url = resolve_url(settings.LOGIN_URL)
        expected_redirect = f"{login_url}?next={reverse('menu_edit')}"
        self.assertEqual(response.url, expected_redirect)

    def test_edit_loads_for_staff(self):
        """Staff users should be able to load the menu editing page."""
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('menu_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_edit.html')