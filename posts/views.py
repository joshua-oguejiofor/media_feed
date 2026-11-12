from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from interactions.views import add_comment
from interactions.models import  Like
import cloudinary.uploader
from .forms import PostForm
from .models import Post
import re


def feed(request):
    posts_list = Post.objects.select_related('author').prefetch_related('likes', 'comments')
    paginator = Paginator(posts_list, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            Like.objects.filter(user=request.user, post__in=page_obj.object_list).values_list('post_id', flat=True)
        )

    return render(request, 'posts/feed.html', {'page_obj': page_obj, 'liked_ids': liked_ids})




def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts_list = profile_user.posts.all()
    paginator = Paginator(posts_list, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'posts/profile.html', {'profile_user': profile_user, 'page_obj': page_obj})




@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.media_type = form.media_type
            
            uploaded_file = request.FILES.get('media_file')
            
            # Map Django media_type to Cloudinary resource_type
            if form.media_type == 'document':
                cloudinary_resource_type = 'raw'
            elif form.media_type == 'video':
                cloudinary_resource_type = 'video'
            else:
                cloudinary_resource_type = 'image'

            # Upload to Cloudinary with explicit resource_type
            upload_result = cloudinary.uploader.upload(
                uploaded_file,
                resource_type=cloudinary_resource_type,
                folder="posts/",
                use_filename=True,       # Preserves original file name
                unique_filename=True
            ) 

            # Assign secure URL string to post.media_file
            post.media_file = upload_result.get('secure_url')
            post.save()
            
            return redirect('feed')
    else:
        form = PostForm()
        
    return render(request, 'posts/create_post.html', {'form': form})




@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text', '').strip().lower()
        if text:
            add_comment(user=request.user, post=post, text=text, pk=pk)
            
    comments = post.comments.select_related('user')
    liked = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'liked': liked})

 

def _delete_cloudinary_asset(file_url, media_type):
    print("data enterint the delete from update:", file_url, media_type)
    """Extracts public_id from Cloudinary URL and deletes the asset."""
    if not file_url or 'cloudinary.com' not in str(file_url):
        return

    try:
        # Extract everything after '/upload/' (excluding version 'v12345/') up to extension
        match = re.search(r'/upload/(?:v\d+/)?(.+?)(?:\.[a-zA-Z0-9]+)?$', str(file_url))
        if match:
            public_id = match.group(1)
            
            # Map media_type to resource_type
            resource_type = 'raw' if media_type == 'document' else media_type
            
            # Delete from Cloudinary
            cloudinary.uploader.destroy(public_id, resource_type=resource_type)
    except Exception as e:
        print(f"Failed to delete Cloudinary asset: {e}")




@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    delete_old_url = post.media_file

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
            updated_post = form.save(commit=False)
            
            uploaded_file = request.FILES.get('media_file')
            
                # 1. DELETE OLD FILE FROM CLOUDINARY
            _delete_cloudinary_asset(delete_old_url, post.media_type)

            # 2. UPLOAD NEW FILE
            updated_post.media_type = form.media_type
            cloudinary_resource_type = 'raw' if form.media_type == 'document' else form.media_type

            upload_result = cloudinary.uploader.upload(
                uploaded_file,
                resource_type=cloudinary_resource_type,
                folder="posts/"
            )
            
            updated_post.media_file = upload_result.get('secure_url')

            updated_post.save()
            return redirect('feed')   
    else:
        form = PostForm(instance=post)
        
    return render(request, 'posts/create_post.html', {'form': form})



@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        # 1. Delete asset from Cloudinary
        _delete_cloudinary_asset(post.media_file, post.media_type)
        
        # 2. Delete post record from database
        post.delete()
        return redirect('feed')
    
    return render(
        request, "delete.html", 
        {
            "title": "Post",
            "post_pk": post.pk,
        }
    )

