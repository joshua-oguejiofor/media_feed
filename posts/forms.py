from django import forms

from .models import Post

ALLOWED_DOCUMENT_TYPES = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/wps-office.docx"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/webm", "video/quicktime"]
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
MAX_DOCUMENT_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_VIDEO_SIZE = 5 * 1024 * 1024     # 5MB



class PostForm(forms.ModelForm):
    caption = forms.CharField(
        label="Add a caption", 
        max_length=800, 
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Write a caption...", "rows": 4})
    )
    
    media_file = forms.FileField(label="Media")
    
    class Meta:
        model = Post
        fields = ['caption', 'media_file']

    def clean_media_file(self):
        media_file = self.cleaned_data.get("media_file")
        if not media_file:
            raise forms.ValidationError("Please select a file to upload.")

        content_type = media_file.content_type

        # 1. Validate content type
        if (content_type not in ALLOWED_IMAGE_TYPES and 
            content_type not in ALLOWED_VIDEO_TYPES and 
            content_type not in ALLOWED_DOCUMENT_TYPES):
            raise forms.ValidationError(f"Unsupported media type: {content_type}.")

        # 2. Check types and sizes for efficent storage
        if content_type in ALLOWED_IMAGE_TYPES:
            self.media_type = "image"
            if media_file.size > MAX_IMAGE_SIZE:
                raise forms.ValidationError("Image size cannot exceed 5MB.")

        elif content_type in ALLOWED_VIDEO_TYPES:
            self.media_type = "video"
            if media_file.size > MAX_VIDEO_SIZE:
                raise forms.ValidationError("Video size cannot exceed 5MB.")

        elif content_type in ALLOWED_DOCUMENT_TYPES:
            self.media_type = "document"
            if media_file.size > MAX_DOCUMENT_SIZE:
                raise forms.ValidationError("Document size cannot exceed 5MB.")
        
        return media_file
