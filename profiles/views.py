from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from checkout.models import Order
from products.models import Product

from .models import UserProfile
from .forms import UserProfileForm, UserDeleteForm


@login_required
def profile(request):
    '''Display the user's profile'''
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,
                           'Update failed.\
                            Please check details and try again.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    '''shows history of completed orders'''
    order = get_object_or_404(Order, order_number=order_number)
    template = 'checkout/order-history.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def deleteProfile(request):
    '''
    View to delete profile after confirming email address
    '''
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserDeleteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('email') == profile.user.email:
                user = request.user
                logout(request)
                user.delete()
                messages.success(request, 'Account deleted!')
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Incorrect email entered!')
    else:
        form = UserDeleteForm()
        context = {'form': form}
        return render(request, 'profiles/delete_profile.html', context)


@login_required
def wishlist(request):
    '''view to render wishlist'''
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "profiles/user_wish_list.html",
                  {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    '''view to add product to wishlist'''
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title + " has been\
            removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to\
            your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
