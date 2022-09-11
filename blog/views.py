from datetime import date
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.defaults import server_error


from .forms import BlogForm
from .models import Blog

def all_blogs(request):
    """ A view to show all blog posts """
    try:
        if request.method == "GET":
            blogs = Blog.objects.all().order_by("-date")

            context = {
                'blogs': blogs,
            }

            return render(request, 'blog/blog.html', context, status=200)
    except Exception:
        return server_error(request)


@login_required
def add_blog(request):
    """ Add a blog to the database """
    try:
        if not request.user.is_superuser:
            messages.error(request, "Sorry, only accessible by site owners.")
            return redirect(reverse("home"))
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully added new blog post!')
                return redirect(reverse('blog'))
            else:
                messages.error(request, 'Failed to add post. Please ensure the form is valid.')
        else:
            form = BlogForm()
            
        template = 'blog/add_blog.html'
        context = {
            'form': form,
        }

        return render(request, template, context)
    except Exception:
        return server_error(request)


@login_required
def edit_blog(request, blog_id):
    """ Edit a blog post """
    try:
        if not request.user.is_superuser:
            messages.error(request, "Sorry, only accessible by site owners.")
            return redirect(reverse("home"))
        blog = get_object_or_404(Blog, pk=blog_id)
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated blog!')
                return redirect(reverse('blog'))
            else:
                messages.error(request, 'Failed to update post. Please ensure the form is valid.')
                return
        else:
            form = BlogForm(instance=blog)

        if request.method == "GET":
            template = 'blog/edit_blog.html'
            context = {
                'form': form,
                'blog': blog,
            }

            return render(request, template, context)

        else:
            return
    except Exception:
        return server_error(request)


@login_required
def delete_blog(request, blog_id):
    """ Remove blog from the database """
    try:
        if not request.user.is_superuser:
            messages.error(request, "Sorry, only accessible by site owners.")
            return redirect(reverse("blog"))
        blog = get_object_or_404(Blog, pk=blog_id)
        blog.delete()
        messages.success(request, 'Blog post deleted!')
        return redirect(reverse('blog'))
    except Exception:
        return server_error(request)
