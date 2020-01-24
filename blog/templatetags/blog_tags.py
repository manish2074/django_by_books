from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
from blog.models import Post

@register.simple_tag(name='my_tag')
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=4):
    return Post.published.annotate(total_comment=Count('comments')).order_by('-total_comment','-publish')[:count] #comments vaneko field ko ho
    
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))