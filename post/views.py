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
from .forms import CoordinatesForm
from .application import write_data
from .models import Coordenadas
import folium
import branca


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
    counter = 0
    size = Post.objects.all().count()
    for counter in range(size):
        counter = counter +1
        comment = Post.objects.filter(id=counter).first()
        comment.display = 0
        comment.save()
    
    counter = 0
    cid = None

    while not Post.objects.filter(display=0).first() is None:
        comment = Post.objects.filter(parent_id=cid,display=0).first()
        if comment is None:
            counter = counter
            comment = Post.objects.filter(id=cid).first()
            cid = comment.parent_id
        else:
            counter = counter + 1
            comment.display = counter
            comment.save()
            cid = comment.id


    context = {
        'post_list': Post.objects.order_by("display"),
        'reply_list': Post.objects.filter(parent__isnull=True),
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


def coordinates_form(request):
    if request.method == 'POST':
        form = CoordinatesForm(request.POST or None)
        if form.is_valid():
            form.save()
            post = form.save(commit=False)
            post.lat = request.lat
            post.lon = request.lon
            post.save()
            return redirect('post:maps')
        context = {
            'form' : form,
            }
        return render(request, 'post/maps_form.html', context)

def maps(request):
    url = 'http://127.0.0.1:8000'
    html=f'<a href={url}> コミュニティ </a>'
    iframe = branca.element.IFrame(html=html, width=300, height=500)
    popup = folium.Popup(iframe, max_width=300)
    map = folium.Map(location=[35.690921, 139.700258], zoom_start=15)
    folium.Marker(
    location=[35.690921, 139.700258],
    popup = popup,
    icon=folium.Icon(color='red', icon='home')
    ).add_to(map)
    #folium.CircleMarker(
    #location=[35.690921, 139.700258],
    #popup='Shinjuku Station',
    #radius=40,
    #color='#ff0000',
    #fill_color='#0000ff'
    #).add_to(map)
    #coordenadas = list(Coordenadas.objects.values_list('lat','lon'))[-1]

    #map = folium.Map(coordenadas)
    #folium.Marker(coordenadas).add_to(map)
    #folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    #folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    #folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    #folium.LayerControl().add_to(map)


    map = map._repr_html_()
    context = {
        'map': map,
    }
    return render(request, 'post/maps.html', context)

def maps_comunity(request,mc):
    comment = Post.objects.filter(id=mc).first()

    return render(request, 'post/post_list.html',{'post':comment})