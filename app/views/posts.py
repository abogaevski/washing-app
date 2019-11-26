from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.utils import ObjectListMixin, objectDetailRequest

from app.models import Post

class PostList(LoginRequiredMixin, ObjectListMixin, View):
    model = Post
    template = 'app/post/post_list.html'
    context = 'posts'


def postDetailRequest(request):
    model = Post
    template = 'app/post/post_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))