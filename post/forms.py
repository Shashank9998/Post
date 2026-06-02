from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "photo"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter the post title"}),
            "photo": forms.FileInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Write a comment for this post",
                    "rows": 4,
                }
            )
        }
