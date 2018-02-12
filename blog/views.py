import datetime as dt

from django import template
from django.shortcuts import render, redirect, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, Http404
from django.conf import settings
from django.urls import reverse
from django.core.mail import mail_admins

from .models import Author, Category, Post, Tag
from .forms import FeedbackForm

# Create your views here.
def index(request):
    return HttpResponse("Hello Django")

def post_list(request):
    posts = Post.objects.all().order_by('-id')
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
    c = Category.objects.get(slug=category_slug)
    # posts = Post.objects.filter(category=c)
    posts = get_list_or_404(Post.objects.order_by('-id'), category=c)
    context = {
        'category': c,
        'posts': posts,
    }
    return render(request, 'blog/post_by_category.html', context)
def post_by_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    # posts = Post.objects.filter(tags__name=tag)
    posts = get_list_or_404(Post.objects.order_by('-id'), tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
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
