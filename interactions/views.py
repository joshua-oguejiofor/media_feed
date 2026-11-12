from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Comment, Like
from posts.models import Post
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.



@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    next_url = request.POST.get('next') or 'feed'
    return redirect(next_url)



def add_comment(user, post, text, pk):
    
    Comment.objects.create(user=user, post=post, text=text)
    return redirect('post_detail', pk=pk)

    
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    post = comment.post
    if request.method == 'POST':     
        comment.delete()
        return redirect('post_detail', pk=post.pk)
            
    return render(
        request, 
        "delete.html", 
        {
            "title": "Comment",
            "post_pk": post.pk,            
            } 
        )
    
                
