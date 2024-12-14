# menu/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django import forms
from django.contrib import messages
from .models import MenuItem, Category

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


def is_staff_user(user):
    """Check if the user is staff or superuser."""
    return user.is_staff or user.is_superuser


@user_passes_test(is_staff_user)
def menu_edit_view(request):
    """Allow staff to add and view menu items."""
    items = MenuItem.objects.select_related('category').all()
    categories = Category.objects.all()

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added successfully.")
            return redirect('menu_edit')
        else:
            messages.error(request, "Error adding menu item. Please check the form.")
    else:
        form = MenuItemForm()

    context = {
        'items': items,
        'categories': categories,
        'form': form
    }
    return render(request, 'menu/menu_edit.html', context)
