from django import forms

from blog.models import Theme, Post


class CreateThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']
        labels = {
            'name': 'Назва'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CreatePostForm(forms.ModelForm):
    theme = forms.ModelChoiceField(queryset=Theme.objects.all(),
                                   label='Тема', empty_label='Тема не обрана',
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'theme']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class RedactPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'theme', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.Select(attrs={'class': 'form-control'}),
        }


class RedactThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
