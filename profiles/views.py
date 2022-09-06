from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from checkout.models import Order

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

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
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
