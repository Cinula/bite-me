from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import MenuItem, Category
from .forms import MenuItemForm

def menu_view(request):
    """
    Render the public menu page accessible by all users.
    """
    categories = Category.objects.prefetch_related('items').all()
    context = {
        'categories': categories
    }
    return render(request, 'menu/menu.html', context)


def is_staff_user(user):
    """Check if the user is staff or superuser."""
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff_user)
def menu_edit_view(request):
    """
    Render the menu management page for admins.
    Allows adding new menu items and viewing existing ones.
    """
    categories = Category.objects.all()
    items = MenuItem.objects.select_related('category').all()

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added successfully.")
            return redirect('menu_edit')
        else:
            messages.error(request, "Error adding menu item. Please check the form.")
    else:
        form = MenuItemForm()

    context = {
        'form': form,
        'categories': categories,
        'items': items
    }
    return render(request, 'menu/menu_edit.html', context)
