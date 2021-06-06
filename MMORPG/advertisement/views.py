from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from .models import Post, PostCategory, Response
from .forms import PostForm
from .filters import ResponseFilter


class PostList(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    queryset = Post.objects.all()
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('posts.add_post',)

    # def post(self, request, *args, **kwargs):
    #     posts_today = Post.objects.filter(create_date__gt=timezone.now().date(), author__user=request.user)
    #
    #     # проверяем, не запостил ли данный пользователь более трех постов за сегодня
    #     if (len(posts_today) >= 3):
    #         print('На сегодня лимит постов исчерпан!')
    #         return super().get(request, *args, **kwargs)
    #
    #     form = self.form_class(request.POST)
    #
    #     post = Post(
    #         header=request.POST['header'],
    #         text=request.POST['text'][:50],
    #     )
    #
    #     if form.is_valid():
    #         form.save()
    #
    #         post_obj = Post.objects.get(header=request.POST['header'])
    #
    #         # отправка email подписантам
    #         # получем наш html
    #         html_content = render_to_string(
    #             'news_announce.html',
    #             {
    #                 'article': post,
    #                 'user': request.user,
    #                 'news_link': f'http://127.0.0.1:8000/news/{post_obj.id}'
    #             }
    #         )
    #
    #         categorys = post_obj.category.filter()
    #         subscribers = []
    #         print('222', categorys)
    #         for category in categorys:
    #             for user in category.subscribers.filter().distinct():
    #                 subscribers.append(user)
    #
    #         # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
    #         for user in subscribers:
    #             msg = EmailMultiAlternatives(
    #                 subject=f'{post.header}',
    #                 body=post.text,  # это то же, что и message
    #                 from_email='xxxx@gmail.com',
    #                 to=[user.email],  # это то же, что и recipients_list
    #             )
    #             msg.attach_alternative(html_content, "text/html")  # добавляем html
    #
    #             msg.send()  # отсылаем
    #             print('Отправили', user.email)

        # return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        post_obj = Post.objects.get(id=self.kwargs["pk"])
        response = Response(user=request.user, post=post_obj, text=request.POST.get('text-response'), accepted=False)
        response.save()

        send_mail(
            subject=f'Вам пришел новый отклик',
            message='Сделйте что-то с новым откликом!',
            from_email='xxx@gmail.com',
            recipient_list=[request.user.email]
        )

        return super().get(request, *args, **kwargs)


class ResponsesList(ListView):
    model = Post
    template_name = "responses.html"
    context_object_name = "responses"
    queryset = Response.objects.all()
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


def RespopnseDelete(request, pk):
    response = Response.objects.get(id=pk).delete()

    return redirect('/posts/responses')


def RespopnseAccept(request, pk):
    response = Response.objects.get(id=pk)
    response.accepted = True
    response.save()

    send_mail(
        subject=f'Ваш отклик был принят',
        message='Ваш отклик был принят автором объявления, что вы чувствуете?',
        from_email='ifreet4@gmail.com',
        recipient_list=[request.user.email]
    )

    return redirect('/posts/responses')