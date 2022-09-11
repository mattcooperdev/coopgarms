from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'content': forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'title': 'Title',
            'author': 'Author',
            'content': 'Content',
            'image_url': 'Image URL',
        }

        self.fields['title'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field == "content":
                self.fields["content"].widget.attrs['class'] = 'materialize-textarea'
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
