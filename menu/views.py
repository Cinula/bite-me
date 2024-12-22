from django.shortcuts import render, redirect, get_object_or_404
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
    """Handle menu editing."""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            form = MenuItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Menu item added successfully.')
                return redirect('menu_edit')
            else:
                messages.error(request, 'Error adding menu item. Please check the form.')
        
        elif action == 'edit':
            item_id = request.POST.get('item_id')
            item = MenuItem.objects.get(id=item_id)
            form = MenuItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, 'Menu item updated successfully.')
                return redirect('menu_edit')
            else:
                messages.error(request, 'Error updating menu item. Please check the form.')
        
        elif action == 'delete':
            item_id = request.POST.get('item_id')
            try:
                item = MenuItem.objects.get(id=item_id)
                item.delete()
                messages.success(request, 'Menu item deleted successfully.')
            except MenuItem.DoesNotExist:
                messages.error(request, 'Menu item not found.')
            return redirect('menu_edit')
    
    categories = Category.objects.prefetch_related('items').all()
    form = MenuItemForm()
    
    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'menu/menu_edit.html', context)

@user_passes_test(lambda u: u.is_staff)
def edit_menu_item(request, pk):
    """Handle menu item editing."""
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.name}" has been updated successfully.')
            return redirect('menu_edit')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('menu_edit')

@user_passes_test(lambda u: u.is_staff)
def delete_menu_item(request, pk):
    """Handle menu item deletion."""
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f'"{item_name}" has been deleted successfully.')
    
    return redirect('menu_edit')
