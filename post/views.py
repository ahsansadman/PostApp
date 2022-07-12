from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post, Comment
from .forms import CommentForm


class HomeView(ListView):
    template_name = 'post/home.html'
    queryset = Post.objects.all()
    paginate_by = 2


class PostView(DetailView):
    model = Post
    template_name = "post/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk, slug=slug)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been created successfully.')
        return reverse_lazy("post:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been updated successfully.')
        
        return reverse_lazy("post:post", kwargs={'pk': self.get_object().id, "slug" : self.get_object().slug  })

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("post:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    
    def get_success_url(self):

        messages.success(
            self.request, 'Comment has been deleted successfully.')
        return reverse_lazy("post:post", kwargs={'pk': self.get_object().post.id, "slug" : self.get_object().post.slug  })
