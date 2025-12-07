from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }
        labels = {
            'content': ''
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) > 500:
            raise forms.ValidationError("Comment cannot exceed 500 characters.")
        return content
