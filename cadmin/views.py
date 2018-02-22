from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from blog.forms import PostForm
from blog.models import Post, Author, Category, Tag

# Create your views here.
def post_add(request):
    # If post, use bound form; else use unbound form
    if request.method == 'POST':
        f = PostForm(request.POST)

        if f.is_valid():
            f.save()
            return redirect("post_add")
        # else: print("Form not valid")
    # if request is GET, show unbound form
    else:
        f = PostForm()

    return render(request, 'cadmin/post_add.html', {'form': f})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # create a bound form
    if request.method == 'POST':
        f = PostForm(request.POST, instance=post)

        # If the form is valid, save the form and redirect
        # Else show the form w/ errors
        if f.is_valid():
            f.save()
            return redirect(reverse('post_update', args=[post.id]))
    else:
        f = PostForm(instance=post)
    context = {'form': f, 'post': post }
    return render(request, 'cadmin/post_update.html', context)

def home(request):
    if not request.user.is_authenticated():
        return redirect('login')
    return render(request, 'cadmin/admin_page.html')

def login(request, **kwargs):
    print(request)
    print(kwargs)
    if request.user.is_authenticated():
        return redirect('/cadmin/')

    # if request.method == 'POST':
    #     usr = request.POST.get('username')
    #     pwd = request.POST.get('password')
    #     usrs = User.objects.all()
    #     if (usr in [user.username for user in usrs) && (pwd in [user.password for user in usrs ]):
    #         return redirect('/cadmin/')
    #     else:
    #         continue
    else:
        return auth_views.login(request, **kwargs)
