from typing import Any
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView , CreateView, UpdateView, DeleteView
from .models import Question, Comment
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse, reverse_lazy



def like_views(request, pk):
    post = get_object_or_404(Question, id=pk)
    liked = False
    if post.upvote.filter(id=request.user.id).exists():
        post.upvote.remove(request.user)
        liked = False
    else:
        post.upvote.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('Questiondetail', args=[str(pk)]))

def get_like_count(request, pk):
    question = get_object_or_404(Question, id=pk)
    total_likes = question.total_likes()
    return JsonResponse({'total_likes': total_likes})

    
class QuestionListView(LoginRequiredMixin,ListView):
    model = Question
    template_name = 'Forum/forum.html'
    context_object_name = 'questions'
    ordering = ['-date_created']
    
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        search_data = self.request.GET.get('search-area') or ""
        if search_data:
            context['questions'] = context['questions'].filter(title__icontains=search_data)
            context['search_data'] = search_data
        return context
    


class QuestionDetailView(LoginRequiredMixin,DetailView):
    model = Question
    template_name = 'Forum/questiondetail.html'
    context_object_name = 'question'

    def post(self, request, *args, **kwargs):
        question = self.get_object()
        content = request.POST.get('content')
        Comment.objects.create(question=question, user=request.user, content=content)
        return redirect('Questiondetail', pk=question.pk)
    
    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False

        if something.upvote.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked

        return context

        

class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    fields = ['title','content']
    template_name = 'Forum/createquestion.html'

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class QuestionUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['title','content']
    template_name = 'Forum/createquestion.html'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False
    

class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('home')  # Redirect URL after successful deletion

    def get(self, request, *args, **kwargs):
        # Get the question instance to be deleted
        self.object = self.get_object()
        # Perform deletion directly without a confirmation template
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
    
    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False



