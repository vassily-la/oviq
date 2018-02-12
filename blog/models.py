from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.
class Author(models.Model):
    # Change the field label
    name = models.CharField(max_length=100, unique=True, verbose_name="Author name")
    email = models.EmailField(unique=True)
    # blank = True means required
    # email = models.EmailField(unique=True, blank=True)
    active = models.BooleanField(default=False)
    created_on=models.DateTimeField(null=True)
    last_logged_in=models.DateTimeField(null=True)

    class Meta:

        unique_together = (('name', 'email'),)

    def __str__(self):
        return self.name +": "+ self.email

    # def get_absolute_url(self):



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        # db_tables = "blog_category"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return f'/category/{self.slug}/'
        return reverse('post_by_category', args=[self.slug])

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_by_tag', args=[self.slug])

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Produced automatically from the slug")
    content = models.TextField()
    # DateField and DateTimeField values with auto_now and auto_now_add don't appear in the admin console, and
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id, self.slug])

class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return self.name + "-" + self.email
