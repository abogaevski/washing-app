from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.utils import ObjectListMixin, objectDetailRequest, ObjectUpdateMixin, ObjectDetailMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from app.models import Post
from app.forms import PostUpdateEripIdForm

class PostList(LoginRequiredMixin, ObjectListMixin, View):
    model = Post
    template = 'app/post/post_list.html'
    context = 'posts'


def postDetailRequest(request):
    model = Post
    template = 'app/post/post_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))


@method_decorator(staff_member_required(login_url='login_url'), name='post')
class UnavailablePostListRequest(LoginRequiredMixin, View):
    def post(self, request):
        posts = Post.objects.filter(is_available=False).values('pk', 'post_id', 'station__owner', 'is_available', 'last_seen')
        for post in posts:
            post["last_seen"] = post["last_seen"].strftime("%d.%m.%Y %H:%M:%S")
        result = {'results': list(posts)}
        return JsonResponse(result)


class PostUpdateEripId(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostUpdateEripIdForm
    template = "app/post/post_update_erip_id.html"


class PostDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Post
    template = "app/post/post_detail_page.html"