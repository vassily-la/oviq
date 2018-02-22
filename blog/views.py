import datetime as dt

from django import template
from django.shortcuts import render, redirect, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.conf import settings
from django.urls import reverse
from django.core.mail import mail_admins
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages, auth

from oviqpr import helpers
from .models import Author, Category, Post, Tag
from .forms import FeedbackForm

# Create your views here.
def index(request):
    return HttpResponse("Hello Django")

def post_list(request):
    posts = Post.objects.all().order_by('-id')
    posts = helpers.pg_records(request, posts, 3)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk, post_slug):
    post = get_object_or_404(Post, pk=pk)
    # try:
    #     post = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:
    #     raise Http404("Post not found2")
        # return HttpResponseNotFound("Page not found")
    return render(request, 'blog/post_detail.html', {'post': post})

def post_by_category(request, category_slug):
    # c = Category.objects.get(slug=category_slug)
    # posts = Post.objects.filter(category=c)
    c = get_object_or_404(Category, slug=category_slug)
    posts = get_list_or_404(Post.objects.order_by('-id'), category=c)
    posts = helpers.pg_records(request, posts, 2)
    context = {'category': c, 'posts': posts,}
    return render(request, 'blog/post_by_category.html', context)

def post_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    # tag = Tag.objects.get(slug=tag_slug)
    # posts = Post.objects.filter(tags__name=tag)
    posts = get_list_or_404(Post.objects.order_by('-id'), tags=tag)
    posts = helpers.pg_records(request, posts, 2)
    context = {'tag': tag, 'posts': posts, }
    return render(request, 'blog/post_by_tag.html', context)

def test_redirect(request):
    # c = Category.objects.get(name='python')
    # d = redirect(c)
    # print(d)
    return redirect('/category/python/')
    # return HttpResponsePermanentRedirect(reverse('post_list'))

def feedback(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data['name']
            sender = f.cleaned_data['email']
            subj = f.cleaned_data['subject']
            msg = f.cleaned_data['message']
            subject = f"You have a new Message from {name}: {sender}."
            message = f"Subject: {subj}\n\nMessage:\n{msg}"
            mail_admins(subject, message)
            f.save()
            return redirect('feedback')
    else:
        f = FeedbackForm()

    return render(request, 'blog/feedback.html', {'form': f})

def test_cookie(request):
    if not request.COOKIES.get('color'):
        response = HttpResponse("Cookie Set")
        response.set_cookie('color', 'blue')
        return response
    else:
        return HttpResponse(f"Your favorite color is {request.COOKIES['color']}")

def track_user(request):
    response = render(request, 'blog/track_user.html')
    if not request.COOKIES.get('visits'):
        response.set_cookie('visits', '1', 3600*24*365)
    else:

        visits = int(request.COOKIES.get('visits', '1')) + 1
        response.set_cookie('visits', str(visits), 3600*24*365)
    return response

def stop_tracking(request):
    if request.COOKIES.get('visits'):
        response = HttpResponse("Cookies cleared")
        response.delete_cookie('visits')
    else:
        response = HttpResponse("We're not tracking you.")
    return response

def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse("Testing session cookie")

def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie Test Passed")
    else:
        response = HttpResponse("Cookie test failed.")
    return response

def save_session_data(request):
    request.session['id'] = 1
    request.session['name'] = 'root'
    request.session['password'] = 'rootpass'
    return HttpResponse("Session data saved!")

def access_session_data(request):
    response = ""
    if request.session.get('id'):
        response += f"ID: {request.session.get('id')} <br>"
    if request.session.get('name'):
        response += f"Name: {request.session.get('name')} <br>"
    if request.session.get('password'):
        response += f"Password: {request.session.get('password')}"
    if not response:
        response = "No session data"

    return HttpResponse(response)

def delete_session_data(request):
    try:
        del request.session['id']
        del request.session['name']
        del request.session['password']
    except KeyError:
        print("Some error with deleting session data")
    return HttpResponse("Session data cleared")

def lousy_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'root' and password == 'pass':
            request.session['logged_in'] = True
            return redirect('lousy_secret')
        else:
            messages.error(request, 'Error wrong username/password')
    return render(request, 'blog/lousy_login.html')

def lousy_secret(request):
    if not request.session.get('logged_in'):
        return redirect('lousy_login')
    return render(request, 'blog/lousy_secret_page.html')

def lousy_logout(request):
    try:
        del request.session['logged_in']
    except KeyError:
        return redirect('lousy_login')
    return render(request, 'blog/lousy_logout.html')

def login(request):
    print(1)
    if request.user.is_authenticated():
        print(2)
        return redirect('admin_page')
    print(10)
    if request.method == 'POST':
        print(3)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print(4)
            auth.login(request, user)
            return redirect('admin_page')

        else:
            print(5)
            messages.error(request, 'Error: wrong username/password')

    else:
        print(6)
    return render(request, 'blog/login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'blog/logout.html')

def admin_page(request):
    if not request.user.is_authenticated():
        return redirect('blog_login')
    return render(request, 'blog/admin_page.html')

# def track_user(request):
#     if not request.COOKIES.get('visits'):
#         resp  = ("This is your first visit to the site.\n")
#         resp +=  ("From now on I will track your visits.")
#         response = HttpResponse(resp)
#         response.set_cookie('visits', '1', 3600*24*365)
#     else:
#         visits = int(request.COOKIES.get('visits')) + 1
#         response = HttpResponse(f"This is your visit {visits}.")
#         response.set_cookie('visits', str(visits), 3600*24*365)
#         # response.set_cookie()
#     return response
