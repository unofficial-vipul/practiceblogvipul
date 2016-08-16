from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


from .forms import CommentForm
from .models import Comment

# Create your views here.
def comment_thread(request, id):
	obj = get_object_or_404(Comment, id=id)
	content_object = obj.content_object
	content_id = obj.content_object.id

	initial_data = {
		"content_type": obj.content_type,
		"object_id":  obj.object_id
	}

	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		print form.cleaned_data
		c_type = form.cleaned_data.get('content_type')
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get('content')
		parent_id = request.POST.get('parent-id')
		parent_obj = None
		try:
			parent_id = int(request.POST.get('parent-id'))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			print parent_qs
			if parent_qs.exists():
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
								user = request.user,
								content_type = content_type,
								object_id = obj_id,
								content = content_data,
								parent = parent_obj,
							)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		"comment":obj,
		"form":form,

	}
	return 	render(request, "comment-thread.html", context) 