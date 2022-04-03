from django.shortcuts import render, redirect
from .forms import CommunityCreateForm, CommunityPostCreateForm
from .models import Community, CommunityPost

# Create your views here.


def community_create(request):
    if request.method == "POST":
        form = CommunityCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = CommunityCreateForm()
    return render(request, 'community/community_create.html', {'form': form})

def community_top(request, name):
    community = Community.objects.get(name=name)
    communitypost = CommunityPost.objects.filter(community=community)
    if request.method == "POST":
        form = CommunityPostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.community = community
            post.save()
            return redirect('community:community_top', name=name)
    else:
        form = CommunityPostCreateForm()
    return render(request, 'community/community_top.html', {'form': form, 'Community': community, 'CommunityPost': communitypost})