from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from website.forms import CommentForm, EditCommentForm
from website.models import Comment, Publication


class CommentView(View):
    @method_decorator(login_required)
    def post(self, request):
        form = CommentForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("<p>Form was invalid</p>")

        parent_id = request.POST["parent"]
        parent = Comment.objects.get(pk=parent_id) if parent_id != "" else None
        is_parent_comment = parent is None
        level = 0 if is_parent_comment else parent.level + 1
        pub = get_object_or_404(Publication, pk=request.POST["pubid"])

        the_comment = Comment(
            text=form.cleaned_data["text"],
            publication=pub,
            created_by=request.user,
            parent_comment=parent,
            level=level,
        )
        the_comment.save()

        return render(
            request,
            "website/components/comment/comment.html",
            {"com": the_comment, "pub": pub},
        )

    @method_decorator(login_required)
    def delete(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        if comment.created_by.id != request.user.id:
            return HttpResponseBadRequest("Unauthorized")
        comment.delete_comment()
        return HttpResponse(comment.text)  # Will return 'Deleted Comment'


@require_http_methods(["GET", "POST"])
def edit_comment(request, comment_id):
    # TODO very inefficient, we should avoid a DB hit for this GET. Solve in frontend
    if request.method == "GET":
        comment = Comment.objects.get(pk=comment_id)
        context = {
            "comment_id": comment_id,
            "form": EditCommentForm(initial={"text": comment.text}),
        }
        return render(request, "website/components/comment/comment_edit.html", context)
    elif request.method == "POST":
        form = EditCommentForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        comment = Comment.objects.get(pk=comment_id)
        if comment.created_by.id != request.user.id:
            return HttpResponseBadRequest("Unauthorized")
        comment.text = form.cleaned_data["text"]
        comment.save()
        return render(
            request, "website/components/comment/comment_text.html", {"com": comment}
        )
