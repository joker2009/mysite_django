# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from .forms import EmailPostForm
from django.core.mail import send_mail


def post_list(request):
    # posts = Post.published.all()
    # return render(request,
    #               'blog/post/list.html',
    #               {'posts': posts})
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  #3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
        # If page is not an integer deliver the first page
    except PageNotAnInteger:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


# my hp_computer

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    print('0')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        print('1')
        if form.is_valid():
            cd = form.cleaned_data
            print('2')
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            print(3)
            send_mail(subject, message, '304640509@qq.com', [cd['to']])
            sent = True
            print(4)
    else:
        form = EmailPostForm()
    print(5)
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

