from django.contrib.auth import get_user_model
from django.shortcuts import render
from post.models import Post


def user_profile(request, username):
    user_model = get_user_model().objects.get(username=username)
    context = {
        'User': user_model,
        'post_list': Post.objects.filter(author=user_model.id),
    }
    return render(request, 'accounts/user_profile.html', context)
