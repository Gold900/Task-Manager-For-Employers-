from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date']


class PostAllView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date')


class PostUserView(ListView):
    model = Post
    template_name = 'blog/post_user.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        user_ = User.objects.get(username=user)
        data['user_'] = user_
        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# def home(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html')
