from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.db.models import Count
from taggit.models import Tag
from .forms import CommentForm
from django.core.mail import send_mail
from .forms import EmailPostForm
from django.views.generic import ListView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

def post_share(request,pk,slug):
    post = get_object_or_404(Post,pk=pk,slug=slug,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]}, {cd["email"]} recommends you reading {post.title}'
            message = f'Read {post.title} at {post_url} \n\n comments:{cd["comment"]}'
            send_mail(subject, message,cd['email'],[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return  render(request, 'blog/share.html',{'post':post,'form':form,'sent':sent})           



def post_list(request,tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,1)
    page = request.GET.get('page')
    try :
        posts = paginator.page(page)
    except PageNotAnInteger as e:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

        
    return render(request,'blog/list.html',{'page':page,'posts':posts,'tag':tag})

# # def post_detail(request,year,month,day,post):
# #     post = get_object_or_404(Post, slug=post,status='publlished',publish__year=year,publish__month=month,publish__day=day)
# #     return render(request,'blog/detail.html',{'post':post})

def post_detail(request,slug,pk):
    
    
    post = get_object_or_404(Post,slug=slug,pk=pk)
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    context={
        'post':post,
        'comments':comments,
        'comment_form':comment_form,
        'similar_posts':similar_posts    
        }
    return render(request,'blog/detail.html',context)

# class PostListView(ListView):
#     queryset=Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 1
#     template_name='blog/list.html' 
