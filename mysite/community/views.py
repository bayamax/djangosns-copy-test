from django.shortcuts import render, redirect
from .forms import CommunityCreateForm
from .models import Community

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
    context = {
        'Community': Community.objects.get(name=name),
    }
    return render(request, 'community/community_top.html', context)