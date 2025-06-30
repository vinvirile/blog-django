from django import forms

class LoginForm(forms.Form):
    # indetifier could be either username or password
    identifier = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput())

class CreateBlogForm(forms.Form):
    title = forms.CharField(max_length=84, widget=forms.TextInput(attrs={'placeholder': 'Enter an engaging title for your post'}))
    category = forms.ChoiceField(
        choices=[
            ('', 'Select a category'),
            ('technology', 'Technology'),
            ('programming', 'Programming'),
            ('design', 'Design'),
            ('business', 'Business'),
            ('lifestyle', 'Lifestyle'),
            ('tutorial', 'Tutorial'),
            ('opinion', 'Opinion'),
            ('news', 'News')
        ]
    )
    excerpt = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Write a brief summary of your post (150 characters max)'}))
    image_url = forms.URLField(max_length=2000, required=False, widget=forms.URLInput(attrs={'placeholder': 'https://example.com/image.jpg'}))
    blog_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'content',
            'name': 'content',
            'class': 'content-editor',
            'placeholder': 'Write your blog post content here...\n\nYou can use markdown formatting:\n- **bold text**\n- *italic text*\n- # Heading 1\n- ## Heading 2\n- [link text](url)\n- > blockquote\n- `code`\n\nStart writing your amazing content!',
            'required': True
        })
    )
    tags = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Type a tag and press Enter', 'class': 'tag-input', 'id': 'tag-input'}))
    status = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'publish-immediately',
                'name': 'publish-immediately',
            }
        )
    )
