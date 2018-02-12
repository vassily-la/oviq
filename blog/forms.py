from django import forms
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify

from .models import Author, Category, Post, Tag, Feedback

# class AuthorForm(forms.Form):
class AuthorForm(forms.ModelForm):
    # name = forms.CharField(max_length=100)
    # email = forms.EmailField()
    # active = forms.BooleanField(required=False)
    # created_on = forms.DateTimeField()
    # last_logged_in = forms.DateTimeField()
    class Meta:
        model = Author
        fields = '__all__'
        # field = ['title', 'content']
    #....
    #....

    def clean_name(self):
        name = self.cleaned_data['name']
        name_l = name.lower()
        if name_l in ['admin', 'uthor']:
            raise ValidationError("Author name can't be 'admin' or 'author'.")
        return name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Author.objects.filter(email=email)
        if r.count:
            raise ValidationError(f'{email} already exists.')
        return self.cleaned_data['email'].lower()

    # def save(self):
    #     new_author = Author.objects.create(
    #         name = self.cleaned_data['name'],
    #         email = self.cleaned_data['email'],
    #         active = self.cleaned_data['active'],
    #         created_on = self.cleaned_data['created_on'],
    #         last_logged_in = self.cleaned_data['last_logged_in'],
    #     )
    #     return new_author

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"

    def clean_name(self):
        n = self.cleaned_data['name']
        nl = n.lower()
        if nl in ['tag', 'add', 'update']:
            raise ValidationError(f"Tag can't be {n}.")
        return n
    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def clean_name(self):
        n = self.cleaned_data['name']
        nl = n.lower()
        if nl in ['tag', 'add', 'update']:
            raise ValidationError(f"Category name can't be {n}.")
        return n
    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'author', 'category', 'tags')

    def clean_name(self):
        n = self.cleaned_data['name']
        nl = n.lower()
        if nl in ['tag', 'add', 'update']:
            raise ValidationError(f"Post name can't be {n}.")
            return n
    def clean(self):
        # Call the parent clean method
        # Does nothing except returning cleaned_data dictionary
        cleaned_data = super(PostForm, self).clean()
        title = cleaned_data.get('title')
        # If title exists, create a slug
        if title:
            cleaned_data['slug'] = slugify(title)
        return cleaned_data

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
