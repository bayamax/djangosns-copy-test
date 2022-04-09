from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostCreateForm
from .models import Post
from community.models import Community
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from .forms import LoginForm
from .application import write_data
from django.contrib.auth import get_user_model

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html" 
    success_url = reverse_lazy('post:post_list')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url()) # リダイレクト

# Create your views here.


def post_list(request):
    context = {
        'post_list': Post.objects.all(),
        'reply_list': Post.objects.filter(parent__isnull=False),
        'community_list': Community.objects.all()

    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = PostCreateForm()
    return render(request, 'post/post_create.html', {'form': form})

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/login.html'

# Create your views here.
def index(req):
    return render(req, 'post/index.html')

# ajaxでurl指定したメソッド
def call_write_data(req):
    if req.method == 'GET':
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        write_data.write_csv(req.GET.get("input_data"))
        return HttpResponse()

def reply_create(request,comment_pk):
    comment = get_object_or_404(Post, id=comment_pk)
    post = comment
    form = PostCreateForm(request.POST or None)
    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = post
        reply.author = request.user
        reply.save()
        return redirect('post:post_list')

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'post/post_create.html', context)
