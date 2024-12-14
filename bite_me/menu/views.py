from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django import forms

from .models import MenuItem, Category

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price']

def is_staff(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff)
def menu_edit_view(request):
    items = MenuItem.objects.select_related('category').all()
    categories = Category.objects.all()

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_edit')
    else:
        form = MenuItemForm()

    return render(request, 'menu/menu_edit.html', {
        'items': items,
        'categories': categories,
        'form': form
    })
