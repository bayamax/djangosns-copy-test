from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from post.models import Post
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import User, Connection


def user_profile(request, username):
    user_model = get_user_model().objects.get(username=username)
    context = {
        'User': user_model,
        'post_list': Post.objects.filter(author=user_model.id),
        'following': Connection.objects.filter(follower__username=username).count(),
        'follower': Connection.objects.filter(following__username=username).count(),
    }
    if username is not request.user.username:
            result = Connection.objects.filter(follower__username=request.user.username).filter(following__username=username)
            context['connected'] = True if result else False
    return render(request, 'accounts/user_profile.html', context)

"""フォロー"""
@login_required
def follow_view(request, *args, **kwargs):

    try:
        #request.user.username = ログインユーザーのユーザー名を渡す。
        follower = User.objects.get(username=request.user.username)
        #kwargs['username'] = フォロー対象のユーザー名を渡す。
        following = User.objects.get(username=kwargs['username'])
    #例外処理：もしフォロー対象が存在しない場合、警告文を表示させる。
    except User.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('post:post_list'))
    #フォローしようとしている対象が自分の場合、警告文を表示させる。
    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
    else:
        #フォロー対象をまだフォローしていなければ、DBにフォロワー(自分)×フォロー(相手)という組み合わせで登録する。
        #createdにはTrueが入る
        _, created = Connection.objects.get_or_create(follower=follower, following=following)

        #もしcreatedがTrueの場合、フォロー完了のメッセージを表示させる。
        if (created):
            messages.success(request, '{}をフォローしました'.format(following.username))
        #既にフォロー相手をフォローしていた場合、createdにはFalseが入る。
        #フォロー済みのメッセージを表示させる。
        else:
            messages.warning(request, 'あなたはすでに{}をフォローしています'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': following.username}))

"""フォロー解除"""
@login_required
def unfollow_view(request, *args, **kwargs):

    try:
        follower = User.objects.get(username=request.user.username)
        following = User.objects.get(username=kwargs['username'])
        if follower == following:
            messages.warning(request, '自分自身のフォローを外せません')
        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            #フォロワー(自分)×フォロー(相手)という組み合わせを削除する。
            unfollow.delete()
            messages.success(request, 'あなたは{}のフォローを外しました'.format(following.username))
    except User.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('post:post_list'))
    except Connection.DoesNotExist:
        messages.warning(request, 'あなたは{0}をフォローしませんでした'.format(following.username))

    return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': following.username}))