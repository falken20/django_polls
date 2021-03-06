from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


def example(request):
    return HttpResponse('Response')


# IndexView, DetailView and ResultView use GenericViews (django.generic)


class IndexView(generic.ListView):
    # In case not to set template_name, Django look for the template with the name
    # <app name>/<model name>_list.html
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'  # By defect <model name>_list
    
    def get_queryset(self):
        """Return the last five published questions. Not including those set to
        the published in the future"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question  # It is like code: queryset = Question.objects.all()

    # In case not to set template_name, Django look for the template with the name
    # <app name>/<model name>_detail.html
    template_name = 'polls/detail.html'

    # It could be used both of them, either queryset or get_queryset, but get_queryset
    # allows more logic.
    # queryset = Question.objects.filter(pub_date__lte=timezone.now())
    def get_queryset(self):
        """Excludes any question that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question  # It is like code: queryset = Question.objects.all()
    # In case not to set template_name, Django look for the template with the name
    # <app name>/<model name>_detail.html
    template_name = 'polls/results.html'

    # It could be used both of them, either queryset or get_queryset, but get_queryset
    # allows more logic.
    queryset = Question.objects.filter(pub_date__lte=timezone.now())
    # def get_queryset(self):


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(request.POST)
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #  KeyError raise if choice wasn’t provided in POST data
        # Redisplay the question voting form with the error message
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Please select a choice...",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # reverse() function helps avoid having to hardcode a URL in the view
        # function. It is given the name of the view that we want to pass control to and
        # the variable portion of the URL pattern that points to that view.
