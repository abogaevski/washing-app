from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.utils import ObjectListMixin, objectDetailRequest
from django.core import serializers

from app.models import Post

class PostList(LoginRequiredMixin, ObjectListMixin, View):
    model = Post
    template = 'app/post/post_list.html'
    context = 'posts'


def postDetailRequest(request):
    model = Post
    template = 'app/post/post_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))


class UnavailablePostListRequest(View):
    def post(self, request):
        posts = Post.objects.filter(is_available=False).values('pk', 'post_id', 'station__owner', 'is_available', 'last_seen')
        result = {'results': list(posts)}
        return JsonResponse(result)